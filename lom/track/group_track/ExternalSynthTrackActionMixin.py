from functools import partial

import Live
from typing import TYPE_CHECKING

from a_protocol_0.devices.InstrumentMinitaur import InstrumentMinitaur
from a_protocol_0.lom.Colors import Colors
from a_protocol_0.lom.clip_slot.ClipSlot import ClipSlot
from a_protocol_0.sequence.Sequence import Sequence

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    from a_protocol_0.lom.track.group_track.ExternalSynthTrack import ExternalSynthTrack


# noinspection PyTypeHints
class ExternalSynthTrackActionMixin(object):
    def action_arm_track(self):
        # type: (ExternalSynthTrack) -> None
        self.color = Colors.ARM
        self.base_track.is_folded = False
        self.midi_track.has_monitor_in = False
        self.audio_track.has_monitor_in = True
        seq = Sequence(silent=True)
        seq.add([
            self.midi_track.action_arm_track,
            self.audio_track.action_arm_track
        ])
        return seq.done()

    def action_unarm_track(self):
        # type: (ExternalSynthTrack) -> None
        self.midi_track.has_monitor_in = self.audio_track.has_monitor_in = False
        if isinstance(self.instrument, InstrumentMinitaur):
            self.midi_track.has_monitor_in = True  # needed when we have multiple minitaur tracks so that other midi clips are not sent to minitaur

    def action_switch_monitoring(self):
        # type: (ExternalSynthTrack) -> None
        if self.midi_track.has_monitor_in and self.audio_track.has_monitor_in:
            self.midi_track.has_monitor_in = self.audio_track.has_monitor_in = False
        elif self.audio_track.has_monitor_in:
            self.midi_track.has_monitor_in = True
        else:
            self.audio_track.has_monitor_in = True

    def action_record_all(self):
        # type: (ExternalSynthTrack) -> None
        """ next_empty_clip_slot_index is guaranteed to be not None """
        seq = Sequence()
        midi_clip_slot = self.midi_track.clip_slots[self.next_empty_clip_slot_index]
        audio_clip_slot = self.audio_track.clip_slots[self.next_empty_clip_slot_index]
        self.audio_track.select()
        seq.add([midi_clip_slot.record, audio_clip_slot.record])
        seq.add(self._post_record)
        return seq.done()

    def action_record_audio_only(self):
        # type: (ExternalSynthTrack, bool) -> Sequence
        midi_clip = self.midi_track.playable_clip or (self.song.highlighted_clip if self.midi_track.is_selected else None)
        if not midi_clip:
            self.parent.show_message("No midi clip selected")
            return

        self.song.metronome = False

        seq = Sequence()
        self.song.recording_bar_count = int(round((self.midi_track.playable_clip.length + 1) / 4))
        audio_clip_slot = self.audio_track.clip_slots[midi_clip.index]
        if audio_clip_slot.clip:
            seq.add(audio_clip_slot.clip.delete, wait=1)
        seq.add(partial(setattr, midi_clip, "start_marker", 0))
        seq.add(partial(self.parent._wait, 5, midi_clip.play))  # launching the midi clip after the record has started
        seq.add(self.audio_track.clip_slots[midi_clip.index].record)
        seq.add(self._post_record)
        return seq.done()

    def action_undo_track(self):
        # type: (ExternalSynthTrack) -> None
        [sub_track.action_undo_track() for sub_track in self.sub_tracks]

    def _post_record(self):
        # type: (ExternalSynthTrack, bool) -> None
        self.song.metronome = False
        self.midi_track.has_monitor_in = self.audio_track.has_monitor_in = False
        self.audio_track.playable_clip.warp_mode = Live.Clip.WarpMode.complex_pro
