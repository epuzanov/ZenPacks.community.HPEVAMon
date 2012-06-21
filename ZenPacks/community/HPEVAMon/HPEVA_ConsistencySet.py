################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVA_ConsistencySet

HPEVA_ConsistencySet is an abstraction of a HPEVA_ConsistencySet

$Id: HPEVA_ConsistencySet.py,v 1.4 2012/06/22 00:03:15 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.CIMMon.CIM_Collection import CIM_Collection
from Products.ZenRelations.RelSchema import ToOne, ToMany
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ZenossSecurity import *
from Products.ZenUtils.Utils import convToUnits

class HPEVA_ConsistencySet(CIM_Collection):
    """HPEVA_ConsistencySet object"""

    failSafe = ""
    hostAccessMode = ""
    participationType = ""
    remoteCellName = ""
    suspendMode = ""
    writeMode = ""

    _properties = CIM_Collection._properties + (
                 {'id':'failSafe', 'type':'string', 'mode':'w'},
                 {'id':'hostAccessMode', 'type':'string', 'mode':'w'},
                 {'id':'participationType', 'type':'string', 'mode':'w'},
                 {'id':'remoteCellName', 'type':'string', 'mode':'w'},
                 {'id':'suspendMode', 'type':'string', 'mode':'w'},
                 {'id':'writeMode', 'type':'string', 'mode':'w'},
                )

    _relations = CIM_Collection._relations + (
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.HPEVAMon.HPEVA_StoragePool",
            "collections")),
        )

    security = ClassSecurityInfo()

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the given
        id.
        """
        if not spid: return
        for sp in self.os().storagepools() or []:
            if sp.poolId != spid: continue
            self.storagepool.addRelation(sp)
            break

    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        return self.storagepool()

    security.declareProtected(ZEN_VIEW, 'getStoragePoolName')
    def getStoragePoolName(self):
        return getattr(self.getStoragePool(), 'name', lambda:'Unknown')()

    def getCurrentPercentLogLevel(self):
        return "%s%%"%self.cacheRRDValue('CurrentPercentLogLevel', 0)

    def getLogDiskReservedCapacity(self):
        return convToUnits(self.cacheRRDValue('LogDiskReservedCapacity', 0)*512)

InitializeClass(HPEVA_ConsistencySet)
