#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
The Main Client for accessing all
`HTTP Operations in the Aesel API <https://aesel.readthedocs.io/en/latest/pages/DVS_API.html>`__.
"""

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

from aesel.model.AeselAssetMetadata import AeselAssetMetadata
from aesel.model.AeselAssetRelationship import AeselAssetRelationship
from aesel.model.AeselDataList import AeselDataList
from aesel.model.AeselObject import AeselObject
from aesel.model.AeselProperty import AeselProperty
from aesel.model.AeselScene import AeselScene
from aesel.model.AeselSceneTransform import AeselSceneTransform
from aesel.model.AeselUserDevice import AeselUserDevice

import requests

class AeselTransactionClient(object):
    """
    Initializing the Transaction Client just requires the HTTP(s) address
    which it can use to communicate with the Aesel server.

    :param str aesel_url: The address of the Aesel servers.
    """
    def __init__(self, aesel_url):
        self.aesel_addr = aesel_url
        self.api_version = 'v1'

        # Start an HTTP Session
        # Includes a connection pool, and let's us set global auth attributes
        self.http_session = requests.session()

    # Internal method for generating the base URL String of the Aesel API
    def gen_base_url(self):
        return self.aesel_addr + "/" + self.api_version

    # Internal method for generating the Query Parameters for an Asset Request
    def gen_asset_params(self, asset, relationship):
        query_params = {}
        if asset is not None:
            query_params['content-type'] = asset.content_type
            query_params['asset-type'] = asset.asset_type
            query_params['file-type'] = asset.file_type
        if relationship is not None:
            query_params['related-id'] = relationship.related
            query_params['related-type'] = relationship.type
        return query_params

    # ------------------End User API Methods----------------------------

    def set_auth_info(self, auth_token):
        """
        Set the authentication token to be used on Requests

        :param str auth_token: The value of the auth token to use on requests
        """
        self.http_session.headers.update({"Authorization": "Bearer %s" % auth_token})

    def set_cookie(self, cookie):
        """
        Set the cookies contained in the Transaction sessions.

        :param cookie: A CookieJar object containing user cookies.
        """
        self.http_session.cookies = cookie

    # -------------
    # Asset Methods
    # -------------

    def create_asset(self, file, asset=None, relationship=None):
        """
        Create a New Asset in the Aesel Server.

        :param str file: The path to the file to save as an Asset
        :param asset: Optional AssetMetadata to associate with the Asset.
        :param relationship: Optional AssetRelationship to associate with the Asset.
        :return: The key of the newly created object.
        """
        # Set up query parameters
        query_params = self.gen_asset_params(asset, relationship)

        # Deduce the content-type
        content_type = "text/plain"
        if asset is not None:
            if asset.content_type is not None:
                content_type = asset.content_type

        # Send the HTTP Request
        request_file = {'file': (file, open(file, 'rb'), content_type, {'Expires': '0'})}
        r = self.http_session.post(self.gen_base_url() + "/asset", files=request_file, params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the body text, which is the Asset ID
        return r.text

    def update_asset(self, key, file, asset=None, relationship=None):
        """
        Update an existing Asset in the Aesel Server.

        :param str file: The path to the file to save as an Asset
        :param asset: Optional AeselAssetMetadata to associate with the Asset.
        :param relationship: Optional AeselAssetRelationship to associate with the Asset.
        :return: The key of the newly created object.
        """
        # Set up query parameters
        query_params = self.gen_asset_params(asset, relationship)

        # Deduce the content-type
        content_type = "text/plain"
        if asset is not None:
            if asset.content_type is not None:
                content_type = asset.content_type

        # Send the HTTP Request
        request_file = {'file': (file, open(file, 'rb'), content_type, {'Expires': '0'})}
        r = self.http_session.post(self.gen_base_url() + "/asset/" + key, files=request_file, params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the body text, which is the Asset ID
        return r.text

    def get_asset(self, key):
        """
        Get an Asset by Key, and return the content of the response.

        :param str key: The key of the Asset to retrieve
        :return: The content of the response, usually to be saved to a file.
        """
        # Send a get request
        r = self.http_session.get(self.gen_base_url() + "/asset/" + key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the content of the response, which can be written to a file
        return r.content

    def query_asset_metadata(self, asset):
        """
        Query Assets by Metadata, and return the json content of the response.

        :param asset: The AeselAssetMetadata which will be used as a match query.
        :return: JSON containing a list of Asset Metadata entries, including keys.
        """
        # Set up query parameters
        query_params = self.gen_asset_params(asset, None)

        # Send a get request
        r = self.http_session.get(self.gen_base_url() + "/asset", params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the content of the response, which can be written to a file
        return r.json()

    def get_asset_history(self, key):
        """
        Get an Asset History by Key, and return the json content of the response.

        :param str key: The key of the Asset to retrieve the history for
        :return: JSON containing an Asset History corresponding to the requested Asset.
        """
        # Send a get request
        r = self.http_session.get(self.gen_base_url() + "/history/" + key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the content of the response, which can be written to a file
        return r.json()

    def delete_asset(self, key):
        """
        Delete an Asset by Key.

        :param str key: The key of the Asset to delete
        """
        r = self.http_session.delete(self.gen_base_url() + "/asset/" + key, allow_redirects=True)
        r.raise_for_status()

    def save_asset_relationship(self, new_relationship, existing_relationship=None):
        """
        Add an Asset Relationship between the specified asset and related element

        :param new_relationship: The relationship to persist.
        :param existing_relationship: If we are updating, then what do we need to query on to find the existing relationship.
        :return: JSON containing the Relationship and ID.
        """
        query_params = {}
        if existing_relationship is not None:
            query_params['asset'] = existing_relationship.asset
            query_params['related'] = existing_relationship.related
            query_params['type'] = existing_relationship.type
            r = self.http_session.put(self.gen_base_url() + "/relationship", json=new_relationship.to_dict(), params=query_params)
        else:
            r = self.http_session.put(self.gen_base_url() + "/relationship", json=new_relationship.to_dict())

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def delete_asset_relationship(self, asset, type, related):
        """
        Delete an Asset Relationship

        :param str asset: The Asset key in the relationship to delete.
        :param str type: The type of the relationship to delete.
        :param str related: The related entity key in the relationship to delete.
        :return: JSON with deleted asset relationships.
        """
        query_params = {"asset": asset, "type": type, "related": related}
        r = self.http_session.delete(self.gen_base_url() + "/relationship", params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def query_asset_relationships(self, query):
        """
        Query for asset relationships.

        :param str query: The AeselAssetRelationship to use as a query.
        :return: JSON with a list of found asset relationships, including keys.
        """
        query_params = {}
        if query.asset is not None:
            query_params['asset'] = query.asset
        if query.related is not None:
            query_params['related'] = query.related
        if query.type is not None:
            query_params['type'] = query.type
        r = self.http_session.get(self.gen_base_url() + "/relationship", params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    # -------------
    # Scene Methods
    # -------------

    def create_scene(self, key, scene):
        """
        Create a new Scene with the given key

        :param str key: The key of the Scene to create
        :param scene: The AeselScene to persist.
        :return: JSON with a list of created scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = 1
        data_list.start_record = 0
        data_list.data.append(scene)
        r = self.http_session.put(self.gen_base_url() + "/scene/" + key, json=(data_list.to_dict("scenes")), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def update_scene(self, key, scene):
        """
        Update an existing Scene with the given key

        :param str key: The key of the Scene to update
        :param scene: The AeselScene to persist.
        :return: JSON with a list of updated scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = 1
        data_list.start_record = 0
        data_list.data.append(scene)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + key, json=data_list.to_dict("scenes"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def get_scene(self, key):
        """
        Get a Scene with the given key

        :param str key: The key of the Scene to update
        :return: JSON with a list of retrieved scenes.
        """
        r = self.http_session.get(self.gen_base_url() + "/scene/" + key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def delete_scene(self, key):
        """
        Delete a Scene with the given key

        :param str key: The key of the Scene to delete
        """
        r = self.http_session.delete(self.gen_base_url() + "/scene/" + key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

    def scene_query(self, scene, num_records=10, start_record=0):
        """
        Query for scenes by attribute.

        :param scene: The AeselScene to use as a query.
        :param num_records: How many records to retrieve.
        :param start_record: The first record to retrieve.  Works with num_records to support pagination.
        :return: JSON with a list of found scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = num_records
        data_list.start_record = start_record
        data_list.data.append(scene)
        r = self.http_session.post(self.gen_base_url() + "/scene/query", json=data_list.to_dict("scenes"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def register(self, scene_key, device, transform=None):
        """
        Register a device to a scene.  Potentially with a transformation.

        :param str scene_key: The key of the AeselScene to register to.
        :param device: The AeselUserDevice which is registering.
        :param transform: The starting AeselSceneTransform to register.
        :return: JSON with a list of updated scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = 2
        data_list.start_record = 0
        scene_data = AeselScene()
        scene_data.key = scene_key
        if transform is not None:
            device.transform = transform
        scene_data.devices.append(device)
        data_list.data.append(scene_data)

        # Send the request
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/register", json=data_list.to_dict("scenes"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def deregister(self, scene_key, device_key):
        """
        Deregister a device from a scene.

        :param str scene_key: The key of the AeselScene to deregister from.
        :param str device: The key of the AeselUserDevice which is deregistering.
        :return: JSON with a list of updated scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = 2
        data_list.start_record = 0
        scene_data = AeselScene()
        ud = AeselUserDevice()
        scene_data.key = scene_key
        ud.key = device_key
        scene_data.devices.append(ud)
        data_list.data.append(scene_data)

        # Send the request
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/deregister", json=data_list.to_dict("scenes"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def synchronize(self, scene_key, device_key, transform):
        """
        Correct the device transformation relative to the scene.

        :param scene_key: The key of the AeselScene in the relationship.
        :param device_key: The key of the AeselUserDevice which is registered.
        :param transform: The updated transformation.
        :return: JSON with a list of updated scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = 2
        data_list.start_record = 0
        scene_data = AeselScene()
        ud = AeselUserDevice()
        scene_data.key = scene_key
        ud.key = device_key
        ud.transform = transform
        scene_data.devices.append(ud)
        data_list.data.append(scene_data)

        # Send the request
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/align", json=data_list.to_dict("scenes"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    # --------------
    # Object Methods
    # --------------

    def create_object(self, scene_key, obj):
        """
        Create a new Object.

        :param str scene_key: The key of the AeselScene the object is associated to.
        :param obj: The AeselObject to persist.
        :return: JSON with a list of created objects, including the newly generated key.
        """
        data_list = AeselDataList()
        data_list.num_records = 1
        data_list.start_record = 0
        data_list.data.append(obj)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/object", json=data_list.to_dict("objects"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def update_object(self, scene_key, obj_key, obj):
        """
        Create a new Object.

        :param str scene_key: The key of the AeselScene the object is associated to.
        :param str obj_key: The key of the AeselObject to update.
        :param obj: The AeselObject to persist.
        :return: JSON with a list of created objects, including the newly generated key.
        """
        data_list = AeselDataList()
        data_list.num_records = 1
        data_list.start_record = 0
        data_list.data.append(obj)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/object/" + obj_key, json=data_list.to_dict("objects"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def get_object(self, scene_key, obj_key):
        """
        Get an Object by key.

        :param str scene_key: The key of the AeselScene to find the object in.
        :param str obj_key: The key of the AeselObject to get.
        :return: JSON with a list of created objects, including the newly generated key.
        """
        r = self.http_session.get(self.gen_base_url() + "/scene/" + scene_key + "/object/" + obj_key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def delete_object(self, scene_key, obj_key):
        """
        Delete an Object by key.

        :param str scene_key: The key of the AeselScene to find the object in.
        :param str obj_key: The key of the AeselObject to get.
        """
        r = self.http_session.delete(self.gen_base_url() + "/scene/" + scene_key + "/object/" + obj_key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

    def object_query(self, scene_key, object, num_records=999):
        """
        Query for objects by scene and attribute.

        :param str scene_key: The key of the AeselScene to find objects in.
        :param object: The AeselObject to use as a query.
        :param num_records: How many records to retrieve.
        :return: JSON with a list of found scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = num_records
        data_list.data.append(object)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/object/query", json=data_list.to_dict("objects"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def lock_object(self, scene_key, obj_key, device_key):
        """
        Lock an Object by key.

        :param str scene_key: The key of the AeselScene to find the object in.
        :param str obj_key: The key of the AeselObject to lock.
        :param str device_key: The key of the AeselUserDevice obtaining the lock.
        """
        query_params = {"device": device_key}
        r = self.http_session.get(self.gen_base_url() + "/scene/" + scene_key + "/object/" + obj_key + "/lock", params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

    def unlock_object(self, scene_key, obj_key, device_key):
        """
        Unlock an Object by key.

        :param str scene_key: The key of the AeselScene to find the object in.
        :param str obj_key: The key of the AeselObject to unlock.
        :param str device_key: The key of the AeselUserDevice obtaining the lock.
        """
        query_params = {"device": device_key}
        r = self.http_session.delete(self.gen_base_url() + "/scene/" + scene_key + "/object/" + obj_key + "/lock", params=query_params, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

    # ----------------
    # Property Methods
    # ----------------

    def create_property(self, scene_key, property):
        """
        Create a new Property.

        :param str scene_key: The key of the AeselScene the object is associated to.
        :param property: The AeselProperty to persist.
        :return: JSON with a list of created properties, including the newly generated key.
        """
        data_list = AeselDataList()
        data_list.num_records = 1
        data_list.start_record = 0
        data_list.data.append(property)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/property", json=data_list.to_dict("properties"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def update_property(self, scene_key, property_key, property):
        """
        Create a new Property.

        :param str scene_key: The key of the AeselScene the object is associated to.
        :param str property_key: The key of the AeselProperty to update.
        :param property: The AeselProperty to persist.
        :return: JSON with a list of created properties, including the newly generated key.
        """
        data_list = AeselDataList()
        data_list.num_records = 1
        data_list.start_record = 0
        data_list.data.append(property)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/property/" + property_key, json=data_list.to_dict("properties"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def get_property(self, scene_key, property_key):
        """
        Get a Property by key.

        :param str scene_key: The key of the AeselScene to find the object in.
        :param str property_key: The key of the AeselProperty to get.
        :return: JSON with a list of created properties, including the newly generated key.
        """
        r = self.http_session.get(self.gen_base_url() + "/scene/" + scene_key + "/property/" + property_key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()

    def delete_property(self, scene_key, property_key):
        """
        Delete an Property by key.

        :param str scene_key: The key of the AeselScene to find the object in.
        :param str property_key: The key of the AeselProperty to get.
        """
        r = self.http_session.delete(self.gen_base_url() + "/scene/" + scene_key + "/property/" + property_key, allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

    def property_query(self, scene_key, property, num_records=999):
        """
        Query for properties by scene and attribute.

        :param str scene_key: The key of the AeselScene to find objects in.
        :param property: The AeselProperty to use as a query.
        :param num_records: How many records to retrieve.
        :return: JSON with a list of found scenes.
        """
        data_list = AeselDataList()
        data_list.num_records = num_records
        data_list.data.append(property)
        r = self.http_session.post(self.gen_base_url() + "/scene/" + scene_key + "/property/query", json=data_list.to_dict("properties"), allow_redirects=True)

        # Throw an error for bad responses
        r.raise_for_status()

        # Return the json content of the response
        return r.json()
