import re
from typing import TYPE_CHECKING

from flet import *

from ui.components.button import MyButton
from ui.components.icon_button import MyIconButton
from ui.components.text_field import MyTextField

if TYPE_CHECKING:
    from main import App


class AuthorizationDialog(AlertDialog):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app

        self.modal = True
        self.content_padding = 8
        self.actions_padding = 0

        self.btn_send = MyIconButton(Icons.SEND, on_click=self.send_token)
        self.btn_continue = MyButton(self.app.get('login'), width=float('inf'), on_click=self.verify, disabled=True)

        self.field_email = MyTextField(
            self.app.get('email'),
            'user@example.com',
            width=float('inf'),
            on_change=self.validate_email
        )
        self.field_token = MyTextField(
            self.app.get('token'),
            '123456',
            width=float('inf'),
            suffix_icon=self.btn_send,
            disabled=True,
            on_change=self.validate_token
        )

        self.authorization = Column([
            Row([
                self.app.set.popup_menu_lang,
                MyIconButton(Icons.CLOSE, on_click=self.handle_close)
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            self.field_email,
            self.field_token,
            self.btn_continue,
        ],
            height=184,
            width=300
        )

        self.content = Container(
            ProgressRing(
                height=50,
                width=50
            ),
            height=184,
            width=300,
            alignment=Alignment.CENTER
        )

        self.app.page.run_task(self.loading)

    async def loading(self):
        await self.app.set.init()

        if await self.app.auth.init():
            self.app.page.pop_dialog()
        else:
            self.content = self.authorization
            self.app.page.update()

    async def send_token(self):
        if await self.app.auth.send_token(self.field_email.value):
            self.btn_send.disabled = True
            self.field_email.disabled = True

    async def verify(self):
        if await self.app.auth.verify(self.field_email.value, self.field_token.value):
            self.app.page.pop_dialog()

    async def validate_email(self, e):
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        self.field_token.disabled = not re.match(pattern, e.control.value) is not None

    async def validate_token(self, e):
        validate = not len(e.control.value) == 6

        self.btn_continue.disabled = validate

    async def handle_close(self):
        await self.app.page.window.close()
