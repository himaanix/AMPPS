"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import logging
import os
import subprocess
import json
import datetime
import time
from functools import reduce
import csv
logger = logging.getLogger(__name__)


class PerformanceTestingException(Exception):
    """ Custom Exception class for performance testing """
    pass

def process_json(file):
    f = open(file)
    return json.load(f)
    
def chdir(path):
    os.chdir(path)

def join_paths(*paths):
    return os.path.join(*paths)
    
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

def process_data(sample):
    #Only for ASV right now
    safe_call("pwd")
    chdir("../" + sample["project"] + "/user/Scripts/PerformanceBenchmarks/100KDraw_10KDrawable_MultiView")
    fps = []
    for frame in range(1,101):
        f = process_json('cpu_frame' + str(frame) + '_time.json')
        fps.append((f["ClassData"])["frameTime"])
    meta = process_json('benchmark_metadata.json')
    date = datetime.datetime.now()
    all_data = {
        "Date": date.strftime("%B %d %Y"),
        "Time": date.strftime("%H:%M:%S"),
        "BenchmarkName": (meta["ClassData"])["benchmarkName"],
        "GPU": ((meta["ClassData"])["gpuInfo"])["description"],
        "Mean": reduce(lambda a, b: a+ b, fps)/ len(fps),
        "Min": min(fps),
        "Max": max(fps),
        "Data": fps
    }
    chdir(settings["THIS_DIRECTORY"])
    return all_data

def add_row_csv(sample, data):
    chdir(sample["PathToData"])
    headers = ["Date", "Time", "BenchmarkName", "GPU", 
               "Mean", "Min", "Max", "Data"]
    with open('Data.csv', 'a', newline='') as f:
        i = csv.DictWriter(f, headers)
        i.writerow(data)
    chdir(settings["THIS_DIRECTORY"])
    
def get_row_csv(sample, row): 
    all_data = get_all_rows(sample)
    return all_data[row]
    

def get_all_rows(sample):
    chdir(sample["PathToData"])
    with open('Data.csv', 'r') as f:
        csv_reader = csv.DictReader(f)
        data = list(csv_reader)
    chdir(settings["THIS_DIRECTORY"])
    for i in data:
        i["Mean"] = float(i["Mean"])
        i["Min"] = float(i["Min"])
        i["Max"] = float(i["Max"])
        i["Data"] = stringrep_to_floats(i["Data"])
    return data

    
def stringrep_to_floats(list):
    list_of_strings = list.strip('][').split(', ')
    list_of_floats = []
    for i in list_of_strings:
        list_of_floats.append(float(i))
    return list_of_floats
    


settings = process_json('settings.json')
chdir(settings["THIS_DIRECTORY"])

