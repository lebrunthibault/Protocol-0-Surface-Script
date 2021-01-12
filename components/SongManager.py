import collections
from plistlib import Dict
from typing import Optional, Any

from a_protocol_0.AbstractControlSurfaceComponent import AbstractControlSurfaceComponent
from a_protocol_0.lom.track.AbstractTrack import AbstractTrack
from a_protocol_0.lom.track.group_track.AbstractGroupTrack import AbstractGroupTrack
from a_protocol_0.lom.track.simple_track.SimpleTrack import SimpleTrack
from a_protocol_0.utils.decorators import subject_slot, has_callback_queue, retry


class SongManager(AbstractControlSurfaceComponent):
    __subject_events__ = ('selected_track', 'scene_list', 'added_track')

    def __init__(self, *a, **k):
        super(SongManager, self).__init__(*a, **k)
        self._live_track_to_simple_track = collections.OrderedDict()  # type: Dict[Any, SimpleTrack]
        self._simple_track_to_abstract_group_track = collections.OrderedDict()  # type: Dict[SimpleTrack, AbstractGroupTrack]
        self._tracks_listener.subject = self.song._song
        self.update_highlighted_clip_slot = True

    def init_song(self):
        self._tracks_listener()
        self._highlighted_clip_slot = self.song.highlighted_clip_slot
        self._highlighted_clip_slot_poller()
        self.song.reset()

    @has_callback_queue
    def on_selected_track_changed(self):
        self._set_current_track()
        self.parent.clyphxNavigationManager.show_track_view()
        # noinspection PyUnresolvedReferences
        self.notify_selected_track()

    def on_scene_list_changed(self):
        # noinspection PyUnresolvedReferences
        self.notify_scene_list()

    @subject_slot("tracks")
    def _tracks_listener(self):
        # type: () -> Optional[SimpleTrack]
        return "totototo"
        track_added = False
        if len(self.song.tracks) and len(self.song._song.tracks) > len(self.song.tracks):
            track_added = True

        # generate simple tracks
        self.song.tracks = []
        for i, track in enumerate(list(self.song._song.tracks)):
            simple_track = self.parent.trackManager.instantiate_simple_track(track=track, index=i)
            self._live_track_to_simple_track[track] = simple_track
            self.song.tracks.append(simple_track)

        # generate group tracks
        self.song.abstract_group_tracks = list(filter(None,
                                                      [self.parent.trackManager.instantiate_abstract_group_track(track)
                                                       for track in self.song.tracks]))
        self._simple_track_to_abstract_group_track = {}
        for abstract_group_track in self.song.abstract_group_tracks:  # type: AbstractGroupTrack
            for abstract_group_sub_track in abstract_group_track.all_tracks:
                self._simple_track_to_abstract_group_track.update({abstract_group_sub_track: abstract_group_track})

        self.song.abstract_tracks = list(set([self.get_current_track(track) for track in self.song.tracks]))
        self._set_current_track()
        if track_added:
            # noinspection PyUnresolvedReferences
            self.notify_added_track()
        self.parent.log_info("SongManager : mapped tracks")

    def _highlighted_clip_slot_poller(self):
        # type: () -> None
        if self.song.highlighted_clip_slot != self._highlighted_clip_slot:
            self._highlighted_clip_slot = self.song.highlighted_clip_slot
            if self.song.highlighted_clip_slot and self.song.highlighted_clip_slot.has_clip:
                # self.song.highlighted_clip_slot.track._clip_notes_listener.subject = self.song.highlighted_clip_slot.clip._clip
                self.parent.push2Manager.update_clip_grid_quantization()
        self.parent.defer(self._highlighted_clip_slot_poller)

    def _update_highlighted_clip_slot(self):
        """ auto_update highlighted clip slot to match the playable clip """
        if self.update_highlighted_clip_slot:
            track = self.song.selected_track
            if track and track.is_visible and track.playable_clip and self.song.highlighted_clip_slot == \
                    track.clip_slots[0]:
                self.song.highlighted_clip_slot = track.playable_clip.clip_slot
        self.update_highlighted_clip_slot = True

    def _get_simple_track(self, track, default=None):
        # type: (Any, Optional[SimpleTrack]) -> Optional[SimpleTrack]
        """ default is useful when the _ableton_track_to_simple_track is not built yet """
        if not track:
            return None
        if isinstance(track, AbstractTrack):
            raise Exception("Expected Live track, got AbstractTrack instead")

        if track == self.song._song.master_track or track in self.song._song.return_tracks:
            return default
        if track not in self._live_track_to_simple_track.keys():
            if default:
                return default
            raise Exception("_get_simple_track mismatch on %s" % track.name)

        return self._live_track_to_simple_track[track]

    @retry(2)
    def _set_current_track(self):
        self.song.selected_track = self._get_simple_track(self.song._view.selected_track) or self.song.tracks[0]
        self.song.current_track = self.get_current_track(self.song.selected_track)

    def get_current_track(self, track):
        # type: (SimpleTrack) -> AbstractTrack
        if track in self._simple_track_to_abstract_group_track:
            if not track.is_scrollable or self._simple_track_to_abstract_group_track[track].base_track == track:
                # click either on a sub_track forwarding to group or the group_track base track yields the group track
                return self._simple_track_to_abstract_group_track[track]

        return track
