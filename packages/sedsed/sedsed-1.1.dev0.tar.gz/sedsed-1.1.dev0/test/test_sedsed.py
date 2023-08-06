#/usr/bin/env python

import os
import os.path
import subprocess

import pytest

pwd = os.path.dirname(os.path.abspath(__file__))
folders = [f for f in next(os.walk(pwd))[1]
                if not f.startswith('_')]


@pytest.mark.parametrize("folder", folders)
def test_dir(folder):
    subprocess.check_call(os.path.join(pwd, folder, 'run'), shell=True)

