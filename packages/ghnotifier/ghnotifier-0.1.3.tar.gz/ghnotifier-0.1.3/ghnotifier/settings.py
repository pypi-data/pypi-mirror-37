#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from ghnotifier.config import Config


class Settings(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.set_size_request(200, 100)
        self.set_border_width(10)
        self.config = Config()
        self.refreshTime = self.config.get('refreshTime')
        self.entry = None

        self.build_view()

    def build_view(self):
        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vertical_box)

        self.add_access_token_input(vertical_box)
        self.add_refresh_time_radio_buttons(vertical_box)

        horizontal_box = Gtk.Box(spacing=6)
        vertical_box.pack_start(horizontal_box, True, True, 0)

        save_button = Gtk.Button("_Save", use_underline=True)
        save_button.set_label("Save")
        save_button.connect("clicked", self.save)
        horizontal_box.pack_start(save_button, True, True, 0)

    def add_access_token_input(self, vertical_box):
        label = Gtk.Label("Access Token:")
        vertical_box.add(label)

        self.entry = Gtk.Entry()
        self.entry.set_text(self.config.get('accessToken'))
        vertical_box.pack_start(self.entry, True, True, 0)

    def add_refresh_time_radio_buttons(self, vertical_box):
        label = Gtk.Label("Refresh time:")
        vertical_box.add(label)

        horizontal_box = Gtk.Box(spacing=6)
        vertical_box.pack_start(horizontal_box, True, True, 0)

        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "10 seconds")
        button1.connect("toggled", self.on_button_toggled, "10")
        horizontal_box.pack_start(button1, False, False, 0)

        if "10" == self.refreshTime:
            button1.set_active(True)

        for refreshTime in ['30', '60', '300']:
            button = Gtk.RadioButton.new_from_widget(button1)
            button.set_label(refreshTime + " seconds")
            if refreshTime == self.refreshTime:
                button.set_active(True)
            button.connect("toggled", self.on_button_toggled, refreshTime)
            horizontal_box.pack_start(button, False, False, 0)

    def on_button_toggled(self, button, button_value):
        self.refreshTime = button_value

    def save(self, button):
        self.config.set('accessToken', self.entry.get_text())
        self.config.set('refreshTime', str(self.refreshTime))
        self.config.update()
        Gtk.main_quit()

    def open(self):
        self.connect("delete-event", Gtk.main_quit)
        self.set_resizable(False)
        self.show_all()
        Gtk.main()


Settings().open()
