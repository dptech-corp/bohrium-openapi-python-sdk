
from client import Client
from image import Image
from job import Job
from storage import Storage
from project import Project
from util import Util
from node import Node
from database import Database
import os, sys

def test_image():
    c = Client()
    c.login()
    i = Image(c)
    res = i.list_image_by_page(project_id=154)
    #print(res["items"][0].keys())
    i.print_image(154)


def test_job():
    c = Client()
    # c.login()
    # print(c.token)
    # ak = c.generate_access_key("ak")
    # print(ak)
    j = Job(c)
    s = Storage(client = c)
    #data = j.detail()
    #print(j.log(10009242))
    data = j.create(project_id=154, name="test-env-job")

    # print(data)
    file_path = "/Users/dingzhaohan/Downloads/out.zip"
    file_name = os.path.basename(file_path)
    token = data["token"]
    print(data)
    #print(j.list_by_page(job_group_id=2107148))
    jid = data["jobId"]
    # j.get_job_token(jid)
    object_key = os.path.join(data["storePath"], file_name)
    print(object_key)
    res = s.upload_From_file_multi_part(object_key=object_key, file_path=file_path,  token=token, progress_bar=True)
    #res = s.upload_from_file(object_key=object_key, file_path=file_path, token=token)
    # s.download_from_file()

    #res = s.read(object_key=res["path"], token=token)
    #print(res)

    data = {
        "oss_path": object_key,
        'input_file_type': 3,
        'input_file_method': 1,
        "job_type": "container",
        "job_name": "test-name",
        "project_id": 154,
        "scass_type": "c2_m4_cpu",
        "cmd": "echo 1asdfasdfasdfasdfasdfasdfasdf11 >> test.result;",
        "log_files": ["test.result"],
        "out_files": ["test.result"],
        "platform": "ali",
        "image_address": "registry.dp.tech/dev/test/ubuntu:20.04-py3.10",
        "job_id": jid
    }
    j.insert(**data)
    #print(a["items"][0].keys())

def test_job_detail():
    c = Client()
    j = Job(client=c)
    data = j.detail(10059657)
    print(data["status"])

def test_node():
    c = Client()
    node = Node(c)
    node.print_node(154)
    # data = node.list_server(154)
    # print(data)
    # headers = data[0].keys()
    # print(list(headers))
    # headers = ['nodeName','ip','nodePwd','cpu','memory','imageName', "cost",  'spec', 'createTime', 'diskSize', 'device']
    # items = []
    # for i in data:
    #     tmp_data = []
    #     # tmp_data = list(i.values())
    #     for k in headers:
    #         tmp_data.append(i[k])
    #     #print(tmp_data)
    #     items.append(tmp_data)
    # u = Util()
    # u.nice_print_table(headers=headers, items=items)

def test_project():
    c = Client()
    c.login()
    p = Project(client=c)
    p.print_project()

def test_storage():
    c = Client()
    j = Job(client=c)
    s = Storage(client = c)

    resp = j.create(project_id=154, name="upload_test")
    file_path = "/Users/dingzhaohan/Desktop/Bohrium_CALYPSO_example.zip"
    file_name = os.path.basename(file_path)
    token = resp["token"]
    object_key = os.path.join(resp["storePath"], file_name)

    res = s.upload_From_file_multi_part(file_path=file_path, object_key=object_key, token=token)
    #res = s.upload_from_file(object_key=object_key, file_path=file_path, token=token)
    print(res)
    # filename = "a.txt"
    # object_key = os.path.join(resp["storePath"], filename)
    #
    # print(resp)
    # param = Parameter()
    # param.userMeta = {
    #         "a": "b",
    #         "ever":"17"
    #     }
    # param.contentType = "text/plain"
    # param.contentDisposition = f"attachment; filename={filename}"
    # param.filename = filename
    # res = s.write(object_key=object_key, data="1231231231231", token=token, parameter=param)
    # print(res)

    res = s.read(object_key=res["path"], token=token)
    print(res)

def test_base64():
    encode_data = "eyJhcHBLZXkiOiJib2hyLXRlc3QiLCJ0YWciOiJjbG91ZCIsInJlc291cmNlcyI6W3siUHJlZml4IjoiMTU3L2pvYi8yMDEzNDE0NS9pbnB1dC8iLCJBY3Rpb24iOjE1fV0sInByZWRlZmluZWRNZXRhIjpudWxsLCJleHAiOjE2ODYyNzQxOTl9"
    c = Client()
    s = Storage(c)
    decode = s.decode_base64(encode_data=encode_data)
    print(decode)

def test_db():
    db = Database()
    db.init_db()
    db.insert_record(1,1,"/home/test", "abcd")
    db.insert_record(2,1,"/home/test", "abcd")
    db.get_all_record()
    db.get_record(2)
    db.update_record(2,1,"/root/test", "aaaaaa")
    db.get_record(2)
    db.delete_record(2)
    db.get_all_record()


def test_chat():

    c = Client()
    prompt = "你好"
    res = c.chat(prompt)
    print(res)


if __name__ == "__main__":
    # test_chat()
    test_job_detail()
    # test_base64()
    # test_db()
