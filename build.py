"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
settings = ""

def buildassetsbatch():
    return util.safe_call("cmake --build build --target AssetProcessorBatch --config profile -- /m")


def configure():
    return util.safe_call("cmake -B build -G \"Visual Studio 16 2019\"")

def buildproject(sample):
    return util.safe_call("cmake --build build --target Editor " + sample["GameExecutable"] + " --config profile -- /m")

def runassetprocess():
    return util.safe_call("build/bin/profile/AssetProcessorBatch.exe")

def build_config(sample):
    util.safe_call("pwd")
    util.chdir(util.join_paths("../", 
                          sample["project"],
                          sample["subfolder"]))  

    config = configure()
    if config != 0:
        exit()
    edit_exe = buildproject(sample) 
    if edit_exe != 0:
        exit()     
    apbatch = buildassetsbatch()
    if apbatch != 0:
        exit()
    util.home()


    
def collect_data(sample):
    #util.safe_call("benchmark.lua")
    util.safe_call("pwd")
    util.chdir(util.join_paths("..", sample["project"], sample["subfolder"], "build", "bin", "profile"))
    util.safe_call("pwd")
    cmd = sample["GameExecutable"] + ".exe " +  sample["cmdparam"]
    print(cmd)
    util.safe_call(cmd)
    util.home()

def copy_data(sample):
    data = util.process_data(sample)
    util.add_row_csv(sample, data)

def cleanbuild(sample):
    #delete build folder
    util.chdir(util.join_paths("..", sample["project"], sample["subfolder"]))
    util.safe_call("rm -rf build")
    util.home()

def cleanassets(sample):
    #delete cache and user folder
    util.chdir(util.join_paths("..", sample["project"], sample["subfolder"]))
    util.safe_call("rm -rf Cache")
    util.safe_call("rm -rf user")
    util.home()

def clone(sample):
    util.chdir("..")
    util.safe_call("git clone " + sample["url"])
    util.home()

def update(sample):
    util.chdir(util.join_paths("..", sample["project"] ))
    util.safe_call("git pull")
    util.home()    



settings = util.settings
samples = settings["SAMPLES_TO_RUN"]

def build():
    for i in samples:
        #build_config(i)
        #collect_data(i)
        copy_data(i)


