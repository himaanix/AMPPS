
"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
settings = ""

def ConfigureProjectCentric() -> int:
    """
    @returns 0 if configured successfully, errorcode if not successful
    """
    return util.SafeCall("cmake -B build -G \"Visual Studio 16 2019\"")

def BuildProject(sample: dict) -> int:
    """
    @returns 0 if project built successfully, errorcode if not successful
    """
    return util.SafeCall("cmake --build build --target Editor " + sample["game_executable"] + " --config profile -- /m")

def BuildAssetsBatch() -> int:
    """
    @returns 0 if AssetProcessorBatch built successfully, errorcode if not successful
    """
    return util.SafeCall("cmake --build build --target AssetProcessorBatch --config profile -- /m")

def RunAssetProcess() -> int:
    """
    @returns 0 if Assets Processed successfully, errorcode if not successful
    """
    return util.SafeCall("build/bin/profile/AssetProcessorBatch.exe")

def BuildConfigProjectCentric(sample:dict, ignoreerrors:bool):
    """
    @param sample This is the dictionary of the project
    @param ignoreerrors Boolean to continue with script if there are errors
    Exits script if any errors during build and configure
    """
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

def ConfigureEngineCentric(settings:dict) -> int:
    """
    @param settings Settings file
    @returns 0 if configured successfully, errorcode if not successful
    """
    projectstring = ""
    for i in settings["projects_to_run"]:
        projectstring = projectstring + i["project"] + ";"
    projectstring = projectstring[:-1]
    return util.SafeCall("cmake -B build -G \"Visual Studio 16 2019\" -DLY=" + projectstring)

def BuildProjects(settings:dict) -> int:
    """
    @param settings Settings file
    @returns 0 if projects built successfully, errorcode if not successful
    """
    projectstring = ""
    for i in settings['projects_to_run']:
        projectstring = projectstring + i["game_executable"] + " "
    return util.SafeCall("cmake --build build --target Editor " + projectstring + "--config profile -- /m")

def RunAssetProcessEngineCentric(settings:dict, ignoreerrors:bool) -> int:
    """
    @param settings Settings file
    @param ignoreerrors Boolean to continue with script if there are errors
    @returns 0 if Assets processed successfully, errorcode if not successful
    """
    for i in settings["projects_to_run"]:
        absolutepath = util.GetAbsPath(util.JoinPaths(i['project'],i['subfolder']))
        return (util.SafeCall("build/bin/profile/AssetProcessorBatch.exe --project-path=\"" + absolutepath + "\"")) != 0 and (not ignoreerrors)

def BuildConfigEngineCentric(settings:dict, ignoreerrors:bool, pathtobuild:str):
    """
    @param sample This is the dictionary of the project
    @param ignoreerrors Boolean to continue with script if there are errors
    @param pathtobuild This is the path to the projectcentric build
    Exits script if any errors during build and configure
    """
    util.ChDir(pathtobuild)
    if ConfigureEngineCentric(settings) !=0 and (not ignoreerrors):
        exit()
    if BuildProjects(settings) !=0 and (not ignoreerrors):
        exit()
    if BuildAssetsBatch() !=0 and (not ignoreerrors):
        exit()
    if (RunAssetProcessEngineCentric(settings,ignoreerrors)) !=0 and (not ignoreerrors):
        exit()
    util.Home()


def CleanBuild(pathtobuild:str):
    """
    @param pathtobuild This is the path to the folder in which the build folder is located
    Deletes the build folder
    """
    pathtobuild = util.JoinPaths(path_to_build, "build")
    util.RmDir(pathtobuild)
    print(sample["project"] +"'s build folder has been cleaned")

def CleanAssets(pathtobuild:str): #this is wrong need to be fixed
    """
    @param pathtobuild This is the path to the folder in which the build folder is located
    Deletes user and cache folder 
    """
    util.RmDir(util.JoinPaths(pathtobuild, "Cache"))
    util.RmDir(util.JoinPaths(pathtobuild, "user"))
    print(sample["project"] + "'s assets have been cleaned")

   
def PCentric(cleanAssets:bool, cleanBuild:bool, build:bool, settings:dict, ignoreerrors:bool): 
    """
    @param cleanAssets Boolean to determine if Assets should be cleaned
    @param cleanBuild Boolean to determine if build folder should be cleaned
    @param build Boolean to determine if projects should be built
    @param settings settings file
    @param ignoreerrors Boolean to determine if script should continue despite errors
    Builds in Project Centric Approach
    """ 
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

def ECentric(cleanAssets:bool, cleanBuild:bool, build:bool, settings:dict, ignoreerrors:bool, pathtobuild:str):
    """
    @param cleanAssets Boolean to determine if Assets should be cleaned
    @param cleanBuild Boolean to determine if build folder should be cleaned
    @param build Boolean to determine if projects should be built
    @param settings settings file
    @param ignoreerrors Boolean to determine if script should continue despite errors
    @param pathtobuild path to engine centric build
    Builds in Engine Centric Approach
    """ 
    if cleanAssets:
        cleanAssets(pathtobuild)
    if cleanBuild:
        CleanBuild(pathtobuild)
    if build:
        BuildConfigEngineCentric(settings,ignoreerrors,pathtobuild)

def Build(cleanAssets:bool, cleanBuild:bool, build:bool, settings:dict, ignoreerrors:bool, enginecentric:str):
    """
    @param cleanAssets Boolean to determine if Assets should be cleaned
    @param cleanBuild Boolean to determine if build folder should be cleaned
    @param build Boolean to determine if projects should be built
    @param settings settings file
    @param ignoreerrors Boolean to determine if script should continue despite errors
    @param enginecentric path to engine centric build if it exists
    """ 
    if enginecentric == "":
        PCentric(cleanAssets,cleanBuild,build, settings, ignoreerrors)
    else:
        ECentric(cleanAssets,cleanBuild, build, settings, ignoreerrors, enginecentric)


def CollectData(sample:dict, ignoreerrors:bool) -> int:
    """
    @param sample dictionary of project
    @param ignoreerrors boolean to determine if script should continue if errors
    @returns 0 if collection successful return code if not
    """
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
    else:
        print("Data collection for " + sample["project"] + " has failed")
    return ret


def CopyData(sample:dict,annotation:str):
    """
    @param sample dictionary of project
    @param annotation string to label dataset
    Copies Data into CSV
    """
    data = util.ProcessData(sample, annotation)
    util.AddRowCsv(sample, data, annotation)
    print("Data has been copied to " + sample["path_to_data"]+ "/" + sample["data_name"])

def Collect( annotation:str, settings:dict, ignoreerrors:bool):
    """
    @param annotation string to label dataset
    @param settings settings file
    @param ignoreerrors boolean to determine if script should continue despite errors
    """
    for i in settings["projects_to_run"]:
        if "path_to_build" not in i:
            i["path_to_build"] = util.JoinPaths(i["project"], i["subfolder"])
        if CollectData(i,ignoreerrors) != 0:
            exit()
        if CopyData(i, annotation) != 0:
            exit()


if __name__ == '__main__': 
    Build(False, False, True, "settings.json", False, False)
    Collect( "", "settings.json", False)


