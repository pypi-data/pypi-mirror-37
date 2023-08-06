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
import json

class AeselObject(object):
    """
    Data Model for Renderable Object.
    """
    def __init__(self):
        self.key = None
        self.name = None
        self.scene = None
        self.type = None
        self.subtype = None
        self.frame = None
        self.timestamp = None
        self.transform = []
        self.translation = []
        self.euler_rotation = []
        self.quaternion_rotation = []
        self.scale = []
        self.translation_handle = None
        self.rotation_handle = None
        self.scale_handle = None

    def to_dict(self):
        return_dict = copy.deepcopy(vars(self))
        if self.translation_handle is not None:
            return_dict['translation_handle'] = vars(self.translation_handle)
            return_dict['rotation_handle'] = vars(self.rotation_handle)
            return_dict['scale_handle'] = vars(self.scale_handle)
        return return_dict

    def to_transform_json(self):
        msg_dict = {
                    "msg_type": 1,
                    "key":self.key,
                    "name":self.name,
                    "frame":self.frame,
                    "scene":self.scene,
                    "transform": self.transform
                    }
        if self.translation_handle is not None:
            msg_dict['translation_handle'] = vars(self.translation_handle)
        if self.rotation_handle is not None:
            msg_dict['rotation_handle'] = vars(self.rotation_handle)
        if self.scale_handle is not None:
            msg_dict['scale_handle'] = vars(self.scale_handle)
        return json.dumps(msg_dict)
