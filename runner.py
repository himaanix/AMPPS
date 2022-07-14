"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import logging
import os
import subprocess
import json
logger = logging.getLogger(__name__)
settings = ""

class PerformanceTestingException(Exception):
    """ Custom Exception class for performance testing """
    pass

def process_settings():
    f = open('settings.json')
    return json.load(f)
    
    

def safe_call(command, **kwargs):
    """
    Method adapted from Lumberyard Utilities
    
    Forwards arguments to subprocess.check_call so better error messages can be displayed upon failure.
    This function eats the subprocess.CalledProcessError exception upon command failure and returns the exit code.

    :param command: A list of the command to execute and its arguments as if split by whitespace.
    :param kwargs: Keyword args forwarded to subprocess.check_call.
    :return: An exitcode of 0 if the call succeeds, otherwise the exitcode returned from the failed subprocess call.
    """
    cmd_string = command
    if type(command) == list:
        cmd_string = ' '.join(command)

    logger.info(f'Executing "check_call({cmd_string})"')
    try:
        subprocess.check_call(command, **kwargs)
    except subprocess.CalledProcessError as e:
        logger.warning(f'Command "{cmd_string}" failed with returncode {e.returncode}')
        return e.returncode
    else:
        logger.info(f'Successfully executed "check_call({cmd_string})"')
    return 0


def build_config(sample):
    os.chdir("../" + sample["project"] + "/" + sample["subfolder"])
    safe_call("cmake --build build --target Editor " + sample["GameExecutable"] +" --config profile -- /m")
    safe_call("cmake --build build --target AssetProcessorBatch --config profile -- /m")
    safe_call("build/bin/profile/AssetProcessorBatch.exe")
    #safe_call("build/bin/profile/AtomSampleViewerStandalone.exe " + samples["cmdparam"])
    #safe_call("build/bin/profile/LoftSample.GameLauncher.exe " + samples["cmdparam"])


settings = process_settings()
samples = settings["SAMPLES_TO_RUN"]
for i in samples:
    build_config(i)
#issues with asset processor need to be fixed






