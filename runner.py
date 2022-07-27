"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
settings = ""


def build_config(sample):
    util.change_dir(util.join_paths("../", 
                          sample["project"],
                          sample["subfolder"]))
    config = util.safe_call("cmake -B build -G \"Visual Studio 16 2019\"")
    edit_exe = util.safe_call("cmake --build build --target Editor " + sample["GameExecutable"] +" --config profile -- /m")
    if edit_exe != 0:
        return edit_exe
    apbatch = util.safe_call("cmake --build build --target AssetProcessorBatch --config profile -- /m")
    if apbatch != 0:
        return apbatch
    util.safe_call("build/bin/profile/AssetProcessorBatch.exe")
    

    
def collect_data(sample):
    util.safe_call(util.join_paths("build/bin/profile/",
                           sample["GameExecutable"],
                           sample["cmdparam"]))

def copy_data(sample):
    data = util.process_data(sample)
    print(data)
    util.add_row_csv(data)

def test(sample):
    util.get_row_csv(sample, 0)




    



settings = util.settings
samples = settings["SAMPLES_TO_RUN"]
for i in samples:
    
    test(i)







