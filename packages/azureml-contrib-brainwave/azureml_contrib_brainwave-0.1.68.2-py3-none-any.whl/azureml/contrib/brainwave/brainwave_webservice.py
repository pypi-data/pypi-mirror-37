# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Deploy GRPC web services accelerated with Project Brainwave.
"""

import requests
from azureml.contrib.brainwave import BrainwaveImage
from dateutil.parser import parse
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._constants import MMS_SYNC_TIMEOUT_SECONDS
from azureml._model_management._util import _get_mms_url
from azureml.core.webservice import Webservice
from azureml.core.webservice.webservice import WebserviceDeploymentConfiguration
from azureml.exceptions import WebserviceException
import json
from pkg_resources import resource_string

import numpy as np
from .client import PredictionClient

realtimeai_service_payload_template = json.loads(resource_string(__name__,
                                                                 'data/brainwave_service_payload_template.json')
                                                 .decode('ascii'))


class BrainwaveWebservice(Webservice):
    """
    Class for AzureML RealTimeAI Webservices
    """
    _expected_payload_keys = ['name', 'description', 'kvTags', 'createdTime', 'computeType', 'keys', 'properties',
                              'sslEnabled', 'ipAddress', 'port', 'numReplicas']
    _webservice_type = 'FPGA'

    def _initialize(self, workspace, obj_dict):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        name = obj_dict['name']
        description = obj_dict['description']
        tags = obj_dict['kvTags']
        properties = obj_dict['properties']
        state = obj_dict['state'] if 'state' in obj_dict else None
        created_time = parse(obj_dict['createdTime'])
        updated_time = parse(obj_dict['updatedTime']) if 'updatedTime' in obj_dict else None
        error = obj_dict['error'] if 'error' in obj_dict else None
        compute_type = obj_dict['computeType']
        mms_endpoint = _get_mms_url(workspace) + '/services/{}'.format(name)
        super(BrainwaveWebservice, self)._initialize(name, description, tags, properties, state, created_time,
                                                     updated_time, error, compute_type, workspace, mms_endpoint,
                                                     None, workspace._auth)
        self.ssl = obj_dict['sslEnabled']
        self.port = obj_dict['port']
        self.ip_address = obj_dict['ipAddress']
        self.num_replicas = obj_dict['numReplicas']
        self.image_id = obj_dict['imageId']
        self.client = None

    @staticmethod
    def deploy_configuration(num_replicas=None, tags=None, description=None):
        """

        :param num_replicas:
        :type num_replicas: int
        :param tags:
        :type tags: list[str]
        :param description:
        :type description: str
        """
        config = RealTimeAIWebserviceDeploymentConfiguration(num_replicas, tags, description)
        return config

    @staticmethod
    def _deploy(workspace, name, image, deployment_config):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.image.Image
        :param deployment_config:
        :type deployment_config: RealTimeAIWebserviceDeploymentConfiguration
        :return:
        :rtype: AciWebservice
        """
        if not deployment_config:
            raise ValueError('deployment_config')
        if not image:
            raise ValueError('image not defined')
        deployment_config.validate_image(image)
        create_payload = BrainwaveWebservice._build_create_payload(name, deployment_config, image)
        return Webservice._deploy_webservice(workspace, name, create_payload, BrainwaveWebservice)

    @staticmethod
    def _build_create_payload(name, deploy_config, image):
        """

        :param name:
        :type name: str
        :param deploy_config:
        :type deploy_config: RealTimeAIWebserviceDeploymentConfiguration
        :param image:
        :type image: azureml.core.Image
        :return:
        :rtype: dict
        """
        import copy
        json_payload = copy.deepcopy(realtimeai_service_payload_template)
        json_payload['name'] = name
        json_payload['kvTags'] = deploy_config.tags
        json_payload['properties'] = deploy_config.properties
        json_payload['description'] = deploy_config.description
        json_payload['numReplicas'] = deploy_config.num_replicas
        json_payload['sslEnabled'] = deploy_config.ssl_enabled
        json_payload['imageId'] = image.id
        return json_payload

    def wait_for_deployment(self, show_output=False):
        """
        Wait for the service to finish deploying.
        :param show_output:
        :type show_output: bool
        :return:
        :rtype: None
        :raises: azureml.exceptions.azureml_exception.WebserviceException
        """
        try:
            operation_state, error = self._wait_for_deployment(show_output)
            print('Service creation operation finished, operation "{}"'.format(operation_state))
            if operation_state == 'Failed':
                if error and 'statusCode' in error and 'message' in error:
                    print('Service creation failed with\n'
                          'StatusCode: {}\n'
                          'Message: {}'.format(error['statusCode'], error['message']))
                else:
                    print('Service creation failed, unexpected error response:\n'
                          '{}'.format(error))
            self.update_deployment_state()
        except WebserviceException as e:
            if e.message == 'No operation endpoint':
                self.update_deployment_state()
                print('Long running operation information not known, unable to poll. '
                      'Current state is {}'.format(self.state))
            else:
                raise e

    def update_deployment_state(self):
        """
        Update the current properties on the webservice. Primarily useful for manual polling of deployment state.
        :return:
        :rtype: None
        """
        service = Webservice(self.workspace, name=self.name)
        for key in self.__dict__.keys():
            self.__dict__[key] = service.__dict__[key]

    def run(self, input_data):
        """
        :param input_data:
        :type input_data: File | np.array | Path to image
        :return:
        """
        if self.ssl:
            raise NotImplementedError("Use azureml.contrib.realtimeai.client.PredictionClient directly with the"
                                      "FullyQualified domain name of the service")
        if self.client is None:
            self.client = PredictionClient(self.ip_address, self.port, False, "")
        if isinstance(input_data, str):
            return self.client.score_image(input_data)
        if isinstance(input_data, np.ndarray):
            return self.client.score_numpy_array(input_data)
        return self.client.score_file(input_data.read())

    def update(self, image=None, num_replicas=None, tags=None, description=None, ssl_enabled=None,
               ssl_certificate=None, ssl_key=None):
        """

        :param num_replicas:
        :type num_replicas: int
        :param ssl_key:
        :type ssl_key: str
        :param ssl_certificate:
        :type ssl_certificate: str
        :param ssl_enabled:
        :type ssl_enabled: bool | None
        :param image:
        :type image: BrainwaveImage
        :param tags:
        :type tags: list[str]
        :param description:
        :type description: str
        :return:
        :rtype: None
        """
        if tags is None and not description and not image and ssl_enabled is None and not num_replicas:
            raise WebserviceException('No parameters provided to update.')

        if ssl_enabled and (ssl_certificate is None or ssl_key is None):
            raise ValueError("Must provide certificate and key if SSL is enabled")

        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        if image:
            patch_list.append({'op': 'replace', 'path': '/imageId', 'value': image.id})
        if num_replicas:
            patch_list.append({'op': 'replace', 'path': '/numReplicas', 'value': num_replicas})
        if tags is not None:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})

        if ssl_enabled:
            patch_list.append({'op': 'replace', 'path': '/sslEnabled', 'value': True})
            patch_list.append({'op': 'replace', 'path': '/sslCertificate', 'value': ssl_certificate})
            patch_list.append({'op': 'replace', 'path': '/sslKey', 'value': ssl_key})
        if ssl_enabled is False:
            patch_list.append({'op': 'replace', 'path': '/sslEnabled', 'value': False})
            patch_list.append({'op': 'remove', 'path': '/sslCertificate'})
            patch_list.append({'op': 'remove', 'path': '/sslKey'})

        resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list,
                              timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            self.update_deployment_state()
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    def serialize(self):
        """
        Convert this Webservice into a json serialized dictionary.
        :return: The json representation of this Webservice
        :rtype: dict
        """
        properties = super(BrainwaveWebservice, self).serialize()
        rt_properties = {'num_replicas': self.num_replicas}
        properties.update(rt_properties)
        return properties

    @staticmethod
    def deserialize(workspace, webservice_payload):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param object_dict:
        :type object_dict: dict
        :return:
        :rtype: BrainwaveWebservice
        """
        BrainwaveWebservice._validate_get_payload(webservice_payload)
        webservice = BrainwaveWebservice(None)
        webservice._initialize(workspace, webservice_payload)
        return webservice

    @staticmethod
    def _validate_get_payload(payload):
        """

        :param payload:
        :type payload: dict
        :return:
        :rtype: None
        """
        if 'computeType' not in payload:
            raise WebserviceException('Invalid webservice payload, missing computeType:\n'
                                      '{}'.format(payload))
        if payload['computeType'] != BrainwaveWebservice._webservice_type:
            raise WebserviceException('Invalid payload for RealtimeAi webservice":\n'
                                      '{}'.format(payload))
        for service_key in BrainwaveWebservice._expected_payload_keys:
            if service_key not in payload:
                raise WebserviceException('Invalid RealTimeAI webservice payload, missing "{}":\n'
                                          '{}'.format(service_key, payload))

    def delete(self):
        """
        Delete this Webservice from its associated workspace

        :raises: WebserviceException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        resp = requests.delete(self._mms_endpoint, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            self.state = 'Deleting'
        if resp.status_code == 202:
            self.state = 'Deleting'
        elif resp.status_code == 204:
            print('No service with name {} found to delete.'.format(self.name))
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))


