"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import util
import os
import subprocess

def Clone(sample):
    util.ChDir(sample["project"])
    ret = util.SafeCall("git Clone " + sample["url"])
    util.Home()
    print(sample["project"] + " has been cloned")
    return ret

def Exists(sample):
    if os.path.exists(sample["project"]):
        try:
            call = subprocess.check_call("git remote --v")
        except subprocess.CalledProcessError as e:
            print(f'Command "{cmdString}" failed with returncode {hex(e.returncode)}')
            return e.returncode
         print(call.stdout)
        #fetch does not match url
    else:
        Clone(sample)