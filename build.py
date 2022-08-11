"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
settings = ""

def BuildAssetsBatch():
    return util.SafeCall("cmake --build build --target AssetProcessorBatch --config profile -- /m")

def Configure():
    return util.SafeCall("cmake -B build -G \"Visual Studio 16 2019\"")

def BuildProject(sample):
    return util.SafeCall("cmake --build build --target Editor " + sample["game_executable"] + " --config profile -- /m")

def RunAssetProcess():
    return util.SafeCall("build/bin/profile/AssetProcessorBatch.exe")

def BuildConfig(sample):
    util.Chdir(util.JoinPaths(sample["project"],
                               sample["subfolder"]))  
    config = Configure()
    if config != 0:
        exit()
    editExe = BuildProject(sample) 
    if editExe != 0:
        exit()     
    apBatch = BuildAssetsBatch()
    if apBatch != 0:
        exit()
    if RunAssetProcess() != 0:
        exit()
    util.Home()


    
def CollectData(sample):
    util.SafeCall("pwd")
    util.Chdir(util.JoinPaths(sample["project"], sample["subfolder"], "build", "bin", "profile"))
    cmd = sample["game_executable"] + ".exe " +  sample["cmd_param"]
    print(cmd)
    util.SafeCall("pwd")
    util.SafeCall(cmd)
    util.Home()

def CopyData(sample):
    data = util.ProcessData(sample)
    util.AddRowCsv(sample, data)

def CleanBuild(sample):
    #delete build folder
    util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "build"))

def CleanAssets(sample):
    #delete cache and user folder
    util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "Cache"))
    util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "user"))

def Clone(sample):
    util.Chdir("..")
    util.SafeCall("git Clone " + sample["url"])
    util.Home()

def UpdateSample(sample):
    util.Chdir(util.JoinPaths(sample["project"] ))
    util.SafeCall("git pull")
    util.Home() 

def UpdateO3de():
    util.Chdir(settings["path_to_o3de"])
    util.SafeCall("git pull")   
    util.Home()




def Build(cleanAssets, cleanBuild, build, update, collect, settings):

    samples = settings["samples_to_run"]
    if update:
        UpdateO3de()
        for i in samples:
            UpdateSample(i)
    for i in samples:

        if cleanAssets:
            CleanAssets(i)
        if cleanBuild:
            CleanBuild(i)
        if build:
            BuildConfig(i)
        if collect:
            CollectData(i)
            CopyData(i)


if __name__ == '__main__': 
    Build(True, True, True, True, True)



