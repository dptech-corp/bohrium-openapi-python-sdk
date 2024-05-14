
from typing import List, Optional, Literal

class JobAddRequest(object):
    def __init__(
        self, 
        job_type: str = "",
        oss_path: List[str] = [],
        job_group_id: int = 0,
        project_id: int = 0,
        rerun: int = 0,
        job_name: str = "",
        image_name: str = "",
        disk_size: int = 0,
        scass_type: str = "",
        nnode: int = 0,
        cmd: str = "",
        log_files: List[str] = [],
        out_files: List[str] = [],
        platform: str = "",
        region: str = "",
        zone: str = "",
        on_demand: int = 0,
        checkpoint_time: int = 0,
        checkpoint_files: List[str] = [],
        cli_instance_id: str = "",
        download_path: str = "",
        work_path: str = "",
        job_id: int = 0,
        max_run_time: int = 0,
        client: str = "",
        bohr_job_group_id: int = 0,
        max_reschedule_times: int = 0,
        dataset_path: List[str] = [],
        local_download_path: str = "",
        input_directory: str = "",
        instance_group_id: int = 0,
        input_file_type: int = 2,
        input_file_method: int = 4,
    ):
        self.jobType = job_type
        self.ossPath = oss_path
        self.jobGroupId = job_group_id
        self.projectId = project_id
        self.rerun = rerun
        self.jobName = job_name
        self.imageName = image_name
        self.diskSize = disk_size
        self.scassType = scass_type
        self.nnode = nnode
        self.instanceGroupId = instance_group_id
        self.cmd = cmd
        self.logFiles = log_files  
        self.outFiles = out_files
        self.platform = platform
        self.region = region
        self.zone = zone
        self.onDemand = on_demand
        self.checkpointTime = checkpoint_time
        self.checkpointFiles = checkpoint_files
        self.cliInstanceId = cli_instance_id
        self.downloadPath = download_path
        self.workPath = work_path
        self.jobId = job_id
        self.maxRunTime = max_run_time
        self.client = client
        self.bohrJobGroupId = bohr_job_group_id
        self.inputFileType = input_file_type
        self.inputFileMethod = input_file_method
        self.maxRescheduleTimes = max_reschedule_times
        self.inputDirectory = input_directory
        self.datasetPath = dataset_path
        self.localDownloadPath = local_download_path
        
    def to_dict(self):
        return {
            "jobType": self.jobType,
            "ossPath": [self.ossPath],
            "jobGroupId": self.jobGroupId,
            "projectId": self.projectId,
            "rerun": self.rerun,
            "jobName": self.jobName,
            "imageName": self.imageName,
            "diskSize": self.diskSize,
            "scassType": self.scassType,
            "nnode": self.nnode,
            "instanceGroupId": self.instanceGroupId,
            "cmd": self.cmd,
            "logFiles": self.logFiles,
            "outFiles": self.outFiles,
            "platform": self.platform,
            "region": self.region,
            "zone": self.zone,
            "onDemand": self.onDemand,
            "checkpointTime": self.checkpointTime,
            "checkpointFiles": self.checkpointFiles,
            "cliInstanceId": self.cliInstanceId,
            "downloadPath": self.downloadPath,
            "workPath": self.workPath,
            "jobId": self.jobId,
            "maxRunTime": self.maxRunTime,
            "client": self.client,
            "bohrJobGroupId": self.bohrJobGroupId,
            "inputFileType": self.inputFileType,
            "inputFileMethod": self.inputFileMethod,
            "maxRescheduleTimes": self.maxRescheduleTimes,
            "inputDirectory": self.inputDirectory,
            "datasetPath": self.datasetPath,
            "localDownloadPath": self.localDownloadPath
        }
    
