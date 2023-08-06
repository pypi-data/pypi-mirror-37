import pathlib
import sys
import types

import pytest

from ._bwrap import SandboxCommand, SandboxedTestFailed


def _get_filtered(text, testname):
    # FIXME: Scraping the output of a program is fragile, can we do better?
    if not text:
        return '', '', ''

    lines = text.split('\n')

    error = []
    stdout = []
    stderr = []
    buffer = None

    function_indication = '_ {testname} _'.format(testname=testname)
    stdout_indication = '- Captured stdout call -'
    stderr_indication = '- Captured stderr call -'
    end_indication = '= 1 failed in '

    for line in lines:
        if end_indication in line:
            break

        if stdout_indication in line:
            buffer = stdout
            continue

        if stderr_indication in line:
            buffer = stderr
            continue

        if function_indication in line:
            buffer = error
            continue

        if buffer is not None:
            buffer.append(line)

    return '\n'.join(error), '\n'.join(stdout), '\n'.join(stderr)


def _run_test(item):
    config = item.config
    cwd = str(pathlib.Path.cwd().resolve())

    cmd = SandboxCommand()

    # Requested read-only directories
    global_ro_dirs = config.getini('extra-ro-dirs')
    ro_dirs = global_ro_dirs + getattr(item.function, '_read_only_dirs', [])
    cmd.add_extra_readonly_dirs(ro_dirs)

    if getattr(item.function, '_network_allowed', False):
        cmd.allow_network()

    testfile = item.fspath.relto(cwd)
    test = '{testfile}::{item.name}'.format(testfile=testfile, item=item)

    try:
        cmd.run(test)

    except SandboxedTestFailed as e:
        failure, out, err = _get_filtered(e.args[0], item.name)

        print(out)
        print(err, file=sys.stderr)
        pytest.fail(failure)


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--bwrap', action='store_true',
        help='Run your tests in Bubblewrap a sandbox')

    parser.addini(
        'extra-ro-dirs', type='linelist', default=[],
        help='A list of additional directories to make read-only in the '
             'sandbox')


def pytest_runtest_call(item):
    config = item.config

    if not config.option.bwrap:
        return

    # Now monkey-patch the test runner
    item.runtest = types.MethodType(_run_test, item)

    return True
