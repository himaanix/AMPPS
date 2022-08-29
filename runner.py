"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import build 
import graph
import clone
import utilities
import argparse



parser = argparse.ArgumentParser(description= "Options for Running AMPPS")
parser.add_argument("--clean_build", help = "Runs a clean build of the project", default = False, action = 'store_true')
parser.add_argument("--clean_assets", help = "Runs a clean build of assets", default = False, action = 'store_true')
parser.add_argument("--graph", help = "Uses the graphing utility", default = False, action = 'store_true')
parser.add_argument("--collect", help = "Collects data", default = False, action = 'store_true')
parser.add_argument("--build", help = "Builds the Project", default = False, action = 'store_true')
parser.add_argument("--update", help = "git pull on the project and O3DE", default = False, action = 'store_true')
parser.add_argument("--path_to_settings", help = "Specify an alternate path to a settings.json file", default = "settings.json")
parser.add_argument("--path_to_build", help = "Specify the path to the build folder if not using AMPPS build functionality. This path should be to the folder containing the build folder", default = "")
parser.add_argument("--annotation", help = "Add an annotation for this dataset if collecting data", default = "")
args = parser.parse_args()


doBuild=True
doUpdate=True
doCollect=True
doGraph = True
if args.build or args.update or args.collect or args.graph:
    doBuild = args.build
    doUpdate = args.update
    doCollect = args.collect
    doGraph = args.graph

clone.Manage(doUpdate)
settings = utilities.SetConstants(args.path_to_settings)
print(args)
if doBuild or doCollect:
    build.Build(args.clean_build, args.clean_assets, doBuild, args.path_to_build, doCollect, args.annotation, settings)
if doGraph:
    graph.Graph(settings)
