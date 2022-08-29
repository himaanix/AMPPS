"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
import os
import subprocess
import string

def Clone(sample):
    ret = util.SafeCall("git clone" + sample["url"] + " " + sample["project"])
    Setup(sample)
    print(sample["project"] + " has been cloned")
    return ret

def RepExists(sample):
    if os.path.exists(sample["project"]):
        util.ChDir(sample["project"])
        try:
            call = subprocess.run("git remote --v", capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f'Command "{cmdString}" failed with returncode {hex(e.returncode)}')
            return e.returncode
        urls = call.stdout
        urls = urls.decode("utf-8")
        urls = urls.splitlines()
        print(urls)
        fetchs = []
        for i in urls:
            if " (fetch)" in i:
                fetchs.append(i)
        print(fetchs)
        if fetchs == []:
            #the folder exists but no repository
            if Clone(sample) == 0:
                print("The project has been cloned")
                util.Home()
                return True
            else:
                print("Error in cloning repository")
                util.Home()
                return False
        for i in fetchs:
            print(i)
            print(sample["url"])
            if sample["url"] in i:
                print("The project exists")
                util.Home()
                return True
        print("A different repository is cloned at the given project path. Please provide an different path")
        util.Home()
        return False
    else:
        Clone(sample)
        print("The project has been cloned")
        util.Home()
        return True

def Setup(sample):
    #git lfs
    #register engines
    #change project.json to new engine
    return 0

def Branch(sample):
    #check if given branch is valid
    #if valid switch
    #if not valid create new branch and switch
    return 0

def UpdateSample(sample):
    util.ChDir(util.JoinPaths(sample["project"], sample["subfolder"]))
    ret = util.SafeCall("git pull")
    util.Home()
    if ret == 0:
        print(sample["project"] + " has been updated")
    return ret

def UpdateO3de(settings):
    print(settings)
    print(settings["path_to_o3de"])
    util.ChDir(settings["path_to_o3de"])
    ret = util.SafeCall("git pull")   
    util.Home()
    if ret == 0:
        print("O3DE has been updated")
    return ret

settings = util.ProcessJson('settings.json')
samples = settings["projects_to_run"]

def Manage(update):
    for i in samples:
        print(i)
        if RepExists(i):
            if update:
                UpdateO3de(settings)
                for i in samples:
                    UpdateSample(i)
        else:
            print("The project could not be cloned")
