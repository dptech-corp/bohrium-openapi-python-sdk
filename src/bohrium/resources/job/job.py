import logging

from ..._resource import AsyncAPIResource, SyncAPIResource

from pprint import pprint

log: logging.Logger = logging.getLogger(__name__)


class Job(SyncAPIResource):

    def submit(self, project_id, name):
        log.info(f"submit job {name},project_id:{project_id}")

    def get(self, job_id):
        log.info(f"get job {job_id}")
        response = self._client.get(f"/openapi/v1/job/{job_id}")

        pprint(response.request)

        print(response.json())


class AsyncJob(AsyncAPIResource):
    pass
