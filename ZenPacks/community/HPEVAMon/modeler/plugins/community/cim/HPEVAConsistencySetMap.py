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

$Id: HPEVAConsistencySetMap.py,v 1.2 2012/06/26 23:37:06 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMReplicationGroupMap \
    import CIMReplicationGroupMap

class HPEVAConsistencySetMap(CIMReplicationGroupMap):
    """Map HPEVA_ConsistencySet CIM class to CIM_Collection class"""

    modname = "ZenPacks.community.HPEVAMon.HPEVA_ConsistencySet"

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_ReplicationGroup":
                (
                    "SELECT __PATH,drmlogdiskgroupid,ElementName,FailSafe,HostAccessMode,InstanceID,ParticipationType,RemoteCellName,SuspendMode,WriteMode FROM HPEVA_ConsistencySet",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "setStoragePool":"drmlogdiskgroupid",
                        "title":"ElementName",
                        "failSafe":"FailSafe",
                        "hostAccessMode":"HostAccessMode",
                        "_sysname":"InstanceID",
                        "id":"InstanceID",
                        "participationType":"ParticipationType",
                        "remoteCellName":"RemoteCellName",
                        "suspendMode":"SuspendMode",
                        "writeMode":"WriteMode",
                    }
                ),
            }
