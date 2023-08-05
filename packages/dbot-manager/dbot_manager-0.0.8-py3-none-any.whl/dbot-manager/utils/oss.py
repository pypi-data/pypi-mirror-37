#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oss2

auth = oss2.Auth('LTAIlYmmgfYsCDWf', 'yEFGgoxgZF3OM4LoEZMacgxcIkPkTm')
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'response-files')

def put(obj_name, content_bytes):
    assert isinstance(content_bytes, 'bytes')
    bucket.put_object(obj_name, content_bytes)
