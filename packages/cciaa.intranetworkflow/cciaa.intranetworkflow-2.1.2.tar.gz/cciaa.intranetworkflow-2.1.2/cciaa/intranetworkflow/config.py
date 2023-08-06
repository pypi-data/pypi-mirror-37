# -*- coding: utf-8 -*-

from Products.CMFCore.permissions import setDefaultRoles
from AccessControl import ModuleSecurityInfo

security = ModuleSecurityInfo("cciaa.intranetworkflow.config")

PROJECTNAME = 'cciaa.intranetworkflow'

REVIEW_LEV1 = 'CamCom: Approvazione livello 1'
REVIEW_LEV2 = 'CamCom: Approvazione livello 2'

try:
    from customize import CCIAA_ROLES_GLOBALLY_ASSIGNABLE
except ImportError:
    CCIAA_ROLES_GLOBALLY_ASSIGNABLE = False

setDefaultRoles(REVIEW_LEV1, ('Manager',))
setDefaultRoles(REVIEW_LEV2, ('Manager',))

# Controls access to the "sharing" page
security.declarePublic("DelegateRoles")
DelegateRoles = "Sharing page: Delegate roles"
setDefaultRoles(DelegateRoles, ('Manager', 'Editor', 'Cuff', 'CSer', 'SegGen'))

# Control the individual roles
security.declarePublic("DelegateReaderRole")
DelegateReaderRole = "Sharing page: Delegate Reader role"
setDefaultRoles(DelegateReaderRole, ('Manager', 'Editor', 'Cuff', 'CSer', 'SegGen'))

security.declarePublic("DelegateContributorRole")
DelegateContributorRole = "Sharing page: Delegate Contributor role"
setDefaultRoles(DelegateContributorRole, ('Manager', 'Cuff', 'CSer', 'SegGen'))

security.declarePublic("DelegateEditorRole")
DelegateEditorRole = "Sharing page: Delegate Editor role"
setDefaultRoles(DelegateEditorRole, ('Manager', 'Cuff', 'CSer', 'SegGen'))

security.declarePublic("DelegateCuffRole")
DelegateCuffRole = "Sharing page: Delegate Cuff role"
setDefaultRoles(DelegateCuffRole, ('Manager', 'Cuff', 'CSer', 'SegGen',))

security.declarePublic("DelegateCSerRole")
DelegateCSerRole = "Sharing page: Delegate CSer role"
setDefaultRoles(DelegateCSerRole, ('Manager', 'CSer', 'SegGen',))

security.declarePublic("DelegateSegGenRole")
DelegateSegGenRole = "Sharing page: Delegate SegGen role"
setDefaultRoles(DelegateSegGenRole, ('Manager', 'SegGen',))
