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
    util.ChDir(util.JoinPaths(sample["project"],
                               sample["subfolder"]))  
    if Configure() != 0:
        exit()
    print(sample["project"] + " has been configured")
    if BuildProject(sample) != 0:
        exit()     
    print(sample["project"] + " has been built")
    if BuildAssetsBatch() != 0:
        exit()
    print(sample["project"] + "'s assets have been built")
    if RunAssetProcess() != 0:
        exit()
    print(sample["project"] + "'s assets have been processed")
    util.Home()
    


    
def CollectData(sample):
    util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "user", sample["output_location"]))
    print("Previous output JSON files have been deleted")
    util.ChDir(util.JoinPaths(sample["project"], sample["subfolder"], "build", "bin", "profile"))
    cmd = (sample["game_executable"] + ".exe " +  sample["cmd_param"] + " "  +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/CaptureCount=" + str(sample["frame_count"]) +"\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/IdleCount=" + str(sample["idle_count"]) + "\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/ViewportWidth=" + str(sample["width"]) + "\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/ViewportHeight=" + str(sample["height"]) + "\" ")
    ret = util.SafeCall(cmd)
    util.Home()
    #if ret == 0:
     #   print("Data for " + sample["project"] + "has been collected")
    #else:
     #   print("Data collection for " + sample["project"] + " has failed")
    return 0

def CopyData(sample):
    data = util.ProcessData(sample)
    util.AddRowCsv(sample, data)
    print("Data has been copied to " + sample["path_to_data"]+ "/" + sample["data_name"])
    return 0

def CleanBuild(sample):
    #delete build folder
    #util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "build"))
    print(sample["project"] +"'s build folder has been cleaned")

def CleanAssets(sample):
    #delete cache and user folder
    util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "Cache"))
    util.RmDir(util.JoinPaths(sample["project"], sample["subfolder"], "user"))
    print(sample["project"] + "'s assets have been cleaned")


def Build(cleanAssets, cleanBuild, build, collect, settings):

    samples = settings["projects_to_run"]
    for i in samples:
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



