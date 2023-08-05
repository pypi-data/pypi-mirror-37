# -*- coding: utf-8 -*-

from zope.interface import implements
from plone.app.workflow.interfaces import ISharingPageRole
from cciaa.intranetworkflow import config

from Products.CMFPlone import PloneMessageFactory as _

class DUffRole(object):
    implements(ISharingPageRole)
    
    title = _(u"title_duff", default=u"Può gestire contenuti")
    if config.CCIAA_ROLES_GLOBALLY_ASSIGNABLE:
        required_permission = config.DelegateRoles
    else:
        required_permission = config.DelegateEditorRole

class CUffRole(object):
    implements(ISharingPageRole)
    
    title = _(u"title_cuff", default=u"Può gestire l'ufficio")
    if config.CCIAA_ROLES_GLOBALLY_ASSIGNABLE:
        required_permission = config.DelegateRoles
    else:
        required_permission = config.DelegateCuffRole
    
class CSerRole(object):
    implements(ISharingPageRole)
    
    title = _(u"area_cser", default=u"Può gestire il servizio")
    if config.CCIAA_ROLES_GLOBALLY_ASSIGNABLE:
        required_permission = config.DelegateRoles
    else:
        required_permission = config.DelegateCSerRole

class SegGenRole(object):
    implements(ISharingPageRole)
    
    title = _(u"ufficio_seggen", default=u"Può dirigere l'Ente")
    if config.CCIAA_ROLES_GLOBALLY_ASSIGNABLE:
        required_permission = config.DelegateRoles
    else:
        required_permission = config.DelegateSegGenRole

