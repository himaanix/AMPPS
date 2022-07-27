"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import utilities as util
import matplotlib.pyplot as plt 

def hist_of_single_test(sample):
    data = sample["Data"]
    print(data)
    fig, ax = plt.subplots()
    ax.hist(data, bins=100, linewidth=1, edgecolor= "white")
    plt.show()



settings = util.settings
samples = settings["SAMPLES_TO_RUN"]
for i in samples:
    sample = util.get_row_csv(i, 0)
    hist_of_single_test(sample)

    