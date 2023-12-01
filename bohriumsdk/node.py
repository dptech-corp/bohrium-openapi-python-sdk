from bohriumsdk.client import Client
from bohriumsdk.util import Util
class Node:
    def __init__(self, client):
        self.client = client
        

    def list_server(self, project_id):
        self.client.params["projectId"] = project_id
        self.client.params["device"] = "container"
        data = self.client.get('/openapi/v1/node/list', params=self.client.params)
        return data['items']

    def stop(self, machine_id, creator_id):
        data = self.client.post(f'/openapi/v1/node/stop/{machine_id}', data={"creatorId": creator_id}, params=self.client.params)
        return data

    def restart(self, machine_id):
        data = self.client.post(f'/openapi/v1/node/restart/{machine_id}', params=self.client.params)
        return data

    def delete(self, machine_id, creator_id):
        data = self.client.post(f'/openapi/v1/node/del/{machine_id}', data={"creatorId": creator_id}, params=self.client.params)
        return data

    def create(self, image_id, disk_size, memory, cpu, gpu, project_id, name=None):
        post_data = {
            'imageId': image_id,
            'diskSize': disk_size,
            'projectId': project_id,
            'memory': memory,
            'cpu': cpu,
            'gpu': gpu,
            'name': name
        }
        data = self.client.post(f'/openapi/v1/node/add', data=post_data, params=self.client.params)
        return data

    def to_dev_image(self, machine_id, image_name, comment=''):
        post_data = {
            'imageName': image_name,
            'nodeId': machine_id,
            'comment': comment
        }
        data = self.client.post(f'/openapi/v1/image/add', data=post_data, params=self.client.params)
        return data

    def print_node(
            self,
            project_id: int = 0 
        ) -> None:
        data = self.list_server(project_id)
        headers = ['nodeName','ip','nodePwd','cpu','memory','imageName', "cost",  'spec', 'createTime', 'diskSize', 'device']
        items = []
        for row in data:
            i = [row[k] for k in headers]
            items.append(i)
        Util().nice_print_table(headers=headers, items=items)

