from typing import Any, Optional, TYPE_CHECKING

from a_protocol_0.consts import GROUP_EXT_NAMES
from a_protocol_0.lom.AbstractObject import AbstractObject
from a_protocol_0.lom.SongActionMixin import SongActionMixin
from a_protocol_0.lom.track.AbstractTrack import AbstractTrack
from a_protocol_0.lom.track.GroupTrack import GroupTrack
from a_protocol_0.lom.track.SimpleTrack import SimpleTrack

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from a_protocol_0.Protocol0Component import Protocol0Component


class Song(SongActionMixin, AbstractObject):
    def __init__(self, *a, **k):
        super(Song, self).__init__(*a, **k)
        self.parent._my_song = self  # because we need access to the song object before instantiation step is over
        self._song = self.parent.song()
        self.view = self._song.view  # type: Any
        self.tracks = []
        self.build_tracks()
        for g_track in self.g_tracks:
            g_track.color = g_track.color  # when booting live, a track could be red without being armed

    def init_listeners(self):
        # type: () -> None
        self._song.add_tracks_listener(self.build_tracks)

    def build_tracks(self):
        self.tracks = [SimpleTrack(track=track, index=i) for i, track in
                       enumerate(list(self._song.tracks))]  # type: list[SimpleTrack]
        self.g_tracks = [GroupTrack(base_track=track) for track in self.tracks if track.name in GROUP_EXT_NAMES]
        self.parent.log("Song : built tracks")

    @property
    def selected_track(self):
        # type: () -> Optional[SimpleTrack]
        if not self.view.selected_track:
            return None

        return self.get_track(self.view.selected_track)

    @selected_track.setter
    def selected_track(self, selected_track):
        # type: (SimpleTrack) -> None
        self.view.selected_track = selected_track.track

    @property
    def current_track(self):
        # type: () -> Optional[AbstractTrack]
        return self.selected_track.abstract_track

    @property
    def tempo(self):
        # type: () -> float
        return self._song.tempo

    @property
    def metronome(self):
        # type: () -> float
        return self._song.metronome

    @metronome.setter
    def metronome(self, metronome):
        # type: (bool) -> None
        self._song.metronome = metronome

    def set_metronome(self, metronome):
        # type: (bool) -> None
        self._song.metronome = metronome

    @property
    def is_playing(self):
        # type: () -> float
        return self._song.is_playing

    @is_playing.setter
    def is_playing(self, is_playing):
        # type: (bool) -> None
        self._song.is_playing = is_playing

    @property
    def session_record_status(self):
        # type: () -> float
        return self._song.session_record_status

    @property
    def top_tracks(self):
        # type: () -> list[SimpleTrack]
        return [track for track in self.tracks if track.is_top_visible]

    @property
    def simple_tracks(self):
        # type: () -> list[SimpleTrack]
        return [track for track in self.tracks if not track.is_groupable]

    def simple_armed_tracks(self, track):
        # type: (AbstractTrack) -> list[SimpleTrack]
        return [t for t in self.simple_tracks if t.arm and t != track]

    @property
    def clip_trigger_quantization(self):
        # type: () -> int
        return self._song.clip_trigger_quantization

    @clip_trigger_quantization.setter
    def clip_trigger_quantization(self, clip_trigger_quantization):
        # type: (int) -> None
        self._song.clip_trigger_quantization = clip_trigger_quantization

    @property
    def scene_count(self):
        # type: () -> int
        return len(self._song.scenes)

    @property
    def playing_tracks(self):
        # type: () -> list[AbstractTrack]
        return [track for track in self.tracks if track.is_playing]

    def delay_before_recording_end(self, bar_count):
        # type: (int) -> int
        return round((600 / self._song.tempo) * (4 * int(bar_count) - 0.5))

    def get_track(self, track):
        # type: (Any) -> SimpleTrack
        if isinstance(track, AbstractTrack):
            raise Exception("Expected Live track, got AbstractTrack instead")

        for t in self.tracks:
            if t.track == track:
                return t

        raise Exception("this track cannot be matched")

    def other_armed_group_track(self, abstract_track=None):
        # type: (Optional[AbstractTrack]) -> Optional[GroupTrack]
        return next(iter([g_track for g_track in self.g_tracks if (
                not abstract_track or not isinstance(abstract_track,
                                                     GroupTrack) or abstract_track.index != g_track.index) and g_track.any_armed]),
                    None)
