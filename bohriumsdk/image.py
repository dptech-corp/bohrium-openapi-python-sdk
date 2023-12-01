from bohriumsdk.client import Client
from bohriumsdk.util import Util

class Image(object):
    def __init__(
            self, 
            client: Client = None
        ) -> None:
        self.client = client

    def list_image_by_page(
            self, 
            project_id: int = 1, 
            kind=None, 
            page=1, 
            per_page=30
        ) -> None:
        params = {
            'page': page, 
            'pageSize': per_page, 
            'projectId': project_id, 
            "type": "private"
        }
        if kind is not None:
            params['kind'] = kind
        url = '/brm/v1/image/list'
        host = "https://bohrium.dp.tech"
        data = self.client.get(host=host, url=url, params=params)
        #print(data)
        return data
    
    def list_all_image(self, project_id, kind=None):
        project_list = []
        data = self.list_image_by_page(project_id=project_id, kind=kind)
        total = data['total']
        per_page = data['pageSize']
        page_number = 0
        while page_number * per_page < total:
            page_number = page_number + 1
            if page_number > 1:
                data = self.list_image_by_page(project_id=project_id, kind=kind, page=page_number, per_page=30)
            project_list.extend(data['items'])
        return project_list


    def delete(self, image_id):
        host = "https://bohrium.dp.tech"
        url = f'/brm/v1/image/del/{image_id}'
        data = self.client.get(host=host, url=url)
        
        return data

    def print_image(
            self,
            project_id: int = 0 
        ) -> None:
        data = self.list_all_image(project_id)
        headers = ['imageName','createTime', "creatorName",  'diskSize', 'projectRole', 'status']
        items = []
        for row in data:
            i = [row[k] for k in headers]
            items.append(i)
        Util().nice_print_table(headers=headers, items=items)

    

    