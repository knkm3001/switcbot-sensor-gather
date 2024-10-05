import json
import time
import hashlib
import hmac
import base64
import uuid
import requests

from modules.exceptions import *

class SwitchBotDeviceController():
    """
    cf. https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#update-webhook-configuration
    """

    BASE_URL = 'https://api.switch-bot.com/v1.1'

    def __init__(self,token:str, secret_key:str):
        self.base_url = self.BASE_URL
        self._token = token
        self._secret_key = secret_key
    
    def _create_api_header(self):
        apiHeader = {}

        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self._token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self._secret_key, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        #Build api header JSON
        apiHeader['Authorization']=self._token
        apiHeader['Content-Type']='application/json'
        apiHeader['charset']='utf8'
        apiHeader['t']=str(t)
        apiHeader['sign']=str(sign, 'utf-8')
        apiHeader['nonce']=str(nonce)

        #print(f'apiHeader: {apiHeader}')
        
        return apiHeader


    def get_devices(self,apiHeader=None):
        if apiHeader is None:
            apiHeader = self._create_api_header()
        response = requests.get(self.base_url+'/devices', headers=apiHeader)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIErrorExecption(f"Error: {response.status_code}, {response.json()}")


    def get_device_status(self, device_id:str):
        apiHeader = self._create_api_header()
        url = f'{self.base_url}/devices/{device_id}/status'
        response = requests.get(url, headers=apiHeader)
        if response.status_code == 200:
            return response.json()
        else:
            return APIErrorExecption(f"Error: {response.status_code}, {response.json()}")


    def exec_device_commands(self, device_id:str, payload:dict):
        apiHeader = self._create_api_header()
        url = f'{self.base_url}/devices/{device_id}/commands'

        response = requests.post(url, headers=apiHeader, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return APIErrorExecption(f"Error: {response.status_code}, {response.json()}")


    def get_scenes(self):
        apiHeader = self._create_api_header()
        url = f'{self.base_url}/scenes'
        response = requests.get(url, headers=apiHeader)
        if response.status_code == 200:
            return response.json()
        else:
            APIErrorExecption(f"Error: {response.status_code}, {response.json()}")
        

    def exec_scene(self, scene_id:str):
        apiHeader = self._create_api_header()
        url = f'{self.base_url}/scenes/{scene_id}/execute'

        response = requests.post(url, headers=apiHeader)
        if response.status_code == 200:
            return response.json()
        else:
            APIErrorExecption(f"Error: {response.status_code}, {response.json()}")

