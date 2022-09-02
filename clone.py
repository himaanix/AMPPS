"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
import os
import subprocess
import string
import json

def Clone(path:str, url:str) -> int:
    """
    @param path path to the repository
    @param url url of repository
    @returns 0 if successful return code if not
    Clones repository at given path
    """
    ret = util.SafeCall("git clone" + url + " " + path)
    print(url + " has been cloned at " + path)
    return ret

def RepExists(path:str, url:str) -> bool:
    """
    @param path path where repository should exits
    @param url url of repository
    @returns True if repository exists, False if not
    """
    if os.path.exists(path):
        util.ChDir(path)
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
            util.Home()
            return False
        for i in fetchs:
            if url in i:
                print("The project exists")
                util.Home()
                return True
        print("A different repository is cloned at the given project path. Please provide an different path")
        exit()
    else:
        return True

def SetupEngine(path:str):
    """
    @param path path to engine
    Sets up engine by installing gif lfs and registering engine
    """
    util.ChDir(path)
    if util.SafeCall("git lfs install") != 0:
        exit()
    enginefile = util.ProcessJson('engine.json')
    enginefile["engine_name"] = "o3de_AMPPS"
    json.dump(enginefile, open('engine.json', 'w'), indent=4)
    if util.SafeCall("scripts\o3de.bat register --this-engine") != 0:
        exit()

def SetupProject(sample:dict):
    """
    @param sample dictionary of project
    Sets up project by installing git lfs and changing engine name
    """
    util.ChDir(sample["project"])
    if util.SafeCall("git lfs install") != 0:
        exit()
    projectfile = util.ProcessJson('project.json')
    projectfile['engine'] = 'o3de_AMPPS'
    json.dump(projectfile, open('engine.json', 'w'), indent=4)
    return 0

def Branch(sample:dict):
    """
    @param sample dictionary of project
    Switches branch to the one in the dictionary
    """
    util.ChDir(sample["project"])
    try:
        call = subprocess.run("git remote --v", capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f'Command "{cmdString}" failed with returncode {hex(e.returncode)}')
        return e.returncode
    output = call.stdout
    output = output.decode("utf-8")
    util.Home()
    if 'fatal' in output:
        print('branch does not exist')
        exit()

def UpdateSample(sample:dict) -> int:
    """
    @param sample dictionary of project
    git pulls on repository of project
    """
    util.ChDir(util.JoinPaths(sample["project"], sample["subfolder"]))
    ret = util.SafeCall("git pull")
    util.Home()
    if ret == 0:
        print(sample["project"] + " has been updated")
    return ret

def UpdateO3de(settings:dict) -> int:
    """
    @param settings settings file
    git pulls on repository of o3de
    """
    util.ChDir(settings["path_to_o3de"])
    ret = util.SafeCall("git pull")   
    util.Home()
    if ret == 0:
        print("O3DE has been updated")
    return ret

def Manage(update:bool,settings:dict):
    """
    @param update boolean to determine whether or not to update
    @param settings settings file
    """
    samples = settings["projects_to_run"]
    if not RepExists(settings["path_to_o3de"], settings["o3de_url"]):
        clone(settings["path_to_o3de"], settings["o3de_url"])
    SetupEngine(settings["path_to_o3de"])
    if update:
        UpdateO3de(settings)
        print("Updated O3DE")
    for i in samples:
        if not RepExists(i["project"], i["url"]):
            if Clone(i) == 0:
                print("The project " + i["project"] + " has been cloned")
                SetupProject(i)
            else:
                print("Error in cloning repository " + i["url"])
                exit()
        if update:
            UpdateSample(i)
        Branch(i)