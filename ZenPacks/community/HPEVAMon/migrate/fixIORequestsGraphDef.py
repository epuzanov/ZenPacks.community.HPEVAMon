################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class fixIORequestsGraphDef( ZenPackMigration ):
    """
    fix IO Requests GraphDef from RRDTemplates
    """
    version = Version(1, 9, 73)

    def migrate(self, pack):

        hpevaTemplates =   ['HPEVADiskDrive',
                            'HPEVAHostFCPort',
                            'HPEVAStorageProcessorCard',
                            'HPEVAStorageVolume',
                            ]

        for template in pack.dmd.Devices.getAllRRDTemplates():
            if template.id not in hpevaTemplates: continue
            gd = getattr(template.graphDefs, 'IO Requests', None)
	    if not gd: continue
	    gp = getattr(gd.graphPoints, 'WriteIOs', None)
	    if not gp: continue
	    gp.rpn = ''

fixIORequestsGraphDef()
