from bohrium import Bohrium

if __name__ == "__main__":

    bohrium = Bohrium(
        access_key="access_key",
        project_id="project_id"
    )

    # job = bohrium.job.submit("project_id", "name")
    job = bohrium.job.get("job_id")
