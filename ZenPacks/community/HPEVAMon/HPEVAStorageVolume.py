################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageVolume

HPEVAStorageVolume is an abstraction of a HPEVA_StorageVolume

$Id: HPEVAStorageVolume.py,v 1.4 2011/02/28 20:50:30 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import HPEVAComponent

from AccessControl import ClassSecurityInfo
from Products.ZenUtils.Utils import convToUnits

from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.HPEVAStorageVolume")


def manage_addStorageVolume(context, id, userCreated, REQUEST=None):
    """make StorageVolume"""
    svid = prepId(id)
    sv = HPEVAStorageVolume(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class HPEVAStorageVolume(OSComponent, HPEVAComponent):
    """HPStorageVolume object"""

    portal_type = meta_type = 'HPEVAStorageVolume'

    accessType = ""
    caption = ""
    blockSize = 0
    mirrorCache = ""
    preferredPath = ""
    raidType = ""
    readCachePolicy = ""
    writeCachePolicy = ""
    diskType = ""
    state = "OK"

    _properties = OSComponent._properties + (
                 {'id':'accessType', 'type':'string', 'mode':'w'},
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'blockSize', 'type':'int', 'mode':'w'},
                 {'id':'mirrorCache', 'type':'string', 'mode':'w'},
                 {'id':'preferredPath', 'type':'string', 'mode':'w'},
                 {'id':'raidType', 'type':'string', 'mode':'w'},
                 {'id':'readCachePolicy', 'type':'string', 'mode':'w'},
                 {'id':'writeCachePolicy', 'type':'string', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "ZenPacks.community.HPEVAMon.HPEVADevice.HPEVADeviceOS",
            "virtualdisks")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.HPEVAMon.HPEVAStoragePool",
            "virtualdisks")),
        ("drgroup", ToOne(ToMany,
            "ZenPacks.community.HPEVAMon.HPEVAConsistencySet",
            "virtualdisks")),
        )

    factory_type_information = (
        {
            'id'             : 'StorageVolume',
            'meta_type'      : 'StorageVolume',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageVolume_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addStorageVolume',
            'immediate_view' : 'viewHPEVAStorageVolume',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAStorageVolume'
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


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the given
        id.
        """
        strpool = getattr(self.os().storagepools, str(spid), None)
        if strpool: self.storagepool.addRelation(strpool)
        else: log.warn("storage pool id:%s not found", spid)


    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        return self.storagepool()


    security.declareProtected(ZEN_VIEW, 'getStoragePoolName')
    def getStoragePoolName(self):
        return getattr(self.getStoragePool(), 'caption', 'Unknown')


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setDRGroup')
    def setDRGroup(self, drgid):
        """
        Set the drgroup relationship to the DR Group specified by the given id.
        """
        drgroup = getattr(self.os().drgroups, str(drgid), None)
        if drgroup: self.drgroup.addRelation(drgroup)
        else: log.warn("DR group id:%s not found", drgid)


    security.declareProtected(ZEN_VIEW, 'getDRGroup')
    def getDRGroup(self):
        return self.drgroup()


    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('NumberOfBlocks', 0) * self.blockSize


    def totalBytesString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.totalBytes(), divby=1024)


    def getRRDNames(self):
        """
        Return the datapoint name of this StorageVolume
        """
        return ['StorageVolume_NumberOfBlocks']


InitializeClass(HPEVAStorageVolume)
