import os
import click
import contextlib
import tempfile
import errno
import shlex
from shutil import rmtree
from subprocess import call, check_output, Popen

def run(*args, **kwargs):
    shell = kwargs.pop("shell",False)
    capture = kwargs.pop("capture", False)
    method = check_output if capture else call

    cmd = " ".join(args)
    click.echo("> "+click.style(cmd,fg="green"))
    if shell:
        return method(cmd, shell=True)
    else:
        return method(shlex.split(cmd))

@contextlib.contextmanager
def cd(path):
    """ A context manager which changes the working
        directory to the given path, and then changes
        it back to its previous value on exit.
    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    click.echo(path)
    os.chdir(prev_cwd)

@contextlib.contextmanager
def tempdir():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    click.echo("Deleting temporary directory "\
        +click.style(tmp_dir,fg="cyan"))
    try:
        rmtree(tmp_dir)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
        # ENOENT: no such file/directory
            raise

