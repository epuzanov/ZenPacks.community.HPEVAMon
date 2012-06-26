################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVARedundancySetMap

HPEVARedundancySetMap maps HPEVA_RedundancySet class to CIM_RedundancySet class.

$Id: HPEVARedundancySetMap.py,v 1.0 2012/06/13 20:43:13 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMRedundancySetMap \
    import CIMRedundancySetMap

class HPEVARedundancySetMap(CIMRedundancySetMap):
    """Map HPEVA_RedundancySet class to CIM_RedundancySet class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_RedundancySet":
                (
                    "SELECT __PATH,ElementName,InstanceID,LoadBalanceAlgorithm,MinNumberNeeded,OtherLoadBalanceAlgorithm,OtherTypeOfSet,TypeOfSet FROM HPEVA_RedundancySet",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "title":"ElementName",
                        "_sysname":"InstanceID",
                        "id":"InstanceID",
                        "loadBalanceAlgorithm":"LoadBalanceAlgorithm",
                        "minNumberNeeded":"MinNumberNeeded",
                        "_loadBalanceAlgorithm":"OtherLoadBalanceAlgorithm",
                        "_typeOfSet":"OtherTypeOfSet",
                        "typeOfSet":"TypeOfSet",
                    },
                ),
            }
