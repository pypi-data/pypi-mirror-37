#!/usr/bin/env python3

import webbrowser
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from ghnotifier.notifier import Notifier
from ghnotifier.settings import Settings


class Menu:

    GITHUB_NOTIFICATIONS = 'https://github.com/notifications'

    def __init__(self):
        self.menu = Gtk.Menu()
        self.create_menu()
        self.menu.show_all()

    def create_menu(self):
        self.append('Open Notifications', self.notifications)
        self.append('Settings', self.settings)

        self.menu.append(Gtk.SeparatorMenuItem())

        self.append('Quit', self.quit)

    def append(self, name, callback):
        item = Gtk.MenuItem(name)
        item.connect('activate', callback)

        self.menu.append(item)

    @staticmethod
    def notifications(source):
        webbrowser.open(Menu.GITHUB_NOTIFICATIONS)

    @staticmethod
    def settings(source):
        Settings().open()

    @staticmethod
    def quit(source):
        Notifier.stop()
        Gtk.main_quit()

    def get_inner(self):
        return self.menu