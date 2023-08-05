import subprocess
from codegenhelper import debug

def cmd(command, cwd):
    p = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE)
    return p.communicate()

def has_uncommit(project_folder):
    return str(cmd("git status", project_folder)[0]).find("working directory clean") == -1
