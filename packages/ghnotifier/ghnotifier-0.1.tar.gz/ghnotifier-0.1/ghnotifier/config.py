#!/usr/bin/env python3

import configparser
import os


class Config:

    SECTION = 'DEFAULT'
    APP_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.config_file_path = self.APP_PATH + '/config.ini'
        self.configParser = configparser.ConfigParser()
        self.refresh()

    def get(self, name):
        return self.configParser.get(self.SECTION, name)

    def has(self, name):
        return self.configParser.has_option(self.SECTION, name) and self.configParser.get(self.SECTION, name)

    def set(self, name, value):
        self.configParser.set(self.SECTION, name, value)

    def update(self):
        self.configParser.write(open(self.config_file_path, 'w'))

    def refresh(self):
        self.configParser.read(self.config_file_path)