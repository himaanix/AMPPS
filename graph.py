"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
import matplotlib.pyplot as plt 

def calcstd(mean, data):
    res = 0
    for i in data:
        res += (mean - i) ** 2
    res = res/(res - 1)
    res = res ** (1/2)
    return res

def hist_of_single_test(sample, row):
    data = util.get_row_csv(sample, row)

    data = data["Data"]
    fig, ax = plt.subplots()
    ax.hist(data, bins=100, linewidth=1, edgecolor= "white")
    plt.show()

def data_over_time(sample):
    means = []
    maxes = []
    mins =  []
    stds =  []
    runs = []


    for data in util.get_all_rows(sample):
        
        mean = data["Mean"]
        maxx = data["Max"]
        minn = data["Min"]
        run = data["Date"] + " " + data["Time"]

        means.append(mean)
        maxes.append(maxx)
        mins.append(minn)
        stds.append(calcstd(mean,data["Data"]))
        runs.append(run)

    print(len(runs))
    print(len(means))
    fig, ax = plt.subplots()
    ax.errorbar(runs, means, stds, fmt = 'o', linewidth=2, capsize=6)
    plt.show()
    



settings = util.settings
samples = settings["SAMPLES_TO_RUN"]
for i in samples:
    data_over_time(i)

    