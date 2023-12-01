import os
from bohriumsdk.client import Client
from bohriumsdk.storage import Storage
import humps

class Job:
    def __init__(
            self, 
            client: Client = None
        ) -> None:
        self.client = client
        self.store = Storage(client = client)

    def list_by_page(self, job_group_id=0, status=None, page=1, per_page=50):
        self.client.params['page'] = page
        self.client.params['pageSize'] = per_page
        if job_group_id > 0:
            self.client.params['groupId'] = job_group_id
        if status:
            self.client.params['status'] = status
        data = self.client.get(f'/openapi/v1/job/list', params=self.client.params)
        return data
    

    def list_by_number(self, number=10, status=None, job_group_id=0):
        if status is None:
            status = []
        per_page = 50
        job_list = []
        data = self.list_by_page(
            job_group_id = job_group_id,
            page = 1,
            per_page = per_page,
            status = status)
        total = data.get("total")
        per_page = data.get("pageSize")
        page_number = 0
        while page_number * per_page < total:
            page_number = page_number + 1
            if page_number > 1:
                data = self.list_by_page(job_group_id, page_number, per_page, status)
            for each in data.get("items"):
                job_list.append(each)
                if number != -1 and len(job_list) >= number:
                    return job_list
        return job_list
    
    def delete(self, job_id):
        data = self.client.post(f"/openapi/v1/job/del/{job_id}", params=self.client.params)
        return data
    
    def terminate(self, job_id):
        data = self.client.post(f'/openapi/v1/job/terminate/{job_id}', params=self.client.params)
        return data
    
    def kill(self, job_id):
        data = self.client.post(f'/openapi/v1/job/kill/{job_id}', params=self.client.params)
        return data
    
    def log(self, job_id, log_file="STDOUTERR", page=-1, page_size=8192):
        self.client.params['logFile'] = log_file
        self.client.params['page'] = page
        self.client.params['pageSize'] = page_size
        data = self.client.get(f'/openapi/v1/job/{job_id}/log', params=self.client.params)
        return data

    def insert(self, **kwargs):
        must_fill = ['job_type', 'oss_path', 'project_id', 'scass_type', 'cmd', 'platform', 'image_address', 'job_id']
        for each in must_fill:
            if each not in kwargs:
                raise ValueError(f'{each} is required when submitting job')
        camel_data = {humps.camelize(k): v for k, v in kwargs.items()}
        if not isinstance(camel_data['ossPath'], list):
            camel_data['ossPath'] = [camel_data['ossPath']]
        if 'logFile' in camel_data:
            camel_data['logFiles'] = camel_data['logFile']
        if 'logFiles' in camel_data and not isinstance(camel_data['logFiles'], list):
            camel_data['logFiles'] = [camel_data['logFiles']]
        data = self.client.post(f"/openapi/v2/job/add", json=camel_data, params=self.client.params)
        return data


    def detail(self, job_id):
        data = self.client.get(f'/openapi/v1/job/{job_id}', params=self.client.params)
        return data
    
    def create(self, project_id, name='', group_id=0):
        data = {
            'projectId': project_id
        }
        if name:
            data['name'] = name
        if group_id:
            data['bohrGroupId'] = group_id
        try:
            data = self.client.post(f'/openapi/v1/job/create', json=data, params=self.client.params)
        except Exception as e:
            raise e
        return data
    
    def create_job_group(self, project_id, job_group_name):
        data = {
            "name": job_group_name,
            "projectId": project_id
        }
        try:
            data = self.client.post(f"/openapi/v1/job_group/add", json=data, params=self.client.params)
        except Exception as e:
            raise e
        return data
    
    def get_job_token(self, job_id):
        url = f"/openapi/v1/job/{job_id}/input/token"
        data = self.client.get(url=url, params=self.client.params)
        print(data)

    def upload(self, file_path, object_key, token):
        self.store.upload_From_file_multi_part(
            object_key=object_key,
            file_path=file_path,
            token=token,
            progress_bar=True)

    def uploadr(self, work_dir, store_path, token):
        if not work_dir.endswith('/'):
            work_dir = work_dir + '/'
        for root, _, files in os.walk(work_dir):
            for file in files:
                full_path = os.path.join(root, file)
                object_key = full_path.replace(work_dir, store_path)
                self.upload(full_path, object_key, token)

    def submit(
            self,
            project_id,
            job_name,
            machine_type,
            cmd,
            image_address,#镜像地址
            job_group_id=0,
            work_dir='',
            platform='ali',
            log_files=[],
            out_files=[]):
        job_params = {"input_file_type": 2,"input_file_method": 4}
        data = self.create(project_id=project_id, name=job_name, group_id=job_group_id)

        if work_dir != '':
            if not os.path.exists(work_dir):
                raise FileNotFoundError
            if os.path.isdir(work_dir):
                self.uploadr(work_dir, data["storePath"], data["token"])
            else:
                file_name = os.path.basename(work_dir)
                object_key = os.path.join(data["storePath"], file_name)
                self.upload(work_dir, object_key, data["token"])
        
        job_params['job_name'] = job_name
        job_params['project_id'] = project_id
        job_params['job_id'] = data["jobId"]
        job_params['oss_path'] = data["storePath"]
        job_params['image_address'] = image_address
        job_params['scass_type'] = machine_type
        job_params['cmd'] = cmd
        job_params['platform'] = platform
        job_params['log_files'] = log_files
        job_params['out_files'] = out_files
        job_params['job_type'] = 'container'
        return self.insert(**job_params)
    
    def download(self, job_id, save_path):
        detail = self.detail(job_id)
        self.store.download_from_url(detail['resultUrl'], save_path)