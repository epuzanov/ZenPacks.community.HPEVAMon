################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of HPEVA components.

$Id: info.py,v 1.5 2012/06/22 00:01:01 egor Exp $"""

__version__ = "$Revision: 1.5 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.decorators import info
from Products.ZenUtils.Utils import convToUnits
from ZenPacks.community.CIMMon.info import  StoragePoolInfo,\
                                            StorageVolumeInfo,\
                                            CollectionInfo
from ZenPacks.community.HPEVAMon import interfaces


class HPEVA_StoragePoolInfo(StoragePoolInfo):
    implements(interfaces.IHPEVAStoragePoolInfo)

    diskGroupType = ProxyProperty("diskGroupType")
    diskType = ProxyProperty("diskType")
    protLevel = ProxyProperty("protLevel")

class HPEVA_StorageVolumeInfo(StorageVolumeInfo):
    implements(interfaces.IHPEVAStorageVolumeInfo)

    preferredPath = ProxyProperty("preferredPath")
    mirrorCache = ProxyProperty("mirrorCache")
    readCachePolicy = ProxyProperty("readCachePolicy")
    writeCachePolicy = ProxyProperty("writeCachePolicy")

class HPEVA_ConsistencySetInfo(CollectionInfo):
    implements(interfaces.IHPEVAConsistencySetInfo)

    participationType = ProxyProperty("participationType")
    writeMode = ProxyProperty("writeMode")
    remoteCellName = ProxyProperty("remoteCellName")
    hostAccessMode = ProxyProperty("hostAccessMode")
    failSafe = ProxyProperty("failSafe")
    suspendMode = ProxyProperty("suspendMode")

    @property
    @info
    def storagePool(self):
        return self._object.getStoragePool()

    @property
    def currentPercentLogLevel(self):
        return self._object.getCurrentPercentLogLevel()

    @property
    def logDiskReservedCapacity(self):
        return self._object.getLogDiskReservedCapacity()

