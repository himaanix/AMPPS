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

def ProcessJson(file):
    f = open(file)
    return json.load(f)
    
def Chdir(path):
    os.chdir(path)

def JoinPaths(*paths):
    return os.path.join(*paths)

def Home():
    Chdir(wd)
    
def SafeCall(command, **kwargs):
    """
    Method adapted from Lumberyard Utilities
    
    Forwards arguments to subprocess.check_call so better error messages can be displayed upon failure.
    This function eats the subprocess.CalledProcessError exception upon command failure and returns the exit code.

    :param command: A list of the command to execute and its arguments as if split by whitespace.
    :param kwargs: Keyword args forwarded to subprocess.check_call.
    :return: An exitcode of 0 if the call succeeds, otherwise the exitcode returned from the failed subprocess call.
    """
    cmdString = command
    if type(command) == list:
        cmdString = ' '.join(command)

    logger.info(f'Executing "check_call({cmdString})"')
    try:
        subprocess.check_call(command, **kwargs)
    except subprocess.CalledProcessError as e:
        logger.warning(f'Command "{cmdString}" failed with returncode {e.returncode}')
        return e.returncode
    else:
        logger.info(f'Successfully executed "check_call({cmdString})"')
    return 0

def ProcessData(sample):
    path = os.path.join(sample["project"], sample["subfolder"], "user", sample["output_location"])
    Chdir(path)
    fps = []
    frame = 1
    while(True):
        file_name = 'cpu_frame' + str(frame) + '_time.json'
        if (not os.path.exists(file_name)):
            break
        f = ProcessJson(file_name)
        fps.append((f["ClassData"])["frameTime"])
        frame +=1

        
    meta = ProcessJson('benchmark_metadata.json')
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
    Home()
    return all_data

def AddRowCsv(sample, data):
    Chdir(sample["path_to_data"])
    headers = []
    filename = sample["data_name"]
    if (not os.path.exists(filename)):
        SafeCall("touch " + filename)
        headers = ["Date", "Time", "BenchmarkName", "GPU", "Mean", "Min", "Max", "Data"]
        f = open(filename, 'w') 
        i = csv.writer(f)
        i.writerow(headers)
        f.close()
    else:
        with open(sample["data_name"]) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            dict_from_csv = dict(list(csv_reader)[0])
            headers = list(dict_from_csv.keys())
    with open(sample["data_name"], 'a', newline='') as f:
        i = csv.DictWriter(f, headers)
        i.writerow(data)
    Home()
    
def GetRowCsv(sample, row): 
    all_data = GetAllRows(sample)
    return all_data[row]
    

def GetAllRows(sample):
    Chdir(sample["path_to_data"])
    with open(sample["data_name"], 'r') as f:
        csv_reader = csv.DictReader(f)
        data = list(csv_reader)
    Home()
    for i in data:
        i["Mean"] = float(i["Mean"])
        i["Min"] = float(i["Min"])
        i["Max"] = float(i["Max"])
        i["Data"] = StringRepToFloats(i["Data"])
    return data

    
def StringRepToFloats(list):
    list_of_strings = list.strip('][').split(', ')
    list_of_floats = []
    for i in list_of_strings:
        list_of_floats.append(float(i))
    return list_of_floats
    


settings = ProcessJson('settings.json')
wd = os.getcwd()
Home()

