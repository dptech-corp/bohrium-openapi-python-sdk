
from typing import List, Optional, Literal
class JobAddRequest(object):
    def __init__(
        self, 
        job_type: Literal["container"],
        oss_path: List[str],
        job_group_id: int,
        project_id: int,
        rerun: int,
        job_name: str,
        image_name: str,
        disk_size: int,
        scass_type: str,
        nnode: int,
        instance_group_id: int,
        cmd: str,
        log_files: List[str],
        out_files: List[str],
        platform: str,
        region: str,
        zone: str,
        on_demand: int,
        checkpoint_time: int,
        checkpoint_files: List[str],
        cli_instance_id: str,
        download_path: str,
        work_path: str,
        job_id: int,
        max_run_time: int,
        client: str,
        bohr_job_group_id: int,
        input_file_type: int,
        input_file_method: int,
        max_reschedule_times: int,
        input_directory: str,
        dataset_path: List[str],
        local_download_path: str
    ):
        self.job_type = job_type
        self.oss_path = oss_path
        self.job_group_id = job_group_id
        self.project_id = project_id
        self.rerun = rerun
        self.job_name = job_name
        self.image_name = image_name
        self.disk_size = disk_size
        self.scass_type = scass_type
        self.nnode = nnode
        self.instance_group_id = instance_group_id
        self.cmd = cmd
        self.log_files = log_files  
        self.out_files = out_files
        self.platform = platform
        self.region = region
        self.zone = zone
        self.on_demand = on_demand
        self.checkpoint_time = checkpoint_time
        self.checkpoint_files = checkpoint_files
        self.cli_instance_id = cli_instance_id
        self.download_path = download_path
        self.work_path = work_path
        self.job_id = job_id
        self.max_run_time = max_run_time
        self.client = client
        self.bohr_job_group_id = bohr_job_group_id
        self.input_file_type = input_file_type
        self.input_file_method = input_file_method
        self.max_reschedule_times = max_reschedule_times
        self.input_directory = input_directory
        self.dataset_path = dataset_path
        self.local_download_path = local_download_path
        
        
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