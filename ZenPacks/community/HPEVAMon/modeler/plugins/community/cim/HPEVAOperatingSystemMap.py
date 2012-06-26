################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAOperatingSystemMap

HPEVAOperatingSystemMap maps HPEVA_HSVStorageProduct class to
CIM_OperatingSystem class.

$Id: HPEVAOperatingSystemMap.py,v 1.0 2012/06/22 18:50:21 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.CIMMon.modeler.plugins.community.cim.CIMOperatingSystemMap \
    import CIMOperatingSystemMap

class HPEVAOperatingSystemMap(CIMOperatingSystemMap):
    """Map HPEVA_HSVStorageProduct CIM class to CIM_OperatingSystem class"""

    def queries(self, device):
        connectionString = getattr(device, 'zCIMConnectionString', '')
        if not connectionString:
            return {}
        cs = self.prepareCS(device, connectionString)
        return {
            "CIM_OperatingSystem":
                (
                    "SELECT ElementName,IdentifyingNumber,SKUNumber,Version FROM HPEVA_HSVStorageProduct",
                    None,
                    cs,
                    {
                        "_sysname":"IdentifyingNumber",
                        "setOSProductKey":"ElementName",
                        "_version":"Version",
                    }
                ),
            }
