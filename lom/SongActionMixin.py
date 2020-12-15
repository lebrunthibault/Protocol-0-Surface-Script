from typing import TYPE_CHECKING, Optional

from a_protocol_0.consts import LogLevel
from a_protocol_0.lom.track.SimpleTrack import SimpleTrack
from a_protocol_0.utils.decorators import defer

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from a_protocol_0.lom.Song import Song


# noinspection PyTypeHints
class SongActionMixin(object):
    def select_track(self, selected_track):
        # type: (Song, SimpleTrack) -> None
        self._view.selected_track = selected_track._track

    def unfocus_all_tracks(self):
        # type: (Song) -> None
        [t.action_unarm() for t in self.tracks if t.arm if t != self.selected_track]
        [t.action_unarm() for t in self.external_synth_tracks if t.arm if t != self.current_track]
        [setattr(t, "solo", False) for t in self.song.tracks if t.solo if t != self.selected_track]

    @defer
    def reset(self):
        # type: (Song) -> None
        if self._song.current_song_time == 0 and not self._song.is_playing:
            return
        self.stop_all_clips(0)
        self.stop_playing()
        self._song.current_song_time = 0
        if LogLevel.INFO:
            [track.reset_track() for track in self.tracks]
            if len(self.tracks):
                self.song.select_track(self.tracks[0])

    def stop_playing(self):
        # type: (Song) -> None
        self._song.stop_playing()

    def stop_all_clips(self, quantized=1):
        # type: (Song, int) -> None
        self._song.stop_all_clips(quantized)

    def undo(self):
        # type: (Song) -> None
        self._song.undo()

    def create_scene(self, scene_index=None):
        # type: (Song, Optional[int]) -> None
        self.song._view.selected_scene = self._song.create_scene(scene_index or len(self.song.scenes))

    def show_hide_plugins(self):
        # type: (Song) -> None
        self.parent.ahkManager._sendKeys("^%p")

    def select_device(self, device):
        # type: (Song, Live.Device.Device) -> None
        self._view.select_device(device)

