#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import os
import sys
from subprocess import Popen, PIPE

from robot.api import logger

reload(sys)
sys.setdefaultencoding('utf-8')

name = "RobotGrpc"

__version__ = '0.0.1'
is_windows = os.name == 'nt'


class RobotGrpc:
    """GRpc library"""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, host, git_url, branch, access_token, ssl='none'):
        self._host = host
        self._gitUrl = git_url
        self._branch = branch
        self._accessToken = access_token
        self._ssl = ssl
        logger.info("GRpc config success!")

    def invoke_grpc_method(self, method_name, request):
        """Invoke grpc method"""
        p = Popen(
            [
                'robot-grpc',
                'invokeMethod',
                self._host,
                self._gitUrl,
                self._branch,
                self._accessToken,
                self._ssl,
                method_name,
                base64.b64encode(request),
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=is_windows,
        )
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        if rc != 0:
            raise Exception(output)
        try:
            return json.loads(output)
        except err:
            return output

    def run_grpc_cases(self, case_file_path, case_name=''):
        """Run grpc interface test case"""
        p = Popen(
            [
                'robot-grpc',
                'runCases',
                self._host,
                self._gitUrl,
                self._branch,
                self._accessToken,
                self._ssl,
                base64.b64encode(case_file_path),
                base64.b64encode(case_name),
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=is_windows,
        )
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        logger.info(unicode(output, "utf8", errors="ignore"), html=True)
        if rc == 2:
            raise Exception(u"Case no matched")
        elif rc != 0:
            raise Exception(output)
        return output
