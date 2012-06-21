################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAComputerSystemMap

HPEVAComputerSystemMap maps HPEVA_ComputerSystem class to CIM_ComputerSystem class.

$Id: HPEVAComputerSystemMap.py,v 1.0 2012/06/21 23:47:24 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMComputerSystemMap \
    import CIMComputerSystemMap

class HPEVAComputerSystemMap(CIMComputerSystemMap):
    """Map HPEVA_ComputerSystem CIM class to CIM_ComputerSystem class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_ComputerSystem":
                (
                    "SELECT * FROM CIM_ComputerSystem",
                    None,
                    cs,
                    {
                        "setPath":"__PATH",
                        "_descr":"Description",
                        "_contact":"PrimaryOwnerContact",
                        "_sysname":"Name",
                        "FWRev":"FirmwareVersion",
                        "title":"ElementName",
                    },
                ),
            "CIM_SystemComponent":
                (
                    "SELECT GroupComponent,PartComponent FROM HPEVA_ComponentCS",
                    None,
                    cs,
                    {
                        "gc":"GroupComponent", # System
                        "pc":"PartComponent", # SystemComponent
                    },
                ),
            "CIM_ComputerSystemPackage":
                (
                    "SELECT Antecedent,Dependent FROM HPEVA_ComputerSystemPackage",
                    None,
                    cs,
                    {
                        "ant":"Antecedent", # Controller
                        "dep":"Dependent", # ComputerSystem
                    },
                ),
            "CIM_PhysicalPackage":
                (
                    "SELECT * FROM HPEVA_PhysicalPackage",
                    None,
                    cs,
                    {
                        "_path":"__PATH",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                    },
                ),
            }

    def _getStatPath(self, results, inst):
        return 'HPEVA_StorageSystemControllerStatisticalData.InstanceID="%s"'%(
            inst.get("_sysname"))
