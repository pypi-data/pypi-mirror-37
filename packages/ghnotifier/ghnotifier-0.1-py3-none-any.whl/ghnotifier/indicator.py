#!/usr/bin/env python3

import gi

gi.require_version('AppIndicator3', '0.1')

from gi.repository import AppIndicator3, GObject
from ghnotifier.config import Config


class Indicator:

    INDICATOR_ID = 'Github Notifier'

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(
            self.INDICATOR_ID,
            Config.APP_PATH + "/gh.png",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_label("0", '')

    def set_menu(self, menu):
        self.indicator.set_menu(menu)

    def update_label(self, label):
        GObject.idle_add(
            self.indicator.set_label,
            label, '',
            priority=GObject.PRIORITY_DEFAULT
        )
