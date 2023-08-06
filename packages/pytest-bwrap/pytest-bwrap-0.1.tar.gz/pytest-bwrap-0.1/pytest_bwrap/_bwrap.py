import pathlib
import os
import subprocess
import sys

from ._host import has_lib64, has_merged_usr


def bwrap_is_installed():
    PATH = os.environ.get('PATH', '/usr/bin:/bin')
    PATH = [pathlib.Path(d) for d in PATH.split(':')]

    for bindir in PATH:
        if (bindir / 'bwrap').is_file():
            return True

    return False


class SandboxCommand:
    def __init__(self):
        self._cmd = [
            'bwrap',
            '--unshare-all',
            '--dev', '/dev',
            '--proc', '/proc',
            '--tmpfs', '/tmp',
        ]
        self._get_usr_args()
        self._get_etc_args()
        self._get_project_args()

    def _get_etc_args(self):
        """Get the arguments related to /etc"""
        self._cmd.extend([
            '--ro-bind', '/etc/hosts', '/etc/hosts',
            '--ro-bind', '/etc/resolv.conf', '/etc/resolv.conf',
        ])

    def _get_usr_args(self):
        """Get the arguments related to /usr"""
        self._cmd.extend([
            '--ro-bind', '/usr', '/usr',
        ])
        dirs = ['/bin', '/sbin', '/lib']

        if has_lib64():
            dirs.append('/lib64')

        if has_merged_usr():
            for dest in dirs:
                src = '/usr{dest}'.format(dest=dest)
                self._cmd.extend(['--symlink', src, dest])

        else:
            for dest in dirs:
                src = dest
                self._cmd.extend(['--ro-bind', src, dest])

    def _get_project_args(self):
        """Get the arguments related to the project being tested"""
        cwd = str(pathlib.Path.cwd().resolve())
        exec_prefix = str(pathlib.Path(sys.argv[0]).parent.parent)

        # The virtual env (or similar)
        if exec_prefix not in ('/usr/bin', '/bin'):
            self._cmd.extend(['--ro-bind', exec_prefix, exec_prefix])

        # The project tree being tested
        self._cmd.extend([
            '--bind', cwd, cwd,
            '--chdir', cwd,
        ])

    def add_extra_readonly_dirs(self, ro_dirs):
        """Get the arguments for extra read-only directories

        ro_dirs is a list of paths, either as str or pathlib.Path objects.
        """
        for path in ro_dirs:
            d = str(path)
            self._cmd.extend([
                '--tmpfs', d,
                '--remount-ro', d,
            ])

    def allow_network(self):
        self._cmd.append('--share-net')

    def run(self, test):
        self._cmd.extend(['py.test', test])

        proc = subprocess.Popen(
            self._cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        out, err = out.decode().strip(), err.decode().strip()

        if err:
            raise SandboxError(out, err)

        if proc.returncode != 0:
            raise SandboxedTestFailed(out)


class SandboxedTestFailed(Exception):
    """The test failed

    This is raised when everything went fine as far as this plugin is
    concerned, but the test simply failed."""
    pass


class SandboxError(Exception):
    """Something was wrong in the sandbox

    This is raised when the command couldn't even be run because the sandbox
    had not been properly setup.

    It should never happen. If it does, consider this a bug, and please report
    it: https://framagit.org/bochecha/pytest-bwrap/issues/new
    """
    pass
