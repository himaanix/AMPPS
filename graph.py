"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
import matplotlib.pyplot as plt 



def HistOfSingleTest(sample, row):
    data = util.GetRowCsv(sample, row)
    mean = data["Mean"]
    maxx = data["Max"]
    date_time = data["Timestamp"]
    data = data["Data"]
    fig, ax = plt.subplots()
    ax.hist(data, bins=100, linewidth=1, edgecolor= "white")
    plt.axvline(x=mean, color = 'green')
    plt.axvline(x=maxx, color = 'red')
    ax.spines['bottom'].set_visible(False)
    plt.ylabel("Count")
    plt.xlabel("Frame Time in ms")
    plt.title("Histogram of Frametimes for " + date_time)
    util.ChDir(sample['path_to_data'])
    plt.savefig("hist" + str(row) + ".jpg")
    util.Home()

def HistOfLatest(sample):
    data = util.GetAllRows(sample)
    index = len(data) -1
    print("Histogram of Latest Dataset has been saved to " + sample["path_to_data"])
    return HistOfSingleTest(sample,index)

def DataOverTime(sample,fps):
    means = []
    maxes = []
    mins =  []
    stds =  []
    runs = []

    if fps:
        filename = "fpsovertime"
        ylabel = "Frames/Second"
        title = "Frames/Second Over Time"
    else:
        filename = "frametimeovertime"
        ylabel = "Frame Time (ms)"
        title = "Frame Time Over Time"
    for data in util.GetAllRows(sample):
        mean =  data["Mean"]
        maxx =  data["Max"]
        minn =  data["Min"]
        std  =  data["Standard Deviation"]
        run = data["Timestamp"]
        if(fps):

            fpsdata = [1000/i for i in data["Data"]]
            mean = 1000/mean
            maxx = 1000/maxx
            minn = 1000/minn
            std = util.CalcStd(mean, fpsdata)

        means.append(mean)
        maxes.append(maxx)
        mins.append(minn)
        stds.append(std)
        runs.append(run)

    fig, ax = plt.subplots()
    ax.scatter(runs,maxes, color = 'red', zorder = 1)
    ax.scatter(runs, mins, color = 'red', zorder = 5)
    ax.scatter(runs,means, color = 'black', zorder= 10)
    ax.errorbar(runs, means, stds, fmt = 'none', linewidth=2, capsize=6)
    plt.ylabel(ylabel)
    plt.xlabel("Dates")
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    util.ChDir(sample['path_to_data'])
    plt.savefig(filename + ".jpg")
    util.Home()
    
def FpsOverTime(sample):
    DataOverTime(sample,True)
    print("Graph of Frames/Second Over Time has been saved to " + sample["path_to_data"])

def FramesOverTime(sample):
    DataOverTime(sample,False)
    print("Graph of Frame Times Over Time has been saved to " + sample["path_to_data"])


def Graph(settings):
    samples = settings["samples_to_run"]
    for i in samples:
        FpsOverTime(i)
        FramesOverTime(i)
        HistOfLatest(i)


if __name__ == '__main__':

    Graph()   