#!/usr/bin/env python3

import gi
import requests

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import GLib, Notify
from ghnotifier.config import Config


class Notifier:

    GITHUB_API_NOTIFICATIONS = 'https://api.github.com/notifications'

    def __init__(self, indicator):
        self.indicator = indicator
        self.config = Config()
        self.notified = []

        Notify.init(indicator.INDICATOR_ID)

    def notify(self):
        self.config.refresh()
        GLib.timeout_add_seconds(int(self.config.get('refreshTime')), self.notify)

        if not self.config.has('accessToken'):
            Notify.Notification.new(
                "Missing Access Token", "Please go to settings and add an Access token."
            ).show()
            return

        notifications = self.get_notifications()

        if notifications is None:
            return

        for notification in notifications:
            if not self.is_notified(notification['id']):
                Notify.Notification.new(
                    "<b>" + notification['subject']['title'] + " @ " + notification['repository']['name'] + "</b>"
                ).show()
                self.notified.append(notification['id'])

        self.indicator.update_label(str(len(notifications)))

    def get_notifications(self):
        response = requests.get(
            self.GITHUB_API_NOTIFICATIONS,
            headers={
                'Authorization': 'token ' + self.config.get('accessToken'),
                'User-Agent': 'my app'
            }
        )

        if response.status_code != 200:
            Notify.Notification.new(
                "Something went wrong", "Github didn't respond as expected, check if your access token is correct."
            ).show()
            return

        return response.json()

    def is_notified(self, identifier):
        return identifier in self.notified

    @staticmethod
    def stop():
        Notify.uninit()
