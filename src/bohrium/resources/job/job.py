import logging
from ..._resource import AsyncAPIResource, SyncAPIResource
from ..tiefblue.tiefblue import Tiefblue
from ...types.job.job import JobAddRequest
# from ..._resource import BaseClient
from pprint import pprint
from typing import Optional
import os
from pathlib import Path
import uuid
# log: logging.Logger = logging.getLogger(__name__)


class Job(SyncAPIResource):

    def submit(
        self, 
        project_id: int, 
        job_name: str,
        machine_type: str,
        cmd: str,
        image_address: str,
        job_group_id: int = 0,
        work_dir: str = '',
        result: str = '',
        dataset_path: list = [],
        log_files: list = [],
        out_files: list = [],
    ):
        # log.info(f"submit job {name},project_id:{project_id}")
        data = self.create_job(project_id, job_name, job_group_id)
        print(data)
        if work_dir != '':
            if not os.path.exists(work_dir):
                raise FileNotFoundError
            if os.path.isdir(work_dir):
                self.uploadr(work_dir, data["storePath"], data["token"])
            else:
                file_name = os.path.basename(work_dir)
                object_key = os.path.join(data["storePath"], file_name)
                self.upload(work_dir, object_key, data["token"])
                
        ep = os.path.expanduser(result)
        p = Path(ep).absolute().resolve()
        p = p.joinpath(str(uuid.uuid4()) + "_temp.zip")
        
        job_add_request = JobAddRequest(
            download_path=str(p.absolute().resolve()),
            dataset_path=dataset_path,
            job_name=job_name,
            project_id=project_id,
            job_id=data["jobId"],
            oss_path=data["storePath"],
            image_name=image_address,
            scass_type=machine_type,
            cmd=cmd,
            log_files=log_files,
            out_files=out_files
        )
        return self.insert(job_add_request.to_dict())
    
    def insert(self, data):
        # log.info(f"insert job {data}")
        response = self._client.post(f"/openapi/v2/job/add", json=data)
        pprint(response.request)
        print(response.json())
    
    def delete(self, job_id):
        # log.info(f"delete job {job_id}")
        response = self._client.post(f"/openapi/v1/job/del/{job_id}")
        pprint(response.request)
        print(response.json())
        
    def terminate(self, job_id):
        # log.info(f"terminate job {job_id}")
        response = self._client.post(f"/openapi/v1/job/terminate/{job_id}")
        pprint(response.request)
        print(response.json())
        
    def kill(self, job_id):
        # log.info(f"kill job {job_id}")
        response = self._client.post(f"/openapi/v1/job/kill/{job_id}")
        pprint(response.request)
        print(response.json())
        
    def log(self, job_id, log_file="STDOUTERR", page=-1, page_size=8192):
        # log.info(f"log job {job_id}")
        response = self._client.get(f"/openapi/v1/job/{job_id}/log", params={"logFile": log_file, "page": page, "pageSize": page_size})
        pprint(response.request)
        print(response.json())
        
    def detail(self, job_id):
        # log.info(f"detail job {job_id}")
        response = self._client.get(f"/openapi/v1/job/{job_id}")
        pprint(response.request)
        print(response.json())

    def create_job(
        self,
        project_id: int,
        name: Optional[str] = None,
        group_id: Optional[int] = 0,
    ):
        # log.info(f"create job {name}")
        data = {
            "projectId": project_id,
            "name": name,
            "bohrGroupId": group_id,
        }
        response = self._client.post(f"/openapi/v1/job/create", json=data)
        pprint(response.request)
        print(response.json())
        return response.json().get("data")
    
    def create_job_group(self, project_id, job_group_name):
        # log.info(f"create job group {job_group_name}")
        response = self._client.post(f"/openapi/v1/job_group/add", json={"name": job_group_name, "projectId": project_id})
        pprint(response.request)
        print(response.json())
        
    def upload(
        self,
        file_path: str,
        object_key: str,
        token: str,
    ):
        tiefblue = Tiefblue()
        tiefblue.upload_From_file_multi_part(
            object_key=object_key,
            file_path=file_path,
            progress_bar=True)
        
    def uploadr(self, work_dir, store_path, token):
        if not work_dir.endswith('/'):
            work_dir = work_dir + '/'
        for root, _, files in os.walk(work_dir):
            for file in files:
                full_path = os.path.join(root, file)
                object_key = full_path.replace(work_dir, store_path)
                self.upload(full_path, object_key, token)


class AsyncJob(AsyncAPIResource):
    pass

