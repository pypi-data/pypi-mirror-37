import nodejs_codegen 
from .download import getJson
from .githelper import has_uncommit
from codegenhelper import put_folder, debug
import os
def run(root, url, username = None, password = None):
    def gen_code(app_data, project_folder):
        debug(project_folder, "project_folder")
        if len(os.listdir(project_folder)) == 0 or not has_uncommit(project_folder):
            nodejs_codegen.run(app_data, project_folder)
        else:
            raise ValueError("the git is not configured or there is uncommitted changes in %s" % project_folder)
            
    (lambda folder_path: \
     [gen_code(debug(app_data, "app_data"), \
          put_folder(app_data["deployConfig"]["instanceName"], folder_path)) for app_data in debug(getJson(url, username, password), "getJson result")])(put_folder(root))
