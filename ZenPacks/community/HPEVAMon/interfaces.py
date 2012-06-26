################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.6 2012/06/26 23:35:12 egor Exp $"""

__version__ = "$Revision: 1.6 $"[11:-2]

from ZenPacks.community.CIMMon.interfaces import IStoragePoolInfo,\
                                                IStorageVolumeInfo,\
                                                IReplicationGroupInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IHPEVAStoragePoolInfo(IStoragePoolInfo):
    """
    Info adapter for HPEVA Disk Groups components.
    """
    diskGroupType = schema.Text(title=u"Disk Group Type", group="Details")
    diskType = schema.Text(title=u"Disk Type", group="Details")
    protLevel = schema.Text(title=u"Protection Level", group="Details")

class IHPEVAStorageVolumeInfo(IStorageVolumeInfo):
    """
    Info adapter for HPEVA Storage Volume components.
    """
    preferredPath = schema.Text(title=u"Preferred Path", readonly=True,
                                                                group='Details')
    mirrorCache = schema.Text(title=u"Mirror Cache", readonly=True,
                                                                group='Details')
    readCachePolicy = schema.Text(title=u"Read Cache Policy", readonly=True,
                                                                group='Details')
    writeCachePolicy = schema.Text(title=u"Write Cache Policy", readonly=True,
                                                                group='Details')

class IHPEVAConsistencySetInfo(IReplicationGroupInfo):
    """
    Info adapter for HPEVA DR Group components.
    """
    participationType = schema.Text(title=u"Role",readonly=True,group='Details')
    writeMode = schema.Text(title=u"Write Mode", readonly=True, group='Details')
    storagePool = schema.Entity(title=u"Log Disk Group", readonly=True,
                                                                group='Details')
    logDiskReservedCapacity = schema.Text(title=u"Log Disk Reserved Capacity",
                                                readonly=True, group='Details')
    currentPercentLogLevel = schema.Text(title=u"Log Usage", readonly=True,
                                                                group='Details')
    remoteCellName = schema.Text(title=u"Remote System", readonly=True,
                                                                group='Details')
    hostAccessMode = schema.Text(title=u"Host Access Mode", readonly=True,
                                                                group='Details')
    failSafe = schema.Text(title=u"Failsafe", readonly=True, group='Details')
    suspendMode = schema.Text(title=u"Suspend Mode", readonly=True,
                                                                group='Details')
