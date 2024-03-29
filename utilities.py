"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import logging
import os
import shutil
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
    
def ChDir(path):
    os.chdir(path)

def JoinPaths(*paths):
    return os.path.join(*paths)

def RmDir(path):
    shutil.rmtree(path, onerror=HandleWriteProtectedError)

def HandleWriteProtectedError(func, path, exc_info):
    print('Handling Error for file ', path)
    print(exc_info)
    if not os.access(path, os.W_OK):
        os.chmod(path, 0o200)
        func(path)

def Home():
    ChDir(wd)
    
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

    print(f'Executing "check_call({cmdString})"')
    try:
        subprocess.check_call(command, **kwargs)
    except subprocess.CalledProcessError as e:
        print(f'Command "{cmdString}" failed with returncode {hex(e.returncode)}')
        return e.returncode
    else:
        print(f'Successfully executed "check_call({cmdString})"')
    return 0

def CalcStd(mean, data):
    res = 0
    for i in data:
        res += (mean - i) ** 2
    res = res/(len(data) - 1)
    res = res ** (1/2)
    return res

def ProcessData(sample):
    path = os.path.join(sample["project"], sample["subfolder"], "user", sample["output_location"])
    ChDir(path)
    fps = []
    frame = 1
    while(frame <= sample["frame_count"]):
        file_name = 'cpu_frame' + str(frame) + '_time.json'
        if (not os.path.exists(file_name)):
            break
        f = ProcessJson(file_name)
        fps.append((f["ClassData"])["frameTime"])
        frame +=1

    mean = reduce(lambda a, b: a+b, fps)/len(fps)
    meta = ProcessJson('benchmark_metadata.json')
    date = datetime.datetime.now()
    allData = {
        "Timestamp": date.strftime("%m/%d/%y %H:%M"),
        "BenchmarkName": (meta["ClassData"])["benchmarkName"],
        "GPU": ((meta["ClassData"])["gpuInfo"])["description"],
        "Mean": mean,
        "Min": min(fps),
        "Max": max(fps),
        "Standard Deviation": CalcStd(mean,fps),
        "Data": fps   
    }
    Home()
    return allData

def AddRowCsv(sample, data): #this method needs to be cleaned up
    ChDir(sample["path_to_data"])
    headers = ["Timestamp", "BenchmarkName", "GPU", "Mean", "Min", "Max", "Standard Deviation", "Data"] 
    filename = sample["data_name"]
    if (not os.path.exists(filename)):
        n = open(filename, 'w')
        i = csv.writer(n)
        i.writerow(headers)
        n.close()
    with open(sample["data_name"], 'a', newline='') as f:
        i = csv.DictWriter(f, headers)
        i.writerow(data)
    Home()
    
def GetRowCsv(sample, row): 
    all_data = GetAllRows(sample)
    return all_data[row]
    

def GetAllRows(sample):
    ChDir(sample["path_to_data"])
    with open(sample["data_name"], 'r') as f:
        csv_reader = csv.DictReader(f)
        data = list(csv_reader)
    Home()
    for i in data:
        i["Mean"] = float(i["Mean"])
        i["Min"] = float(i["Min"])
        i["Max"] = float(i["Max"])
        i["Standard Deviation"] = float(i["Standard Deviation"])
        i["Data"] = StringRepToFloats(i["Data"])
    return data

    
def StringRepToFloats(list):
    list_of_strings = list.strip('][').split(', ')
    list_of_floats = []
    for i in list_of_strings:
        list_of_floats.append(float(i))
    return list_of_floats
    

def SetConstants(f):
    settings = ProcessJson(f)
    return settings

wd = os.getcwd()
Home()