from __future__ import unicode_literals

import re

import django
from django.contrib.auth import HASH_SESSION_KEY, get_user_model
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, override_settings

from allauth.socialaccount.models import SocialAccount

import six
from allauth_cas.test.testcases import CASTestCase
from fakeldap import MockLDAP
from mock import patch

from allauth_ens.utils import get_ldap_infos

from .adapter import deprecate_clippers, install_longterm_adapter

_mock_ldap = MockLDAP()
ldap_patcher = patch('allauth_ens.utils.ldap.initialize',
                     lambda x: _mock_ldap)

if django.VERSION >= (1, 10):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

User = get_user_model()


def prevent_logout_pwd_change(client, user):
    """
    Updating a user's password logs out all sessions for the user.
    By calling this function this behavior will be prevented.

    See this link, and the source code of `update_session_auth_hash`:
    https://docs.djangoproject.com/en/dev/topics/auth/default/#session-invalidation-on-password-change
    """
    if hasattr(user, 'get_session_auth_hash'):
        session = client.session
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()


class ViewsTests(TestCase):
    """
    Checks (barely) that templates do not contain errors.
    """
    def setUp(self):
        self.u = User.objects.create_user('user', 'user@mail.net', 'user')

        Site.objects.filter(pk=1).update(domain='testserver')

    def _login(self, client=None):
        if client is None:
            client = self.client
        client.login(username='user', password='user')

    def _get_confirm_email_link(self, email_msg):
        m = re.search(
            r'http://testserver(/accounts/confirm-email/.*/)',
            email_msg.body,
        )
        return m.group(1)

    def _get_reset_password_link(self, email_msg):
        m = re.search(
            r'http://testserver(/accounts/password/reset/key/.*/)',
            email_msg.body,
        )
        return m.group(1)

    def test_account_signup(self):
        r = self.client.get(reverse('account_signup'))
        self.assertEqual(r.status_code, 200)

    @override_settings(
        ACCOUNT_ADAPTER='tests.adapter.ClosedSignupAccountAdapter',
    )
    def test_account_closed_signup(self):
        r = self.client.get(reverse('account_signup'))
        self.assertEqual(r.status_code, 200)

    def test_account_login(self):
        r = self.client.get(reverse('account_login'))
        self.assertEqual(r.status_code, 200)

    def test_account_logout(self):
        self._login()
        r = self.client.get(reverse('account_logout'))
        self.assertEqual(r.status_code, 200)

    def test_account_change_password(self):
        self._login()
        r = self.client.get(reverse('account_change_password'))
        self.assertEqual(r.status_code, 200)

    def test_account_set_password(self):
        self._login()
        self.u.set_unusable_password()
        self.u.save()
        prevent_logout_pwd_change(self.client, self.u)

        r = self.client.get(reverse('account_set_password'))
        self.assertEqual(r.status_code, 200)

    def test_account_inactive(self):
        r = self.client.get(reverse('account_inactive'))
        self.assertEqual(r.status_code, 200)

    def test_account_email(self):
        self._login()
        r = self.client.get(reverse('account_email'))
        self.assertEqual(r.status_code, 200)

    def test_account_email_verification_sent(self):
        self._login()
        r = self.client.get(reverse('account_email_verification_sent'))
        self.assertEqual(r.status_code, 200)

    def test_account_confirm_email(self):
        self._login()
        self.client.post(reverse('account_email'), {
            'action_add': '',
            'email': 'test@mail.net',
        })
        confirm_url = self._get_confirm_email_link(mail.outbox[0])

        r = self.client.get(confirm_url)
        self.assertEqual(r.status_code, 200)

    def test_account_reset_password(self):
        r = self.client.get(reverse('account_reset_password'))
        self.assertEqual(r.status_code, 200)

    def test_account_reset_password_done(self):
        r = self.client.get(reverse('account_reset_password_done'))
        self.assertEqual(r.status_code, 200)

    def test_account_reset_password_from_key(self):
        self.client.post(reverse('account_reset_password'), {
            'email': 'user@mail.net',
        })
        reset_url = self._get_reset_password_link(mail.outbox[0])

        r = self.client.get(reset_url, follow=True)
        self.assertEqual(r.status_code, 200)

    def test_account_reset_password_from_key_done(self):
        r = self.client.get(reverse('account_reset_password_from_key_done'))
        self.assertEqual(r.status_code, 200)