class RealTimeAIWebserviceDeploymentConfiguration(WebserviceDeploymentConfiguration):
    """
    Service deployment configuration object for services deployed on RealTimeAI compute.
    """

    def __init__(self, num_replicas=None, tags=None, properties=None, description=None, ssl_enabled=False,
                 ssl_certificate=None, ssl_key=None):
        """

        :param num_replicas:
        :type num_replicas: int
        :param tags:
        :type tags: list[str]
        :param description:
        :type description: str
        """
        super(RealTimeAIWebserviceDeploymentConfiguration, self).__init__(BrainwaveWebservice)
        self.num_replicas = num_replicas if num_replicas is not None else 1
        self.tags = tags
        self.description = description
        self.ssl_enabled = ssl_enabled
        self.ssl_certificate = ssl_certificate
        self.ssl_key = ssl_key
        self.properties = properties
        self.validate_configuration()

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a WebserviceException if validation
        fails.
        :raises: WebserviceException
        """
        if self.num_replicas and self.num_replicas <= 0:
            raise WebserviceException('Invalid configuration, num_replicas must be positive.')
        if (self.ssl_key or self.ssl_certificate) and not self.ssl_enabled:
            raise WebserviceException('Invalid configuration, can only pass certificate and key if ssl is enabled')
        if self.ssl_enabled and not (self.ssl_key and self.ssl_certificate):
            raise WebserviceException('Invalid configuration, cannot enable SSL without certificate and key')

    @classmethod
    def validate_image(cls, image):
        """
        Checks that the image that is being deployed to the webservice is valid.
        Will raise a WebserviceException if validation fails.
        :param image: The image that will be deployed to the webservice.
        :raises: WebserviceException
        """
        if not isinstance(image, BrainwaveImage):
            raise WebserviceException("Can only deploy Brainwave web service from a BrainwaveImage")
        if image.creation_state != 'Succeeded':
            raise WebserviceException('Unable to create service with image {} in non "Succeeded" state'
                                      .format(image.id))
