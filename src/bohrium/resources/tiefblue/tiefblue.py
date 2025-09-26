import requests
import json
import base64
import os
from tqdm import tqdm
import time
from typing import Union
from ..._base_client import SyncAPIClient
from httpx import URL
from pprint import pprint



_DEFAULT_CHUNK_SIZE = 50 * 1024 * 1024
_DEFAULT_ITERATE_MAX_OBJECTS = 50
class Parameter(object):
    contentType: str
    contentEncoding: str
    contentLanguage: str
    contentDisposition: str
    cacheControl: str
    acl: str
    expires: str
    userMeta: dict
    predefinedMeta: str

class Tiefblue:
    TIEFBLUE_HEADER_KEY = 'X-Storage-Param'

    def __init__(
            self,
            base_url: Union[str, URL] = None,
        ) -> None:
        
        if base_url is None:
            base_url = os.environ.get("TIEFBLUE_BASE_URL")
            
        if base_url is None:
            base_url = "https://tiefblue.dp.tech"
            
        self.base_url = base_url
        self.host = base_url  # 添加host属性
        self.client = SyncAPIClient(base_url=base_url)
        self.client.access_key = None

    
    def encode_base64(
            self, 
            parameter: dict = {}
        ) -> str:
        j = json.dumps(parameter)
        return base64.b64encode(j.encode()).decode()

    def write(
            self, 
            object_key: str = "", 
            data: str = "" , 
            parameter: dict = {}, 
            token: str = "",
            progress_bar: dict = {}
        ) -> dict:

        param = {
            "path": object_key,
            'option': parameter
        }

        if parameter:
            param["option"] = parameter.__dict__
        headers = {
            "Authorization": f"Bearer {token}",
        }
        headers[self.TIEFBLUE_HEADER_KEY] = self.encode_base64(param)
        req = self.client.post("/api/upload/binary", headers=headers, data=data)

        return req
    
    def read(
            self,
            object_key: str = "",
            token: str = "",
            ranges: str = ""
        ) -> None:

        url = f"/api/download/{object_key}"
        self.client.token = token
        res = self.client.get(url, host=self.host, stream=True)
        return res
    

    def upload_from_file(
            self,
            object_key: str = "",
            file_path: str = "",
            token: str = "",
            parameter: dict = None
        ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if os.path.isdir(file_path):
            raise IsADirectoryError
        _, disposition = os.path.split(file_path)
        if parameter is None:
            parameter = Parameter()
        parameter.contentDisposition = f'attachment; filename="{disposition}"'
        with open(file_path, 'rb') as fp:
            res = self.write(object_key=object_key, data=fp.read(), parameter=parameter, token=token)
            return res
    
    def init_upload_by_part(self, object_key: str, parameter=None, token: str = ""):
        data = {
            'path': object_key
        }
        if parameter is not None:
            data['option'] = parameter.__dict__
        headers = {
            "Authorization": f"Bearer {token}",
        }
        url = f"/api/upload/multipart/init"
        return self.client.post(url, host=self.host, headers=headers, json=data)
    
    def upload_by_part(self, object_key: str, initial_key: str, chunk_size: int, number: int, body, token: str = ""):
        param = {
            'initialKey': initial_key,
            'number': number,
            'partSize': chunk_size,
            'objectKey': object_key
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        headers[self.TIEFBLUE_HEADER_KEY] = self._dump_parameter(param)
        url = f"/api/upload/multipart/upload"
        resp = self.client.post(url, host=self.host, data=body, headers=headers)
        return resp


    def complete_upload_by_part(self, object_key, initial_key, part_string, token):
        data = {
            'path': object_key,
            'initialKey': initial_key,
            'partString': part_string
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        url = f"/api/upload/multipart/complete"
        resp = self.client.post(url, host=self.host, headers=headers, json=data)
        return resp
    
    def upload_From_file_multi_part(
            self,
            object_key: str,
            file_path: str,
            chunk_size: int = _DEFAULT_CHUNK_SIZE,
            parameter = None,
            progress_bar = False,
            need_parse = False,
            token: str = ""
        ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if os.path.isdir(file_path):
            raise IsADirectoryError
        if need_parse:
            _, _, object_key = self._parse_ap_name_and_tag(object_key)
        size = os.path.getsize(file_path)
        _, disposition = os.path.split(file_path)
        if parameter is None:
            parameter = Parameter()
        parameter.contentDisposition = f'attachment; filename="{disposition}"'
        bar_format = "{l_bar}{bar}| {n:.02f}/{total:.02f} %  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        with open(file_path, 'rb') as f:
            pbar = tqdm(total=100, desc=f"Uploading {disposition}", smoothing=0.01, bar_format=bar_format,
                        disable=not progress_bar)
            if size < _DEFAULT_CHUNK_SIZE * 2:

                self.write(object_key=object_key, data=f.read(), parameter=parameter, token=token)
                pbar.update(100)
                pbar.close()
                return
            chunks = split_size_by_part_size(size, chunk_size)
            initial_key = self.init_upload_by_part(object_key, parameter, token).json()['data'].get('initialKey')
            part_string = []
            uploaded = 0
            for c in chunks:
                f.seek(c.Offset)
                chunk_data = f.read(c.Size)
                resp = self.upload_by_part(
                    object_key, initial_key, chunk_size=c.Size, number=c.Number,
                    body=chunk_data, token=token
                )
                part_string.append(resp.json()['data'].get('partString'))
                uploaded += c.Size
                percent = uploaded * 100 / size
                pbar.n = percent
                pbar.refresh()
            pbar.update(100 - pbar.n)
            pbar.close()
            return self.complete_upload_by_part(object_key, initial_key, part_string, token)

    def download_from_file(self):

        data = self.client.get()

    def download_from_url(self, url, save_file):
        ret = None
        for retry_count in range(3):
            try:
                ret = requests.get(url, stream=True)
            except Exception as e:
                continue
            if ret.ok:
                break
            else:
                time.sleep(retry_count)
        if ret is not None:
            ret.raise_for_status()
            with open(save_file, "wb") as f:
                for chunk in ret.iter_content(chunk_size=8192):
                    f.write(chunk)
            ret.close()

    def _dump_parameter(self, parameter):
        j = json.dumps(parameter)
        return base64.b64encode(j.encode()).decode()
    
    def decode_base64(self, encode_data):
        data = json.loads(base64.b64decode(encode_data).decode('utf-8'))
        return data

    def _parse_ap_name_and_tag(self, input_path: str):
        l = input_path.split('/')
        if len(l) < 3:
            return "", "", l
        return l[0], l[1], "/".join(l[2:])



class Chunk:
    Number: int
    Offset: int
    Size: int
   
def split_size_by_part_size(total_size: int, chunk_size: int):
    if chunk_size < _DEFAULT_CHUNK_SIZE:
        chunk_size = _DEFAULT_CHUNK_SIZE
    chunk_number = int(total_size / chunk_size)
    if chunk_number >= 10000:
        raise TooManyChunk
    chunks = []
    for i in range(chunk_number):
        c = Chunk()
        c.Number = i + 1
        c.Offset = i * chunk_size
        c.Size = chunk_size
        chunks.append(c)

    if total_size % chunk_size > 0:
        c = Chunk()
        c.Number = len(chunks) + 1
        c.Offset = len(chunks) * chunk_size
        c.Size = total_size % chunk_size
        chunks.append(c)
    return chunks


def partial_with_start_from(start_bytes):
    return f'bytes={start_bytes}-'


def partial_with_end_from(end_bytes):
    return f'bytes=-{end_bytes}'


def partial_with_range(start_bytes, end_bytes):
    return f'bytes={start_bytes}-{end_bytes}'


TooManyChunk = Exception("too many chunks, please consider increase your chunk size")
