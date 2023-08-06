# -*- coding: utf-8 -*-

from django.conf import settings

from allauth.account.models import EmailAddress
from allauth.account.utils import user_email

import ldap

DEPARTMENTS_LIST = {
    'phy': u'Physique',
    'maths': u'Maths',
    'bio': u'Biologie',
    'chimie': u'Chimie',
    'geol': u'Géosciences',
    'dec': u'DEC',
    'info': u'Informatique',
    'litt': u'Littéraire',
    'guests': u'Pensionnaires étrangers',
    'pei': u'PEI',
}


def init_ldap():
    server = getattr(settings, "CLIPPER_LDAP_SERVER",
                     "ldaps://ldap.spi.ens.fr:636")
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,
                    ldap.OPT_X_TLS_NEVER)
    ldap_connection = ldap.initialize(server)
    ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
    ldap_connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    ldap_connection.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
    ldap_connection.set_option(ldap.OPT_X_TLS_DEMAND, True)
    ldap_connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)
    ldap_connection.set_option(ldap.OPT_NETWORK_TIMEOUT, 10)
    ldap_connection.set_option(ldap.OPT_TIMEOUT, 10)
    return ldap_connection


def extract_infos_from_ldap(infos):
    data = {}

    # Name
    if 'cn' in infos:
        data['name'] = infos['cn'][0].decode("utf-8")

    # Parsing homeDirectory to get entrance year and departments
    if 'homeDirectory' in infos:
        dirs = infos['homeDirectory'][0].decode("utf-8").split('/')
        if len(dirs) >= 4 and dirs[1] == 'users':
            # Assume template "/users/<year>/<department>/clipper/"
            annee = dirs[2]
            dep = dirs[3]
            dep_fancy = DEPARTMENTS_LIST.get(dep.lower(), '')
            data['entrance_year'] = annee
            data['department_code'] = dep
            data['department'] = dep_fancy

    # Mail
    pmail = infos.get('mailRoutingAddress', [])
    if pmail:
        data['email'] = pmail[0].decode("utf-8")

    # User id
    if 'uid' in infos:
        data['clipper_uid'] = infos['uid'][0].decode("utf-8").strip().lower()

    return data


def get_ldap_infos(clipper_uid):
    if not clipper_uid.isalnum():
        raise ValueError(
            'Invalid uid "{}": contains non-alphanumeric characters'
            .format(clipper_uid)
        )
    data = {}
    try:
        ldap_connection = init_ldap()

        info = ldap_connection.search_s('dc=spi,dc=ens,dc=fr',
                                        ldap.SCOPE_SUBTREE,
                                        ('(uid=%s)' % (clipper_uid,)),
                                        ['cn',
                                         'mailRoutingAddress',
                                         'homeDirectory'])

        if len(info) > 0:
            data = extract_infos_from_ldap(info[0][1])

    except ldap.LDAPError:
        pass

    return data


def get_clipper_email(clipper):
    return '{}@clipper.ens.fr'.format(clipper.strip().lower())


def remove_email(user, email):
    """
    Removes an email address of a user.

    If it is his primary email address, it sets another email address as
    primary, preferably verified.
    """
    u_mailaddrs = user.emailaddress_set.filter(user=user)
    try:
        mailaddr = user.emailaddress_set.get(email=email)
    except EmailAddress.DoesNotExist:
        return

    if mailaddr.primary:
        others = u_mailaddrs.filter(primary=False)

        # Prefer a verified mail.
        new_primary = (
            others.filter(verified=True).last() or
            others.last()
        )

        if new_primary:
            # It also updates 'user.EMAIL_FIELD'.
            new_primary.set_as_primary()
        else:
            user_email(user, '')
            user.save()

    mailaddr.delete()
