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
    if Configure() != 0:
        exit()
    if BuildProject(sample) != 0:
        exit()     
    if BuildAssetsBatch() != 0:
        exit()
    if RunAssetProcess() != 0:
        exit()
    util.Home()


    
def CollectData(sample):
    util.Chdir(util.JoinPaths(sample["project"], sample["subfolder"], "build", "bin", "profile"))
    cmd = (sample["game_executable"] + ".exe " +  sample["cmd_param"] + " " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/CaptureCount=" + str(sample["frame_count"]) +"\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/IdleCount=" + str(sample["idle_count"]) + "\" " 
        #+
    #    "--regset=\"/O3DE/ScriptAutomation/FrameTime/ViewportWidth=" + str(sample["width"]) + "\" " +
     #   "--regset=\"/O3DE/ScriptAutomation/FrameTime/ViewportHeight=" + str(sample["height"]) + "\" "
     )
    print(cmd)
    ret = util.SafeCall(cmd)
    util.Home()
    return ret

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
    ret = util.SafeCall("git Clone " + sample["url"])
    util.Home()
    return ret

def UpdateSample(sample):
    util.Chdir(util.JoinPaths(sample["project"] ))
    ret = util.SafeCall("git pull")
    util.Home() 
    return ret

def UpdateO3de(settings):
    print(settings)
    print(settings["path_to_o3de"])
    util.Chdir(settings["path_to_o3de"])
    ret = util.SafeCall("git pull")   
    util.Home()
    return ret




def Build(cleanAssets, cleanBuild, build, update, collect, settings):

    samples = settings["samples_to_run"]
    if update:
        UpdateO3de(settings)
        for i in samples:
            UpdateSample(i)
    for i in samples:
        if i["subfolder"] != "":
            if cleanAssets:
                CleanAssets(i)
            if cleanBuild:
                CleanBuild(i)
            if build:
                BuildConfig(i)
            if collect:
                if CollectData(i) != 0:
                    exit()
                if CopyData(i) != 0:
                    exit()


if __name__ == '__main__': 
    Build(True, True, True, True, True)



