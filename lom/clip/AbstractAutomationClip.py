from a_protocol_0.lom.clip.AutomationClipName import AutomationClipName
from a_protocol_0.lom.clip.Clip import Clip


class AbstractAutomationClip(Clip):
    def __init__(self, *a, **k):
        super(AbstractAutomationClip, self).__init__(*a, **k)
        self.clip_name = AutomationClipName(self)

    @property
    def automation_ramp_up(self):
        return self.clip_name._automation_ramp_up

    @property
    def automation_ramp_down(self):
        return self.clip_name._automation_ramp_down
