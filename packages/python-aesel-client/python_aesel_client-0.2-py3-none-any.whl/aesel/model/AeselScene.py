#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Apache2 License Notice
Copyright 2018 Alex Barry
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import copy

class AeselScene(object):
    """
    Data Model for Scene.
    """
    def __init__(self):
        self.key = None
        self.name = None
        self.region = None
        self.latitude = None
        self.longitude = None
        self.tags = []
        self.devices = []

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        return_dict['devices'] = []
        for device in self.devices:
            device_dict = vars(device)
            if device.transform is not None:
                device_dict['transform'] = vars(device.transform)
            return_dict['devices'].append(device_dict)
        return return_dict
