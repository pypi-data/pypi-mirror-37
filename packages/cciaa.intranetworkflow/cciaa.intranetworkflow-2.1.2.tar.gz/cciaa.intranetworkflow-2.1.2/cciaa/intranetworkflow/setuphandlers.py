# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'rer.cookieswitcher:uninstall',
            'rer.cookieswitcher:plonegazette',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    createUsers()
    plonegazette()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def createUsers():
    """Crea gli utnenti di test de portale"""
    portal = api.portal.get()
    acl_users = getToolByName(portal, 'acl_users')
    users = (
        ('cc_normal', 'cc_normal', ('Member',),
         {'fullname': 'Utente test comune'}),
        ('cc_editor', 'cc_editor', ('Member', 'Editor'),
         {'fullname': 'Utente test Editor'}),
        ('cc_contributor', 'cc_contributor', ('Member', 'Contributor'),
         {'fullname': 'Utente test Contributor'}),
        ('cc_cuff', 'cc_cuff', ('Member', 'CUff'),
         {'fullname': 'Utente test CUff'}),
        ('cc_cser', 'cc_cser', ('Member', 'CSer'),
         {'fullname': 'Utente test CSer'}),
        ('cc_seggen', 'cc_seggen', ('Member', 'SegGen'),
         {'fullname': 'Utente test SegGen'}),
        ('cc_reader', 'cc_reader', ('Member', 'Reader'),
         {'fullname': 'Utente test Reader'}),
    )
    for e in users:
        kwargs = e[3]
        kwargs['email'] = e[0]+"@redturtle.it"
        acl_users.userFolderAddUser(
            login=e[0], password=e[1], roles=e[2], domains=(), groups=(),)
        acl_users.getUserById(e[0]).setProperties(**kwargs)


def plonegazette():
    """
    if plonegazette is in the buildout, run specified steps
    """
    quickinstaller = api.portal.get_tool('portal_quickinstaller')
    if 'Products.PloneGazette' in quickinstaller.listInstallableProfiles():
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runAllImportStepsFromProfile(
            'profile-cciaa.intranetworkflow:plonegazette'
        )
