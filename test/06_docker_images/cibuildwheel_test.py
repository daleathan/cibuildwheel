import os
import platform

import pytest

import utils


def test():
    project_dir = os.path.dirname(__file__)

    if utils.platform != 'linux':
        pytest.skip('the test is only relevant to the linux build')
    if platform.machine() not in ['x86_64', 'i686']:
        pytest.skip('this test is currently only possible on x86_64/i686 due to availability of alternative images')

    actual_wheels = utils.cibuildwheel_run(project_dir, add_env={
        'CIBW_MANYLINUX_X86_64_IMAGE': 'dockcross/manylinux2010-x64',
        'CIBW_MANYLINUX_I686_IMAGE': 'dockcross/manylinux2010-x86',
        'CIBW_SKIP': 'pp*',
    })

    # also check that we got the right wheels built
    expected_wheels = [w for w in utils.expected_wheels('spam', '0.1.0')
                       if '-pp' not in w]
    assert set(actual_wheels) == set(expected_wheels)
