"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import logging
import os
import subprocess

logger = logging.getLogger(__name__)

class PerformanceTestingException(Exception):
    """ Custom Exception class for performance testing """
    pass

@pytest.mark.parametrize('launcher_platform', ['windows'])
@pytest.mark.parametrize("project", ["AtomSampleViewer", "LoftArchSample"])
@pytest.mark.parametrize('rhi', ['dx12', 'vulkan'])
class TestPerformance:
    def test_Performance(self,request, workspace, launcher_platform, rhi):
        script = 'benchmark.lua'
        script_path = os.path.join(workspace.paths.project(), script )
        if not os.path.exists(script_path):
            raise PerformanceTestingException(f 'Test script does not exist in path: {script_path}')
        exectuable = 'AtomSampleViewer.exe '
        cmd = os.path.join(workspace.paths.build_directory(),
                            exectuable
                            f'--project-path={workspace.paths.project()} '
                            f'--rhi {rhi} '
                            f'--runteststuite scripts/{script} ' 
                            '--exitontesetend')

""" kill processes """

