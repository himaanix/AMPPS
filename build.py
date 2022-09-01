
"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
settings = ""

def BuildAssetsBatch():
    return util.SafeCall("cmake --build build --target AssetProcessorBatch --config profile -- /m")

def ConfigureProjectCentric():
    return util.SafeCall("cmake -B build -G \"Visual Studio 16 2019\"")

def BuildProject(sample):
    return util.SafeCall("cmake --build build --target Editor " + sample["game_executable"] + " --config profile -- /m")

def RunAssetProcess():
    return util.SafeCall("build/bin/profile/AssetProcessorBatch.exe")

def BuildConfigProjectCentric(sample, ignoreerrors):
    util.ChDir(sample["path_to_build"]) 
    if ConfigureProjectCentric() != 0 or ignoreerrors:
        exit()
    print(sample["project"] + " has been configured")
    if BuildProject(sample) != 0 or ignoreerrors:
        exit()     
    print(sample["project"] + " has been built")
    if BuildAssetsBatch() != 0 or ignoreerrors:
        exit()
    print(sample["project"] + "'s assets have been built")
    if RunAssetProcess() != 0 or ignoreerrors:
        exit()
    print(sample["project"] + "'s assets have been processed")
    util.Home()

def ConfigureEngineCentric(settings):
    projectstring = ""
    for i in settings["projects_to_run"]:
        projectstring = projectstring + i["project"] + ";"
    projectstring = projectstring[:-1]
    return util.SafeCall("cmake -B build -G \"Visual Studio 16 2019\" -DLY=" + projectstring)

def BuildProjects(settings):
    projectstring = ""
    for i in settings['projects_to_run']:
        projectstring = projectstring + i["game_executable"] + " "
    return util.SafeCall("cmake --build build --target Editor " + projectstring + "--config profile -- /m")

def RunAssetProcessEngineCentric(settings, ignoreerrors):
    for i in settings["projects_to_run"]:
        absolutepath = util.GetAbsPath(util.JoinPaths(i['project'],i['subfolder']))
        return (util.SafeCall("build/bin/profile/AssetProcessorBatch.exe --project-path=\"" + absolutepath + "\"")) != 0 and (not ignoreerrors)

def BuildConfigEngineCentric(settings, ignoreerrors):
    util.ChDir(settings["path_to_o3de"])
    if ConfigureEngineCentric(settings) !=0 and (not ignoreerrors):
        exit()
    if BuildProjects(settings) !=0 and (not ignoreerrors):
        exit()
    if BuildAssetsBatch() !=0 and (not ignoreerrors):
        exit()
    if (RunAssetProcessEngineCentric(settings,ignoreerrors)) !=0 and (not ignoreerrors):
        exit()
    print(":)")
    util.Home()


    
def CollectData(sample, ignoreerrors):
    pathToOutput = util.JoinPaths(sample["project"], sample["subfolder"], "user", "scriptautomation", "profiling", sample["profile_name"])
    #if os.path.exists(pathToOutput):
     #   util.RmDir(pathToOutput)
      #  print("Previous output JSON files have been deleted")
    pathtobuild = util.JoinPaths(sample["path_to_build"], "build", "bin", "profile")
    print(pathtobuild)
    util.ChDir(pathtobuild)
    cmd = (sample["game_executable"] + ".exe " +  sample["cmd_param"] + " "  +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/ProfileName=" + sample["profile_name"] + "\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/CaptureCount=" + str(sample["frame_count"]) +"\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/IdleCount=" + str(sample["idle_count"]) + "\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/ViewportWidth=" + str(sample["width"]) + "\" " +
        "--regset=\"/O3DE/ScriptAutomation/FrameTime/ViewportHeight=" + str(sample["height"]) + "\" ")
    ret = util.SafeCall(cmd)
    util.Home()
    if ret == 0 or ret ==  3221225477 or ignoreerrors:
        print("Data for " + sample["project"] + "has been collected")
        return 0
    else:
        print("Data collection for " + sample["project"] + " has failed")
        return

def CopyData(sample,annotation):
    data = util.ProcessData(sample, annotation)
    util.AddRowCsv(sample, data, annotation)
    print("Data has been copied to " + sample["path_to_data"]+ "/" + sample["data_name"])
    return 0

def CleanBuild(pathtobuild):
    pathtobuild = util.JoinPaths(path_to_build, "build")
    util.RmDir(pathtobuild)
    print(sample["project"] +"'s build folder has been cleaned")

def CleanAssets(pathtobuild):
    util.RmDir(util.JoinPaths(pathtobuild, "Cache"))
    util.RmDir(util.JoinPaths(pathtobuild, "user"))
    print(sample["project"] + "'s assets have been cleaned")


def Build(cleanAssets, cleanBuild, build, settings, ignoreerrors, enginecentric):
    if enginecentric:
        ECentric(cleanAssets,cleanBuild,build, settings, ignoreerrors)
    else:
        PCentric(cleanAssets,cleanBuild, build, settings, ignoreerrors)
   
def PCentric(cleanAssets, cleanBuild, build, settings, ignoreerrors):  
    samples = settings["projects_to_run"]
    for i in samples:
        if "path_to_build" not in i:
            i["path_to_build"] = util.JoinPaths(i["project"], i["subfolder"])
        if cleanAssets:
            CleanAssets(i["path_to_build"])
        if cleanBuild:
            CleanBuild(i["path_to_build"])
        if build:
            BuildConfigProjectCentric(i, ignoreerrors)

def ECentric(cleanAssets,cleanBuild, build, settings, ignoreerrors):
    if cleanAssets:
        cleanAssets(settings["path_to_o3de"])
    if cleanBuild:
        CleanBuild(settings["path_to_o3de"])
    if build:
        BuildConfigEngineCentric(settings,ignoreerrors)

def Collect(collect, annotation, settings, ignoreerrors):
    for i in settings["projects_to_run"]:
        if CollectData(i,ignoreerrors) != 0:
            exit()
        if CopyData(i, annotation) != 0:
            exit()


if __name__ == '__main__': 
    Build(False, False, True, "settings.json", False, False)
    Collect(True, "", "settings.json", False)


