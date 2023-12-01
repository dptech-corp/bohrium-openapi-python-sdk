import rich
from rich import print
from rich.table import Table
from zipfile import ZipFile
import glob
import os

class Util(object):
    def __init__(self):
        pass

    def nice_print_table(
            self,
            headers: list = [],
            items: list = [],
            env: str = "terminal"
        ) -> None:
        
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        for header in headers:
            table.add_column(header)
        
        for row in items:
            table.add_row(*[str(item) for item in row])
        # if env == "notebook":
        #     console = JupyterConsole()
        #     console.print(table)
        #     display(console) 
        # else:
        print(table)

    @classmethod
    def zip_file_list(cls, root_path, zip_filename, file_list=[]):
        out_zip_file = os.path.join(root_path, zip_filename)
        # print('debug: file_list', file_list)
        zip_obj = ZipFile(out_zip_file, "w")
        for f in file_list:
            matched_files = os.path.join(root_path, f)
            for ii in glob.glob(matched_files):
                # print('debug: matched_files:ii', ii)
                if os.path.isdir(ii):
                    arcname = os.path.relpath(ii, start=root_path)
                    zip_obj.write(ii, arcname)
                    for root, dirs, files in os.walk(ii):
                        for file in files:
                            filename = os.path.join(root, file)
                            arcname = os.path.relpath(filename, start=root_path)
                            # print('debug: filename:arcname:root_path', filename, arcname, root_path)
                            zip_obj.write(filename, arcname)
                else:
                    arcname = os.path.relpath(ii, start=root_path)
                    zip_obj.write(ii, arcname)
        zip_obj.close()
        return out_zip_file


    def unzip_file(zip_file, out_dir="./"):
        obj = ZipFile(zip_file, "r")
        for item in obj.namelist():
            obj.extract(item, out_dir)
            
if __name__ == '__main__':
    headers = [
      "Job ID",
      "Group Name",
      "Job Status",
      "Group ID",
      "Job Groups",
      "Project",
      "Duration",
      "Creation Time",
      "Cost",
      "Submission type"
    ]

    items = [
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
    ]
    util = Util()
    util.nice_print_table(headers=headers, items=items)

    print("asdf")