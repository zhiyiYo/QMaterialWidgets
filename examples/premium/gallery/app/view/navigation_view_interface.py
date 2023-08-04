# coding:utf-8
from qmaterialwidgets import InfoBadge, NavigationBar, TabWidget, InfoBadgePosition, FluentIcon, DotInfoBadge

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.icon import Icon


class NavigationViewInterface(GalleryInterface):
    """ Navigation view interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.navigation,
            subtitle="qmaterialwidgets.components.navigation",
            parent=parent
        )
        self.setObjectName('navigationViewInterface')

        # navigation bar
        self.addExampleCard(
            title='Navigation bar',
            widget=self.createNavigationBar(),
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/navigation_bar/demo.py'
        )

        # tab widget
        self.addExampleCard(
            title='Tab widget',
            widget=self.createTabWidget(),
            sourcePath='https://github.com/zhiyiYo/QMaterialWidgets/blob/master/examples/tab_widget/demo.py',
        )

    def createNavigationBar(self):
        bar = NavigationBar(self)
        bar.addItem('Mail', Icon.MAIL_OUTLINE, 'Mail', selectedIcon=Icon.MAIL)
        bar.addItem('Chat', Icon.CHAT_BUBBLE_OUTLINE, 'Chat', selectedIcon=Icon.CHAT_BUBBLE)
        bar.addItem('Rooms', Icon.PEOPLE_OUTLINE, 'Rooms', selectedIcon=Icon.PEOPLE)
        bar.addItem('Meet', Icon.VIDEOCAM_OUTLINE, 'Meet', selectedIcon=Icon.VIDEOCAM)
        DotInfoBadge.success(bar, bar.widget('Mail'), InfoBadgePosition.NAVIGATION_ITEM)
        InfoBadge.error(1, bar, bar.widget('Chat'), InfoBadgePosition.NAVIGATION_ITEM)
        DotInfoBadge.attension(bar, bar.widget('Rooms'), InfoBadgePosition.NAVIGATION_ITEM)
        InfoBadge.warning(3, bar, bar.widget('Meet'), InfoBadgePosition.NAVIGATION_ITEM)
        bar.setCurrentItem('Mail')
        return bar

    def createTabWidget(self):
        tab = TabWidget(self)
        tab.addItem('Mail', icon=FluentIcon.MAIL, text='Mail')
        tab.addItem('Chat', icon=FluentIcon.CHAT, text='Chat')
        tab.addItem('Rooms', icon=FluentIcon.PEOPLE, text='Rooms')
        tab.addItem('Meet', icon=FluentIcon.CAMERA, text='Meet')
        tab.setCurrentItem('Mail')
        return tab