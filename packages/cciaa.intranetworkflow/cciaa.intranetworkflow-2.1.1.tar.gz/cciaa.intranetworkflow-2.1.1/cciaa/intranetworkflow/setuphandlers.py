# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


def setupVarious(context):
    portal = context.getSite()
    
    if context.readDataFile('cciaa.intranetworkflow_various.txt') is None: 
        return
    
    createUsers(context, portal)


def createUsers(context,portal):
    """Crea gli utnenti di test de portale"""
    acl_users = getToolByName(portal,'acl_users')
    users = (
             ('cc_normal','cc_normal',('Member',), {'fullname':'Utente test comune'}),
             ('cc_editor','cc_editor',('Member','Editor'),{'fullname':'Utente test Editor'}),
             ('cc_contributor','cc_contributor',('Member','Contributor'), {'fullname':'Utente test Contributor'}),
             ('cc_cuff','cc_cuff',('Member','CUff'), {'fullname':'Utente test CUff'}),
             ('cc_cser','cc_cser',('Member','CSer'), {'fullname': 'Utente test CSer'}),
             ('cc_seggen','cc_seggen',('Member','SegGen'), {'fullname': 'Utente test SegGen'}),
             ('cc_reader','cc_reader',('Member','Reader'), {'fullname': 'Utente test Reader'}),
            )
    for e in users:
        kwargs = e[3]
        kwargs['email'] = e[0]+"@redturtle.it"
        acl_users.userFolderAddUser(login= e[0], password=e[1],roles=e[2],domains=(), groups=(),)
        acl_users.getUserById(e[0]).setProperties(**kwargs)
