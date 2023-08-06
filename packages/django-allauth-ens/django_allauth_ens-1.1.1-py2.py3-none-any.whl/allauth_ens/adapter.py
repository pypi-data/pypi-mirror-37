# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from allauth.account.utils import user_email, user_field, user_username
from allauth.socialaccount.adapter import (
    DefaultSocialAccountAdapter, get_account_adapter, get_adapter,
)
from allauth.socialaccount.models import SocialAccount

import ldap

from .utils import (
    extract_infos_from_ldap, get_clipper_email, get_ldap_infos, init_ldap,
    remove_email,
)

User = get_user_model()


class LongTermClipperAccountAdapter(DefaultSocialAccountAdapter):
    """
    A class to manage the fact that people loose their account at the end of
    their scolarity and that their clipper login might be reused later
    """

    def pre_social_login(self, request, sociallogin):
        """
        If a clipper connection has already existed with the uid, it checks
        that this connection still belongs to the user it was associated with.

        This check is performed by comparing the entrance years provided by the
        LDAP.

        If the check succeeds, it simply reactivates the clipper connection as
        belonging to the associated user.

        If the check fails, it frees the elements (as the clipper email
        address) which will be assigned to the new connection later.
        """

        if sociallogin.account.provider != "clipper":
            return super(LongTermClipperAccountAdapter,
                         self).pre_social_login(request, sociallogin)

        clipper_uid = sociallogin.account.uid
        try:
            old_conn = SocialAccount.objects.get(provider='clipper_inactive',
                                                 uid=clipper_uid)
        except SocialAccount.DoesNotExist:
            return

        # An account with that uid was registered, but potentially
        # deprecated at the beginning of the year
        # We need to check that the user is still the same as before
        ldap_data = get_ldap_infos(clipper_uid)
        sociallogin._ldap_data = ldap_data

        if ldap_data is None or 'entrance_year' not in ldap_data:
            raise ValueError("No entrance year in LDAP data")

        old_conn_entrance_year = (
            old_conn.extra_data.get('ldap', {}).get('entrance_year'))

        if old_conn_entrance_year != ldap_data['entrance_year']:
            # We cannot reuse this SocialAccount, so we need to invalidate
            # the email address of the previous user to prevent conflicts
            # if a new SocialAccount is created
            email = ldap_data.get('email', get_clipper_email(clipper_uid))
            remove_email(old_conn.user, email)

            return

        # The admission year is the same, we can update the model and keep
        # the previous SocialAccount instance
        old_conn.provider = 'clipper'
        old_conn.save()

        # Redo the thing that had failed just before
        sociallogin.lookup()

    def get_username(self, clipper_uid, data):
        """
        Util function to generate a unique username, by default 'clipper@promo'
        """
        if data is None or 'entrance_year' not in data:
            raise ValueError("No entrance year in LDAP data")
        return "{}@{}".format(clipper_uid, data['entrance_year'])

    def save_user(self, request, sociallogin, form=None):
        if sociallogin.account.provider != "clipper":
            return super(LongTermClipperAccountAdapter,
                         self).save_user(request, sociallogin, form)
        user = sociallogin.user
        user.set_unusable_password()

        clipper_uid = sociallogin.account.uid
        ldap_data = sociallogin._ldap_data if \
            hasattr(sociallogin, '_ldap_data') \
            else get_ldap_infos(clipper_uid)

        username = self.get_username(clipper_uid, ldap_data)
        email = ldap_data.get('email', get_clipper_email(clipper_uid))
        name = ldap_data.get('name')
        user_username(user, username or '')
        user_email(user, email or '')
        name_parts = (name or '').split(' ')
        user_field(user, 'first_name', name_parts[0])
        user_field(user, 'last_name', ' '.join(name_parts[1:]))

        # Entrance year and department, if the user has these fields
        entrance_year = ldap_data.get('entrance_year', '')
        dep_code = ldap_data.get('department_code', '')
        dep_fancy = ldap_data.get('department', '')
        promotion = u'%s %s' % (dep_fancy, entrance_year)
        user_field(user, 'entrance_year', entrance_year)
        user_field(user, 'department_code', dep_code)
        user_field(user, 'department', dep_fancy)
        user_field(user, 'promotion', promotion)

        # Ignore form
        get_account_adapter().populate_username(request, user)

        # Save extra data (only once)
        sociallogin.account.extra_data['ldap'] = ldap_data
        sociallogin.save(request)
        sociallogin.account.save()

        return user


def deprecate_clippers():
    """
    Marks all the SocialAccount with clipper as deprecated, by setting their
    provider to 'clipper_inactive'
    """

    clippers = SocialAccount.objects.filter(provider='clipper')
    c_uids = clippers.values_list('uid', flat=True)

    # Clear old clipper accounts that were replaced by new ones
    # (to avoid conflicts)
    SocialAccount.objects.filter(provider='clipper_inactive',
                                 uid__in=c_uids).delete()

    # Deprecate accounts
    clippers.update(provider='clipper_inactive')


def install_longterm_adapter(fake=False):
    """
    Manages the transition from an older django_cas or an allauth_ens
    installation without LongTermClipperAccountAdapter
    """

    accounts = {u.username: u for u in User.objects.all()
                if u.username.isalnum()}
    ldap_connection = init_ldap()
    ltc_adapter = get_adapter()

    info = ldap_connection.search_s(
        'dc=spi,dc=ens,dc=fr',
        ldap.SCOPE_SUBTREE,
        ("(|{})".format(''.join(("(uid=%s)" % (un,))
                                for un in accounts.keys()))),
        ['uid',
         'cn',
         'mailRoutingAddress',
         'homeDirectory'])

    logs = {"created": [], "updated": []}
    cases = []

    for userinfo in info:
        infos = userinfo[1]
        data = extract_infos_from_ldap(infos)
        clipper_uid = data['clipper_uid']
        user = accounts.get(clipper_uid, None)
        if user is None:
            continue
        user.username = ltc_adapter.get_username(clipper_uid, data)
        if fake:
            cases.append(clipper_uid)
        else:
            user.save()
            cases.append(user.username)

        try:
            sa = SocialAccount.objects.get(provider='clipper', uid=clipper_uid)
            if not sa.extra_data.get('ldap'):
                sa.extra_data['ldap'] = data
                if not fake:
                    sa.save(update_fields=['extra_data'])
                logs["updated"].append((clipper_uid, user.username))
        except SocialAccount.DoesNotExist:
            sa = SocialAccount(
                provider='clipper', uid=clipper_uid,
                user=user, extra_data={'ldap': data},
            )
            if not fake:
                sa.save()
            logs["created"].append((clipper_uid, user.username))

    logs["unmodified"] = User.objects.exclude(username__in=cases)\
                                     .values_list("username", flat=True)
    return logs
