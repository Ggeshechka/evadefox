from flet import *


class MyTextField(TextField):
    def __init__(self, label=None, hint_text=None, width=None, visible=None, suffix_icon=None, disabled=None,
                 on_change=None):
        super().__init__()

        self.height = 40
        self.width = width
        self.border_radius = 8
        self.visible = visible
        self.disabled = disabled

        self.label = label
        self.hint_text = hint_text
        self.suffix_icon = suffix_icon
        self.on_change = on_change
