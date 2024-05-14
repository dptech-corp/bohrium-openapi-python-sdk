from bohrium import Bohrium

import httpx

if __name__ == "__main__":

    bohrium = Bohrium(
        access_key="7d300756a875455a9faff8eaad2337bf",
        project_id="154",
        timeout=httpx.Timeout(40.0),
    )

    data = {
        "job_type": "container",
        "job_name": "test-name",
        "project_id": 154,
        "machine_type": "c2_m4_cpu",
        "cmd": "ls; echo 1asdfasdfasdfasdfasdfasdfasdf11 >> test.result;",
        "log_files": ["test.result"],
        "out_files": ["test.result"],
        "image_address": "registry.dp.tech/dptech/ubuntu:20.04-py3.10",
        "dataset_path": [],
        "work_dir": "./",
        "job_group_id": 0,
        "result": "/personal/test/result"
    }
    
    job = bohrium.job.submit(
        project_id=data["project_id"],
        job_name=data["job_name"],
        machine_type=data["machine_type"],
        cmd=data["cmd"],
        image_address=data["image_address"],
        job_group_id=data["job_group_id"],
        work_dir=data["work_dir"],
        result=data["result"],
        dataset_path=data["dataset_path"],
        log_files=data["log_files"],
        out_files=data["out_files"],
    )
    
    job = bohrium.job.detail("12513182")
