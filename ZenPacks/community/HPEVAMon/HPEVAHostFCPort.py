################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAHostFCPort

HPEVAHostFCPort is an abstraction of a HPEVA_HostFCPort

$Id: HPEVAHostFCPort.py,v 1.5 2011/02/28 22:13:53 egor Exp $"""

__version__ = "$Revision: 1.5 $"[11:-2]

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from Products.ZenUtils.Utils import convToUnits

import logging
log = logging.getLogger("zen.HPEVAHostFCPort")

class HPEVAHostFCPort(HWComponent, HPEVAComponent):
    """HPHostFCPort object"""

    portal_type = meta_type = 'HPEVAFCPort'

    interfaceName = ""
    fc4Types = []
    fullDuplex = True
    linkTechnology = ""
    networkAddresses = []
    type = ""
    description = ""
    speed = 0
    mtu = 0
    wwn = ""
    state = "OK"

    _properties = HWComponent._properties + (
                 {'id':'interfaceName', 'type':'string', 'mode':'w'},
                 {'id':'fc4Types', 'type':'lines', 'mode':'w'},
                 {'id':'fullDuplex', 'type':'boolean', 'mode':'w'},
                 {'id':'linkTechnology', 'type':'string', 'mode':'w'},
                 {'id':'networkAddresses', 'type':'lines', 'mode':'w'},
                 {'id':'type', 'type':'string', 'mode':'w'},
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'speed', 'type':'int', 'mode':'w'},
                 {'id':'mtu', 'type':'int', 'mode':'w'},
                 {'id':'wwn', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )


    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                    "ZenPacks.community.HPEVAMon.HPEVADeviceHW",
                    "fcports")),
        ("controller", ToOne(ToMany,
                    "ZenPacks.community.HPEVAMon.HPEVAStorageProcessorCard",
                    "fcports")),
        )


    factory_type_information = (
        {
            'id'             : 'HostFCPort',
            'meta_type'      : 'HostFCPort',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HostFCPort_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHostFCPort',
            'immediate_view' : 'viewHPEVAHostFCPort',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAHostFCPort'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    security = ClassSecurityInfo()


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setController')
    def setController(self, cid):
        """
        Set the controller relationship to the Controller specified by the given
        id.
        """
        cntr = getattr(self.hw().cards, str(cid), None)
        if cntr: self.controller.addRelation(cntr)
        else: log.warn("controller id:%s not found", cid)


    security.declareProtected(ZEN_VIEW, 'getController')
    def getController(self):
        return self.controller()


    def speedString(self):
        """
        Return the speed in human readable form ie 10MB
        """
        return convToUnits(self.speed, divby=1024)


    def networkString(self):
        """
        Return the networks string
        """
        if self.networkAddresses: return '<br>'.join(self.networkAddresses)
        else: return 'Unknown'


    def wwnString(self):
        """
        Return the wwn string
        """
        return '-'.join([self.wwn[s*4:s*4+4] for s in range(4)])


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPEVAHostFCPort)
