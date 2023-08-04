# coding: utf-8
from enum import Enum

from qmaterialwidgets import MaterialIconBase, getIconColor, Theme


class Icon(MaterialIconBase, Enum):

    GRID = "Grid"
    MENU = "Menu"
    TEXT = "Text"
    MAIL = "Mail"
    PEOPLE = "People"
    VIDEOCAM = "Videocam"
    CHAT_BUBBLE = "ChatBubble"
    MAIL_OUTLINE = "MailOutline"
    PEOPLE_OUTLINE = "PeopleOutline"
    VIDEOCAM_OUTLINE = "VideocamOutline"
    CHAT_BUBBLE_OUTLINE = "ChatBubbleOutline"

    def path(self, theme=Theme.AUTO):
        return f":/gallery/images/icons/{self.value}_{getIconColor(theme)}.svg"
