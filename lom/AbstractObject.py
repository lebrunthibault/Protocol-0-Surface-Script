from typing import TYPE_CHECKING, Any

from _Framework.ControlSurface import get_control_surfaces
from _Framework.SubjectSlot import SlotManager, Subject
from _Framework.Util import find_if

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from a_protocol_0.lom.Song import Song
    # noinspection PyUnresolvedReferences
    from a_protocol_0 import Protocol0


class AbstractObject(SlotManager, Subject):
    def __init__(self, *a, **k):
        """ we cannot use dependency injection here because objects are created not only at startup """
        from a_protocol_0 import Protocol0
        self._registered_disconnectables = []
        self._parent = find_if(lambda cs: isinstance(cs, Protocol0), get_control_surfaces())

    def __repr__(self):
        repr = "P0 %s" % self.__class__.__name__
        if hasattr(self, 'name'):
            repr = "%s: %s" % (repr, self.name)
        if hasattr(self, 'index'):
            repr = "%s (%s)" % (repr, self.index)
        if hasattr(self, '_device'):
            repr = "%s (%s)" % (repr, self._device)

        return repr

    def __ne__(self, obj):
        # type: (AbstractObject) -> bool
        return not obj or not self == obj

    def set_method_property(self, method, property, value):
        # type: (callable, str, Any) -> None
        method.__dict__[property][self] = value

    @property
    def parent(self):
        # type: () -> Protocol0
        return self._parent

    @property
    def song(self):
        # type: () -> Song
        return self._parent.protocol0_song
