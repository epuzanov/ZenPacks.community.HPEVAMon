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
CIM_ComputerSystem class.

$Id: HPEVAStorageProcessorCardMap.py,v 1.2 2012/10/17 18:23:57 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMControllerMap \
    import CIMControllerMap

class HPEVAStorageProcessorCardMap(CIMControllerMap):
    """Map HPEVA_StorageProcessorCard CIM class to CIM_ComputerSystem class"""

    modname = "ZenPacks.community.CIMMon.CIM_ComputerSystem"

    def queries(self, device):
        connectionString = getattr(device, 'zCIMHWConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_Controller":
                (
                    "SELECT Description,Manufacturer,Model,SerialNumber,Tag,Version,OperationalStatus FROM HPEVA_StorageProcessorCard",
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
                        "status":"OperationalStatus",
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

    def _getSlot(self, results, inst):
        try: return int(inst.get("title").rsplit(' ', 1)[-1])
        except: return 0

    def _getPackage(self, results, inst):
        return {
            'id':inst.get("tag"),
            'setPath':'HPEVA_StorageProcessorSystem.Name="%s  ",CreationClassName="HPEVA_StorageProcessorSystem"'%inst.get("tag"),
            }

    def _getStatPath(self, results, inst):
        return 'HPEVA_StorageSystemControllerStatisticalData.InstanceID="%s"'%(
            inst.get("tag"))
