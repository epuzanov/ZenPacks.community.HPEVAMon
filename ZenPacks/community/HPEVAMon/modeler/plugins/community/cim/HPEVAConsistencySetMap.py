################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAConsistencySetMap

HPEVAConsistencySetMap maps HPEVA_ConsistencySet class to
HPEVAConsistencySet class.

$Id: HPEVAConsistencySetMap.py,v 1.1 2012/06/22 00:06:20 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMCollectionMap \
    import CIMCollectionMap

class HPEVAConsistencySetMap(CIMCollectionMap):
    """Map HPEVA_ConsistencySet CIM class to CIM_Collection class"""

    modname = "ZenPacks.community.HPEVAMon.HPEVA_ConsistencySet"

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Collection":
                (
                    "SELECT * FROM HPEVA_ConsistencySet",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "id":"InstanceID",
                        "title":"ElementName",
                        "setStoragePool":"drmlogdiskgroupid",
                        "failSafe":"FailSafe",
                        "hostAccessMode":"HostAccessMode",
                        "participationType":"ParticipationType",
                        "remoteCellName":"RemoteCellName",
                        "suspendMode":"SuspendMode",
                        "writeMode":"WriteMode",
                        "_sysname":"InstanceID",
                    }
                ),
            "CIM_MemberOfCollection":
                (
                    "SELECT Member,Collection FROM CIM_MemberOfCollection",
                    None,
                    cs,
                    {
                        "member":"Member",
                        "collection":"Collection",
                    },
                ),
            }
