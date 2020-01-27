import os, textwrap
from . import utils


def test(tmpdir):
    project_dir = str(tmpdir)

    utils.generate_project(
        path=project_dir,
        setup_py_add=textwrap.dedent(r'''
            # explode if run on Python 2.7 or Python 3.4 (these should be skipped)
            if sys.version_info[0:2] == (2, 7):
                raise Exception("Python 2.7 should not be built")
            if sys.version_info[0:2] == (3, 4):
                raise Exception("Python 3.4 should be skipped")
        ''')
    )
    
    # build the wheels
    utils.cibuildwheel_run(
        project_dir, add_env={"CIBW_BUILD": "cp3?-*", "CIBW_SKIP": "cp37-*",}
    )

    # check that we got the right wheels. There should be no 2.7 or 3.7.
    expected_wheels = [
        w
        for w in utils.expected_wheels("spam", "0.1.0")
        if ("-cp3" in w) and ("-cp37" not in w)
    ]
    actual_wheels = os.listdir("wheelhouse")
    assert set(actual_wheels) == set(expected_wheels)