@override_settings(
    SOCIALACCOUNT_ADAPTER='allauth_ens.adapter.LongTermClipperAccountAdapter'
)
class LongTermClipperTests(CASTestCase):
    def setUp(self):
        ldap_patcher.start()

    def tearDown(self):
        ldap_patcher.stop()
        _mock_ldap.reset()

    def _setup_ldap(self, promo=12, username="test"):
        try:
            buid = six.binary_type(username, 'utf-8')
            home = six.binary_type('/users/%d/phy/test/' % promo, 'utf-8')
        except TypeError:
            buid = six.binary_type(username)
            home = six.binary_type('/users/%d/phy/test/' % promo)
        _mock_ldap.directory['dc=spi,dc=ens,dc=fr'] = {
            'uid': [buid],
            'cn': [b'John Smith'],
            'mailRoutingAddress': [b'test@clipper.ens.fr'],
            'homeDirectory': [home],
        }

    def _count_ldap_queries(self):
        queries = _mock_ldap.ldap_methods_called()
        count = len([op for op in queries if op != 'set_option'])
        return count

    def test_new_connexion(self):
        self._setup_ldap()

        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username="test")
        u = r.context['user']

        self.assertEqual(u.username, "test@12")
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Smith")
        self.assertEqual(u.email, "test@clipper.ens.fr")
        self.assertEqual(self._count_ldap_queries(), 1)

        sa = list(SocialAccount.objects.all())[-1]
        self.assertEqual(sa.user.id, u.id)
        self.assertEqual(sa.extra_data['ldap']['entrance_year'], '12')

    def test_connect_disconnect(self):
        self._setup_ldap()
        r0 = self.client_cas_login(self.client, provider_id="clipper",
                                   username="test")
        self.assertIn("_auth_user_id", self.client.session)
        self.assertIn('user', r0.context)

        self.client.logout()
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_second_connexion(self):
        self._setup_ldap()

        self.client_cas_login(self.client, provider_id="clipper",
                              username="test")
        self.client.logout()

        nu = User.objects.count()

        self.client_cas_login(self.client, provider_id="clipper",
                              username="test")
        self.assertEqual(User.objects.count(), nu)
        self.assertEqual(self._count_ldap_queries(), 1)

    def test_deprecation(self):
        self._setup_ldap()
        self.client_cas_login(self.client, provider_id="clipper",
                              username="test")
        deprecate_clippers()

        sa = SocialAccount.objects.all()[0]
        self.assertEqual(sa.provider, "clipper_inactive")

    def test_reconnect_after_deprecation(self):
        self._setup_ldap()
        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username="test")
        user0 = r.context['user']
        n_sa0 = SocialAccount.objects.count()
        n_u0 = User.objects.count()
        self.client.logout()

        deprecate_clippers()

        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username="test")
        user1 = r.context['user']
        sa1 = list(SocialAccount.objects.all())
        n_u1 = User.objects.count()
        self.assertEqual(len(sa1), n_sa0)
        self.assertEqual(n_u1, n_u0)
        self.assertEqual(user1.id, user0.id)
        self.assertEqual(self._count_ldap_queries(), 2)

    def test_override_inactive_account(self):
        self._setup_ldap(12)
        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username="test")
        user0 = r.context['user']
        n_sa0 = SocialAccount.objects.count()
        n_u0 = User.objects.count()
        self.client.logout()

        deprecate_clippers()

        self._setup_ldap(13)
        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username="test")

        user1 = r.context['user']
        sa1 = list(SocialAccount.objects.all())
        n_u1 = User.objects.count()
        self.assertEqual(len(sa1), n_sa0 + 1)
        self.assertEqual(n_u1, n_u0 + 1)
        self.assertNotEqual(user1.id, user0.id)

    def test_multiple_deprecation(self):
        self._setup_ldap(12)
        self.client_cas_login(self.client, provider_id="clipper",
                              username="test")
        self.client.logout()

        self._setup_ldap(15, "truc")
        self.client_cas_login(self.client, provider_id="clipper",
                              username="truc")
        self.client.logout()
        sa0 = SocialAccount.objects.count()

        deprecate_clippers()

        self._setup_ldap(13)
        self.client_cas_login(self.client, provider_id="clipper",
                              username="test")
        self.client.logout()

        sa1 = SocialAccount.objects.count()

        deprecate_clippers()
        sa2 = SocialAccount.objects.count()

        # Older "test" inactive SocialAccount gets erased by new one
        # while "truc" remains
        self.assertEqual(sa0, sa2)
        self.assertEqual(sa1, sa0 + 1)

    def test_longterm_installer_from_allauth(self):
        self._setup_ldap(12)
        with self.settings(
                SOCIALACCOUNT_ADAPTER='allauth.socialaccount.'
                'adapter.DefaultSocialAccountAdapter'):
            r = self.client_cas_login(self.client, provider_id="clipper",
                                      username='test')
            user0 = r.context["user"]
            nsa0 = SocialAccount.objects.count()
            self.assertEqual(user0.username, "test")
            self.client.logout()

        outputs = install_longterm_adapter()

        self.assertEqual(outputs["updated"], [("test", "test@12")])
        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username='test')
        user1 = r.context["user"]
        nsa1 = SocialAccount.objects.count()
        conn = user1.socialaccount_set.get(provider='clipper')
        self.assertEqual(user1.id, user0.id)
        self.assertEqual(nsa1, nsa0)
        self.assertEqual(user1.username, "test@12")
        self.assertEqual(conn.extra_data['ldap']['entrance_year'], '12')

    def test_longterm_installer_from_djangocas(self):
        with self.settings(
                SOCIALACCOUNT_ADAPTER='allauth.socialaccount.'
                'adapter.DefaultSocialAccountAdapter'):
            user0 = User.objects.create_user('test', 'test@clipper.ens.fr',
                                             'test')
            nsa0 = SocialAccount.objects.count()

        self._setup_ldap(12)

        outputs = install_longterm_adapter()

        self.assertEqual(outputs["created"], [("test", "test@12")])
        r = self.client_cas_login(self.client, provider_id="clipper",
                                  username='test')
        user1 = r.context["user"]
        nsa1 = SocialAccount.objects.count()
        conn = user1.socialaccount_set.get(provider='clipper')
        self.assertEqual(user1.id, user0.id)
        self.assertEqual(nsa1, nsa0 + 1)
        self.assertEqual(user1.username, "test@12")
        self.assertEqual(conn.extra_data['ldap']['entrance_year'], '12')

    def test_disconnect_ldap(self):
        nu0 = User.objects.count()
        nsa0 = SocialAccount.objects.count()

        ldap_patcher.stop()
        with self.settings(CLIPPER_LDAP_SERVER=''):
            self.assertRaises(ValueError, self.client_cas_login,
                              self.client, provider_id="clipper",
                              username="test")

        nu1 = User.objects.count()
        nsa1 = SocialAccount.objects.count()
        self.assertEqual(nu0, nu1)
        self.assertEqual(nsa0, nsa1)
        ldap_patcher.start()

    def test_invalid_uid(self):
        self._setup_ldap(12, "test")
        uids = [" test", "test ", "\\test", "test)"]
        for uid in uids:
            with self.assertRaises(ValueError) as cm:
                get_ldap_infos(uid)
            self.assertIn(uid, str(cm.exception))
