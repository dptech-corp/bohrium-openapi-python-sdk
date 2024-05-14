import logging
from ..._resource import AsyncAPIResource, SyncAPIResource
# from ..._resource import BaseClient
from pprint import pprint

log: logging.Logger = logging.getLogger(__name__)


class Job(SyncAPIResource):

    def submit(self, project_id, name):
        log.info(f"submit job {name},project_id:{project_id}")

    def delete(self, job_id):
        log.info(f"delete job {job_id}")
        response = self._client.post(f"/openapi/v1/job/del/{job_id}")

        pprint(response.request)

        print(response.json())
        
    def terminate(self, job_id):
        log.info(f"terminate job {job_id}")
        response = self._client.post(f"/openapi/v1/job/terminate/{job_id}")

        pprint(response.request)

        print(response.json())
        
    def kill(self, job_id):
        log.info(f"kill job {job_id}")
        response = self._client.post(f"/openapi/v1/job/kill/{job_id}")

        pprint(response.request)

        print(response.json())
        
    def log(self, job_id, log_file="STDOUTERR", page=-1, page_size=8192):
        log.info(f"log job {job_id}")
        response = self._client.get(f"/openapi/v1/job/{job_id}/log", params={"logFile": log_file, "page": page, "pageSize": page_size})

        pprint(response.request)

        print(response.json())
        
    def detail(self, job_id):
        log.info(f"detail job {job_id}")
        response = self._client.get(f"/openapi/v1/job/{job_id}")

        pprint(response.request)

        print(response.json())

    def create_job_group(self, project_id, job_group_name):
        log.info(f"create job group {job_group_name}")
        response = self._client.post(f"/openapi/v1/job_group/add", json={"name": job_group_name, "projectId": project_id})

        pprint(response.request)

        print(response.json())

class AsyncJob(AsyncAPIResource):
    pass

