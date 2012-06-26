################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageProcessorCardMap

HPEVAStorageProcessorCardMap maps HPEVA_StorageProcessorCard class to
CIM_Controller class.

$Id: HPEVAStorageProcessorCardMap.py,v 1.0 2012/06/26 23:06:24 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMControllerMap \
    import CIMControllerMap

class HPEVAMap(CIMControllerMap):
    """Map HPEVA_Controller CIM class to CIM_Controller class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Controller":
                (
                    "SELECT Description,Manufacturer,Model,SerialNumber,Tag,Version FROM HPEVA_StorageProcessorCard",
                    None,
                    cs,
                    {
                        "title":"Description",
                        "_manuf":"Manufacturer",
                        "setProductKey":"Model",
                        "serialNumber":"SerialNumber",
                        "_sysname":"Tag",
                        "tag":"Tag",
                        "FWRev":"Version",
                    },
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

    def _ignoreController(self, inst):
        return False

    def _getPackage(self, results, inst):
        return {
            'setPath':'HPEVA_StorageProcessorSystem.Name="%s"'%inst.get("tag"),
            }

    def _getStatPath(self, results, inst):
        return 'HPEVA_StorageSystemControllerStatisticalData.InstanceID="%s"'%(
            inst.get("tag"))