"""


type RequJobDetail struct {
	Code int `json:"code"`
	Data struct {
		Id             int    `json:"id"`
		BohrId         int    `json:"bohrId"`
		ProjectId      int    `json:"projectId"`
		UserId         int    `json:"userId"`
		JobGroupId     int    `json:"jobGroupId"`
		JobGroupName   string `json:"jobGroupName"`
		ThirdpartyId   int    `json:"thirdpartyId"`
		Platform       string `json:"platform"`
		SpendTime      int    `json:"spendTime"`
		Status         int    `json:"status"`
		WebStatus      int    `json:"webStatus"`
		Result         string `json:"result"`
		ResultUrl      string `json:"resultUrl"`
		Cost           string `json:"cost"`
		OnDemand       int    `json:"onDemand"`
		InputData      string `json:"inputData"`
		ErrorInfo      string `json:"errorInfo"`
		CreateTime     string `json:"createTime"`
		UpdateTime     string `json:"updateTime"`
		JobName        string `json:"jobName"`
		ProjectName    string `json:"projectName"`
		UserName       string `json:"userName"`
		EndTime        string `json:"endTime"`
		ImageName      string `json:"imageName"`
		MaxRunTime     int    `json:"maxRunTime"`
		MaxRunTimeUnit string `json:"maxRunTimeUnit"`
		MachineType    string `json:"machineType"`
		Region         string `json:"region"`
		WorkPath       string `json:"workPath"`
		Cmd            string `json:"cmd"`
		JobFiles       struct {
			LogFiles []struct {
				Name       string `json:"name"`
				Url        string `json:"url"`
				UpdateTime string `json:"updateTime"`
				Size       int    `json:"size"`
				SizeH      string `json:"sizeH"`
			} `json:"logFiles"`
			InputFiles []struct {
				Name       string `json:"name"`
				Url        string `json:"url"`
				UpdateTime string `json:"updateTime"`
				Size       int    `json:"size"`
				SizeH      string `json:"sizeH"`
			} `json:"inputFiles"`
			OutFiles []struct {
				Name       string `json:"name"`
				Url        string `json:"url"`
				UpdateTime string `json:"updateTime"`
				Size       int    `json:"size"`
				SizeH      string `json:"sizeH"`
			} `json:"outFiles"`
		} `json:"jobFiles"`
		Machines []struct {
			MachineType string `json:"machineType"`
			Cpu         string `json:"cpu"`
			Memory      string `json:"memory"`
			Gpu         string `json:"gpu"`
			Status      int    `json:"status"`
		} `json:"machines"`
		IsK8S            int      `json:"isK8s"`
		EnableWebShell   int      `json:"enableWebShell"`
		WebShellTag      string   `json:"webShellTag"`
		DownloadPath     string   `json:"downloadPath"`
		OutFile          []string `json:"outFile"`
		AutoDownloadInfo struct {
		} `json:"autoDownloadInfo"`
		Client         int           `json:"client"`
		Metrics        []interface{} `json:"metrics"`
		IsShowMetrics  bool          `json:"isShowMetrics"`
		RunningStartAt int           `json:"runningStartAt"`
		RunningEndAt   int           `json:"runningEndAt"`
		MetricsTag     string        `json:"metricsTag"`
	} `json:"data"`
}
"""

class JobDetailRequest():
    def __init__(
        self,
        id: int,
        bohr_id: int,
        project_id: int,
        user_id: int,
        job_group_id: int,
        job_group_name: str,
        thirdparty_id: int,
        platform: str,
        spend_time: int,
        status: int,
        web_status: int,
        result: str,
        result_url: str,
        cost: str,
        on_demand: int,
        input_data: str,
        error_info: str,
        create_time: str,
        update_time: str,
        job_name: str,
        project_name: str,
        user_name: str,
        end_time: str,
        image_name: str,
        max_run_time: int,
        max_run_time_unit: str,
        machine_type: str,
        region: str,
        work_path: str,
        cmd: str,
        job_files: List[str],
        machines: List[str],
        is_k8s: int,
        enable_web_shell: int,
        web_shell_tag: str,
        download_path: str,
        out_file: List[str],
        auto_download_info: dict,
        client: int,
        metrics: List[dict],
        is_show_metrics: bool,
        running_start_at: int,
        running_end_at: int,
        metrics_tag: str
    ):
        self.id = id
        self.bohr_id = bohr_id
        self.project_id = project_id
        self.user_id = user_id
        self.job_group_id = job_group_id
        self.job_group_name = job_group_name
        self.thirdparty_id = thirdparty_id
        self.platform = platform
        self.spend_time = spend_time
        self.status = status
        self.web_status = web_status
        self.result = result
        self.result_url = result_url
        self.cost = cost
        self.on_demand = on_demand
        self.input_data = input_data
        self.error_info = error_info
        self.create_time = create_time
        self.update_time = update_time
        self.job_name = job_name
        self.project_name = project_name
        self.user_name = user_name
        self.end_time = end_time
        self.image_name = image_name
        self.max_run_time = max_run_time
        self.max_run_time_unit = max_run_time_unit