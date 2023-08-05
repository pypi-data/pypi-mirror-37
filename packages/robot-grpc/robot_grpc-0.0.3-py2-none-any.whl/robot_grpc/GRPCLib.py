__version__ = '0.0.1'

import os
import os.path
from subprocess import Popen, PIPE

from robot.api import logger


class GRPCLib:
    """GRpc library"""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, host, git_url, branch, access_token):
        self._host = host
        self._gitUrl = git_url
        self._branch = branch
        self._accessToken = access_token
        logger.info("GRpc config success!")

    def invoke_grpc_method(self, method_name, request):
        """Invoke grpc method"""
        p = Popen(
            [
                'node',
                os.path.dirname(os.path.realpath(__file__)) + '/build/invokeMethod.js',
                self._host,
                self._gitUrl,
                self._branch,
                self._accessToken,
                method_name,
                request,
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        if rc != 0:
            raise Exception(output)
        print output
        return output

    def run_grpc_cases(self, case_file_path, case_name=''):
        """Run grpc interface test case"""
        p = Popen(
            [
                'node',
                os.path.dirname(os.path.realpath(__file__)) + '/build/runCases.js',
                self._host,
                self._gitUrl,
                self._branch,
                self._accessToken,
                case_file_path,
                case_name,
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        logger.info(unicode(output, "utf8", errors="ignore"), html=True)
        if rc == 2:
            raise Exception(u"Case no matched")
        elif rc != 0:
            raise Exception(output)
        return output
