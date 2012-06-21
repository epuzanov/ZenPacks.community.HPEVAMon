
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Acquisition import aq_base
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass


class ZenPack(ZenPackBase):
    """ HPEVAMon loader
    """

    dcProperties = {
        '/Storage/SMI-S/HP/EVA': {
            'description': ('', 'string'),
            'zWmiMonitorIgnore': (False, 'boolean'),
            'zSnmpMonitorIgnore': (True, 'boolean'),
        },
        '/Storage/SMI-S/HP/EVA': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.cim.HPEVAComputerSystemMap',
                'community.cim.HPEVAStorageDiskEnclosureMap',
                'community.cim.HPEVAStoragePoolMap',
                'community.cim.HPEVAConsistencySetMap',
                'community.cim.HPEVAStorageVolumeMap',
                'community.cim.HPEVADiskDriveMap',
                'community.cim.HPEVANetworkPortMap',
                ),
                'lines',
            ),
            'zCIMConnectionString': ("'pywbemdb',scheme='https',host='${here/manageIp}',port=5989,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/eva'", 'string'),
            'zCIMHWConnectionString': ("'pywbemdb',scheme='https',host='${here/manageIp}',port=5989,user='${here/zWinUser}',password='${here/zWinPassword}',namespace='root/eva'", 'string'),
        },
    }

    def addDeviceClass(self, app, dcp, properties):
        try:
            dc = app.zport.dmd.Devices.getOrganizer(dcp)
            if dc.getOrganizerName() != dcp:
                raise KeyError
        except KeyError:
            dcp, newdcp = dcp.rsplit('/', 1)
            dc = self.addDeviceClass(app, dcp, self.dcProperties.get(dcp, {}))
            manage_addDeviceClass(dc, newdcp)
            dc = app.zport.dmd.Devices.getOrganizer("%s/%s"%(dcp, newdcp))
            dc.description = ''
        for prop, value in properties.iteritems():
            if not hasattr(aq_base(dc), prop):
                dc._setProperty(prop, value[0], type = value[1])
        return dc

    def install(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        for dcp in self.dcProperties.keys():
            try:
                dc = app.zport.dmd.Devices.getOrganizer(dcp)
                dc._delProperty('zCollectorPlugins')
            except: continue
        ZenPackBase.remove(self, app, leaveObjects)
