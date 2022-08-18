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
    util.ChDir(sample["project"])
    ret = util.SafeCall("git Clone " + sample["url"])
    #git lfs
    util.Home()
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
        for i in fetchs:
            print(i)
            print(sample["url"])
            if sample["url"] in i:
                return 0
        #clone the repository
    else:
        #create the folder
        #clone the repository
        print("the project exists or has been cloned")

def Branch(sample):
    return 0

def UpdateSample(sample):
    util.ChDir(util.JoinPaths(sample["project"] ))
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

def Mangage(update)

    for i in samples:
        print(i)
        RepExists(i)
        #if it already exists update
            if update:
            UpdateO3de(settings)
            for i in samples:
                UpdateSample(i)