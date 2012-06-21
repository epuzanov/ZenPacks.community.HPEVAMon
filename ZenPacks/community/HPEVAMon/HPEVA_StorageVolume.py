################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVA_StorageVolume

HPEVA_StorageVolume is an abstraction of a HPEVA_StorageVolume

$Id: HPEVA_StorageVolume.py,v 1.5 2012/06/22 00:04:39 egor Exp $"""

__version__ = "$Revision: 1.5 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.CIMMon.CIM_StorageVolume import CIM_StorageVolume
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ZenossSecurity import *

class HPEVA_StorageVolume(CIM_StorageVolume):
    """HPEVA_StorageVolume object"""

    mirrorCache = ""
    preferredPath = ""
    readCachePolicy = ""
    writeCachePolicy = ""

    _properties = CIM_StorageVolume._properties + (
                 {'id':'mirrorCache', 'type':'string', 'mode':'w'},
                 {'id':'preferredPath', 'type':'string', 'mode':'w'},
                 {'id':'readCachePolicy', 'type':'string', 'mode':'w'},
                 {'id':'writeCachePolicy', 'type':'string', 'mode':'w'},
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

InitializeClass(HPEVA_StorageVolume)
