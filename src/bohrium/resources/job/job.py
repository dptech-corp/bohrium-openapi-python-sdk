from ..._resource import SyncAPIResource, AsyncAPIResource


class Job(SyncAPIResource):
    def submit(self, project_id, name, script, **kwargs):
        data = {
            "projectId": project_id,
            "name": name,
            "script": script,
        }
        data.update(kwargs)
        return self._post("/openapi/v1/job/submit", data=data)


class AsyncJob(AsyncAPIResource):
    pass
