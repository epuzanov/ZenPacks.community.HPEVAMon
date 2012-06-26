################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVA_StoragePool

HPEVA_StoragePool is an abstraction of a HPEVA_StoragePool

$Id: HPEVA_StoragePool.py,v 1.8 2012/06/26 23:31:01 egor Exp $"""

__version__ = "$Revision: 1.8 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.CIMMon.CIM_StoragePool import CIM_StoragePool
from Products.ZenRelations.RelSchema import ToOne, ToMany

class HPEVA_StoragePool(CIM_StoragePool):
    """HPEVA_StoragePool object"""

    diskGroupType = ""
    diskType = ""
    protLevel = ""

    _properties = CIM_StoragePool._properties + (
                 {'id':'diskGroupType', 'type':'string', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'protLevel', 'type':'string', 'mode':'w'},
                )


    _relations = CIM_StoragePool._relations + (
        ("replicationgroups", ToMany(
            ToOne,
            "ZenPacks.community.HPEVAMon.HPEVA_ConsistencySet",
            "storagepool")),
        )

    def groupId(self):
        try: return int(self.poolId[:2])
        except: return 0

InitializeClass(HPEVA_StoragePool)
