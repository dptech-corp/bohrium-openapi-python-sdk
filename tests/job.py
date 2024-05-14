from bohrium import Bohrium

import httpx

if __name__ == "__main__":

    bohrium = Bohrium(
        access_key="access_key",
        project_id="project_id",
        timeout=httpx.Timeout(40.0),
    )

    # job = bohrium.job.submit("project_id", "name")
    job = bohrium.job.detail("job_id")
