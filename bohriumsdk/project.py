
from bohriumsdk.client import Client
from bohriumsdk.util import Util
class Project(object):
    def __init__(
            self, 
            client: Client = None
        ) -> None:
        self.client = client

    def list_project_by_page(
            self,
            page: int = 1,
            per_page: int = 30
        ) -> None:
        host = "https://bohrium.dp.tech"
        # host = "https://openapi.dp.tech/"
        url = "/account/programs"
        params = {
            "page": page,
            "per_page": per_page
        }
        #self.client.token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc2ODE2MTEsImlkZW50aXR5Ijp7Im9yZ0lkIjoxNTcsInVzZXJJZCI6MTU3fSwib3JpZ19pYXQiOjE2ODUwODk2MTF9.OGASZRsHqAKILDSYqyfd76yVktQ8L_oIHFFvWmY54yl7qFaSXXgx6-9_1KoeZG4S36tZFfk8isZaBPpTSTIX6JMkYqdLtxVBGogr4np3hz_ZV8a3set5uTst47Rwa_7Yk1v2iAU4FrghnKemnVu8e4uJSH2pClLgPQVZKF1CZd3AlG55fAvqnzY0-9uiKyBYmfuvUNM1ZlMJXHmFJ400NKZWkZj4iygJ03wGjKBBeXhyIZ4EyIbGrP7683JN2jOyw4wJJISAvKsv_gTNw_mRkdFsZuYx-u19II2UhqCAvMJtwjwgtIY4ReNfEoQPBUJWVyFBi7vaNbkwk-fghr2L0g"
        data = self.client.get(url=url, host=host, params=params)
        return data
    
    def list_all_project(self):
        host = "https://bohrium.dp.tech"
        url = "/brm/v1/project/list"
        params = {
            'page': 1,
            'pageSize': 10000,
            'queryType': 'all'
        }
        data = self.client.get(url=url, host=host, params=params)
        return data["items"]
    
    # 返回data盘大小
    def file_account(self, project_id):
        host = "https://bohrium.dp.tech"
        url = "/brm/v1/file/accounting"
        params = { "projectId": project_id }
        data = self.client.get(url=url, host=host, params=params)
        return data
    
    def print_project(self, env):
        data = self.list_all_project()
        headers = ['id', 'name', 'creatorEmail', 'jobCount', 'nodeCount', 'imageLimit', 'nodeLimit', 'storageLimit', 'storageUsed', 'costLimit', 'totalCost', 'userCost', 'userCostLimit']
        items = []
        for row in data:
            i = [row[k] for k in headers]
            items.append(i)
        Util().nice_print_table(headers=headers, items=items, env=env)

