import Live
from typing import TYPE_CHECKING, List

from _Framework.SubjectSlot import subject_slot
from _Framework.Util import find_if
from a_protocol_0.lom.AbstractObject import AbstractObject
from a_protocol_0.lom.device.DeviceParameter import DeviceParameter
from a_protocol_0.lom.device.DeviceType import DeviceType

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from a_protocol_0.lom.track.simple_track.SimpleTrack import SimpleTrack


class Device(AbstractObject):
    def __init__(self, device, track, index, *a, **k):
        # type: (Live.Device.Device, SimpleTrack, int) -> None
        super(Device, self).__init__(*a, **k)
        self._device = device
        self.track = track
        self.index = index
        self._view = self._device.view  # type: Live.Device.Device.View
        self.parameters = []  # type: (List[DeviceParameter])
        self._parameters_listener.subject = self._device
        self._parameters_listener()
        self.is_simpler = isinstance(device, Live.SimplerDevice.SimplerDevice)
        self.is_plugin = isinstance(device, Live.PluginDevice.PluginDevice)
        self.can_have_drum_pads = self._device.can_have_drum_pads
        self.can_have_chains = self._device.can_have_chains
        self.device_type = DeviceType.ABLETON_DEVICE

    def __eq__(self, device):
        # type: (Device) -> bool
        return device and self._device == device._device

    @staticmethod
    def make(device, track, index):
        # type: (Live.Device.Device, SimpleTrack, int) -> Device
        from a_protocol_0.lom.device.RackDevice import RackDevice
        from a_protocol_0.lom.device.PluginDevice import PluginDevice
        if isinstance(device, Live.RackDevice.RackDevice):
            return RackDevice(device=device, track=track, index=index)
        elif isinstance(device, Live.PluginDevice.PluginDevice):
            return PluginDevice(device=device, track=track, index=index)
        else:
            return Device(device=device, track=track, index=index)

    @property
    def name(self):
        return self._device.name

    @property
    def is_active(self):
        return self._device.is_active

    @property
    def is_collapsed(self):
        return self._view.is_collapsed

    @is_collapsed.setter
    def is_collapsed(self, is_collapsed):
        self._view.is_collapsed = is_collapsed

    @subject_slot("parameters")
    def _parameters_listener(self):
        self.parameters = [DeviceParameter(self, parameter) for parameter in self._device.parameters]

    def get_parameter(self, device_parameter):
        # type: (Live.DeviceParameter.DeviceParameter) -> DeviceParameter
        return find_if(lambda p: p.name == device_parameter.name, self.parameters)

    def disconnect(self):
        super(Device, self).disconnect()
        [parameter.disconnect() for parameter in self.parameters]
