#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdpy
auth = gdpy.GeneDockAuth("1FJGq7h+cesj6tVz91e4Lg==", "h9DzvQADeddq2/Ku8GVDpdG2IPs=")

task = gdpy.Tasks(auth, "https://cn-beijing-api.genedock.com", "zexiong_niu", "default", connect_timeout=600)
active_workflow_result = task.active_workflow(
    '/Users/chensixiu/genedock/genedock-official-python-sdk/gdpy/LBH8122T.json', 'wes_somatic_pipeline_split', int(5))
print(active_workflow_result.status)
