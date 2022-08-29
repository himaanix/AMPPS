----------------------------------------------------------------------------------------------------
--
-- Copyright (c) Contributors to the Open 3D Engine Project.
-- For complete copyright and license terms please see the LICENSE at the root of this distribution.
--
-- SPDX-License-Identifier: Apache-2.0 OR MIT
--
--
--
----------------------------------------------------------------------------------------------------
g_baseFolder = ResolvePath('@user@/Scripts/PerformanceBenchmarks/')
IDLE_COUNT = 1000
FRAME_COUNT = 2500
projects_to_run = {
    {prefix = 'Performance', name = '100KDraw_10KDrawable_MultiView', width = 800, height =600
    }
}

Print('Capturing data for ' ..tostring(#projects_to_run) .. ' benchmarks')
for index, sample in ipairs(projects_to_run) do 
    sample_path = sample['prefix'] ..'/' .. sample ['name']
    Print('Opening sample' ..sample_path)
    OpenSample(sample_path)
    ResizeViewport(sample['width'],sample['height'])

    output_path =  g_baseFolder.. sample['name']
    CaptureBenchmarkMetaData(sample['name'], output_path) 
    Print('Idling for ' .. tostring(IDLE_COUNT) .. ' frames..')
    IdleFrames(IDLE_COUNT)
    Print('Capturing timestamps for ' .. tostring(FRAME_COUNT) .. ' frames...')
    for i = 1, FRAME_COUNT do 
        frame_timestamps = output_path .. '/frame' .. tostring(i) .. '_timestamps.json'
        cpu_timings = output_path .. '/cpu_frame' .. tostring(i) .. '_time.json'
        --CapturePassTimestamp(frame_timestamps)
        CaptureCpuFrameTime(cpu_timings) 
    end
end

Print('Capturing complete.')

