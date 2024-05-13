from ..._resource import SyncAPIResource, AsyncAPIResource


class Job(SyncAPIResource):
    def submit(self, project_id, name, script, **kwargs):
        pass


class AsyncJob(AsyncAPIResource):
    pass
