import Live
from typing import List

from a_protocol_0.lom.device.Device import Device
from a_protocol_0.lom.device.DeviceType import DeviceType


class PluginDevice(Device):
    def __init__(self, *a, **k):
        super(PluginDevice, self).__init__(*a, **k)
        self._device = self._device  # type: Live.PluginDevice.PluginDevice
        self.device_type = DeviceType.PLUGIN_DEVICE

    @property
    def presets(self):
        # type: () -> List[str]
        return [preset for preset in list(self._device.presets) if not preset == "empty"]

    @property
    def selected_preset_index(self):
        # type: () -> int
        return self._device.selected_preset_index

    @selected_preset_index.setter
    def selected_preset_index(self, selected_preset_index):
        # type: (int) -> None
        self._device.selected_preset_index = selected_preset_index

    @property
    def selected_preset(self):
        # type: () -> str
        return self.presets[self.selected_preset_index]
