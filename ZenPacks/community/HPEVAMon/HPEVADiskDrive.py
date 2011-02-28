################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVADiskDrive

HPEVADiskDrive is an abstraction of a harddisk.

$Id: HPEVADiskDrive.py,v 1.6 2011/02/28 20:47:31 egor Exp $"""

__version__ = "$Revision: 1.6 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import HPEVAComponent
from Products.ZenUtils.Utils import convToUnits

import logging
log = logging.getLogger("zen.HPEVADiskDrive")

addHardDisk = DTMLFile('dtml/addHardDisk', globals())

class HPEVADiskDrive(HWComponent, HPEVAComponent):
    """HPDiskDrive object"""

    portal_type = meta_type = 'HPEVADiskDrive'

    manage_editHardDiskForm = DTMLFile('dtml/manageEditHardDisk', globals())

    description = ""
    hostresindex = 0
    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""
    wwn = ""
    state = "OK"

    _properties = HWComponent._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'hostresindex', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'hotPlug', 'type':'boolean', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                 {'id':'wwn', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                            "ZenPacks.community.HPEVAMon.HPEVADeviceHW",
                            "harddisks")),
        ("enclosure", ToOne(ToMany,
                            "ZenPacks.community.HPEVAMon.HPEVAStorageDiskEnclosure",
                            "harddisks")),
        ("storagepool", ToOne(ToMany,
                            "ZenPacks.community.HPEVAMon.HPEVAStoragePool",
                            "harddisks")),
        )


    factory_type_information = ( 
        { 
            'id'             : 'DiskDrive',
            'meta_type'      : 'DiskDrive',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'DiskDrive_icon.gif',
            'product'        : 'HPEVAMon',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewHPEVADiskDrive',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVADiskDrive'
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

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setEnclosure')
    def setEnclosure(self, encid):
        """
        Set the enclosure relationship to the enclosure specified by the given
        id.
        """
        encl = getattr(self.hw().enclosures, str(encid), None)
        if encl: self.enclosure.addRelation(encl)
        else: log.warn("enclosure id:%s not found", encid)


    security.declareProtected(ZEN_VIEW, 'getEnclosure')
    def getEnclosure(self):
        """
        Return enclosure object
        """
        return self.enclosure()


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the
        given id.
        """
        spool=getattr(getattr(self.device().os,'storagepools',''),str(spid),'')
        if spool: self.storagepool.addRelation(spool)
        else: log.warn("storage pool id:%s not found", spid)


    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        """
        Return Disk Group object
        """
        return self.storagepool()


    def getEnclosureName(self):
        """
        Return enclosure id
        """
        return getattr(self.getEnclosure(), 'id', 'Unknown')


    def getStoragePoolName(self):
        """
        Return Disk Group name
        """
        return getattr(self.getStoragePool(), 'caption', 'Unknown')


    security.declareProtected(ZEN_VIEW, 'getManufacturerLink')
    def getManufacturerLink(self, target=None):
        """
        Return Manufacturer Link
        """
        if self.productClass():
            url = self.productClass().manufacturer.getPrimaryLink()
            if target: url = url.replace(">", " target='%s'>" % target, 1)
            return url
        return ""


    security.declareProtected(ZEN_VIEW, 'getProductLink')
    def getProductLink(self, target=None):
        """
        Return Product Link
        """
        url = self.productClass.getPrimaryLink()
        if target: url = url.replace(">", " target='%s'>" % target, 1)
        return url


    def diskImg(self):
        """
        Return disk image filename.
        """
        return '/zport/dmd/hpevadisk_%s_%s'%(
                self.diskType.startswith('online') and 'online' or 'nearonline',
                self.statusDot())


    def bayString(self):
        """
        Return enclosure and bay numbers
        """
        return '%s bay %02d'%(self.getEnclosureName(), int(self.bay))


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size, divby=1000)


    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        return 'Unknown'


    def wwnString(self):
        """
        Return the wwn string
        """
        return '-'.join([self.wwn[s*4:s*4+4] for s in range(4)])


    def hotPlugString(self):
        """
        Return the HotPlug Status
        """
        if self.hotPlug: return 'Hot Swappable'
        else: return 'Non-Hot Swappable'


    def viewName(self): return self.description


InitializeClass(HPEVADiskDrive)
