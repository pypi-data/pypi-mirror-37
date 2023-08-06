# -*- coding: utf-8 -*-

"""MagicMarker is a tool that automatically marks pytests with a UUID"""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
from flake8.main.cli import main as flake8_main
from flake8.main.application import Application
from contextlib import contextmanager
from magic_marker.fixable import Fixable
import sys
import six
import json
import uuid
import re
import tempfile
import string
import random
import shutil
import errno
import os


class MagicMarker(object):

    def __init__(self):
        """Crate a new MagicMarker object
        """
        self.options = None
        dir_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self._backup_path = os.path.join(tempfile.gettempdir(), dir_name)
        self._fixable = Fixable()

    @property
    def backup_path(self):
        return self._backup_path

    def find_options(self, config):
        """Use flake8's library to find a valid config for flake8"""
        flk8 = Application()
        args = []
        if config:
            args.append("--config={}".format(config))
        flk8.initialize(args)
        opts = {}
        for key, value in list(vars(flk8.options).items()):
            if re.match(r'pytest_mark.*', key):
                for option in value:
                    try:
                        opts[key]
                    except KeyError:
                        opts[key] = {}
                    val = option.split('=')
                    opts[key][val[0]] = val[1]
        self.options = opts

    def run_flake8_and_mark(self, path, config):
        """Run flak8 and edit and fix errors

        Args:
            path (str): The path to target for the fix
            config (str): The path to a config to be passed to flake8

        Returns:
            str: the message stating what was performed
        """

        self.find_options(config)
        args = [
            'flake8',
            path,
            "--format=json",
            "--select=M5"  # only covers case of no mark present
        ]
        if config:
            args.append("--config={}".format(config))

        with self.patch_sys_argv(args), self.captured_stdout() as stdout:
            try:
                flake8_main()
            except SystemExit:
                pass  # This is raised by flake8

        flake8_output = json.loads(stdout.getvalue())
        self._backup_whole_path(path)
        return self.fix_it(flake8_output)

    def _backup_whole_path(self, path):
        """Backup the entire target

        Args:
            path (str): the path to copy
        """
        try:
            shutil.copytree(path, self._backup_path)
        except OSError as exc:  # python >2.5
            if exc.errno == errno.ENOTDIR:
                # its a single file
                shutil.copy(path, self.backup_path)
            else:
                raise RuntimeError("Magic Marker was not able to backup the target {}".format(path))

    def fix_it(self, flake8_output):
        """Perform the fix

        Args:
            flake8_output (str): The parsed json data from flake8-json

        Returns:
            str: the message stating what was performed
        """
        message = ""
        for file_path in flake8_output:
            if flake8_output[file_path]:
                filname, fixcount = self._fix_file(flake8_output[file_path])
                if fixcount == 1:
                    message += "\n{} : {} test mark added".format(filname, fixcount)
                else:
                    message += "\n{} : {} test marks added".format(filname, fixcount)
        if message:
            return message

    def _fix_file(self, fixes_required):
        """Fixes an individual file

        Args:
            fixes_required (list[dict]): a list of the fixes required for this file

        Returns:
            tuple(str, str):  filename and number of fixes performed
        """
        fixes_performed = 0
        filename = str(fixes_required[0]['filename'])
        with open(filename, 'r') as f:
            data = f.readlines()

        fixes_required.sort(key=lambda x: x['line_number'])

        fixes_required.reverse()  # work from the bottom of the file up
        for fix in fixes_required:
            mark_name, prescribed_fix = self._fixable.check(fix, self.options)
            if prescribed_fix:
                fix_position = fix['line_number']
                if fix_position:
                    fix_position += -1
                mark = self._match_indent(data[fix_position], prescribed_fix(mark_name))
                data.insert(fix_position, mark)
                fixes_performed += 1

        with open(filename, 'w') as f:
            f.writelines(data)
        return filename, fixes_performed

    def _uuid_mark(self):
        """generate a UUID mark string

        Returns:
            str: the correctly formatted UUID mark string
        """
        return "@pytest.mark.{}('{}')\n".format(self._mark, str(uuid.uuid1()))

    @staticmethod
    def _match_indent(def_string, target_line):
        """Match the indent of the original string

        Args:
            def_string (str): the original string from the test definition
            target_line (str): the string that should be updated

        Returns:
            str : The new string updated with correct whitespace
        """
        whitespace = re.match(r'(^\s*)', def_string).group(1)
        if whitespace:
            target_line = whitespace + target_line
        return target_line

    @contextmanager
    def patch_sys_argv(self, new_argv):
        """Patch argv

        Args:
            new_argv (list): the desired argv

        Yields:
            None
        """
        orig = sys.argv
        sys.argv = new_argv
        yield
        sys.argv = orig

    @contextmanager
    def captured_output(self, stream_name):
        """Return a context manager used by captured_stdout/stdin/stderr
        that temporarily replaces the sys stream *stream_name* with a StringIO.

        Args:
            stream_name (str): The name of the stream to capture

        Yields:
            StringIO

        Note: This function and the following ``captured_std*`` are copied
              from CPython's ``test.support`` module."""
        orig_stdout = getattr(sys, stream_name)
        setattr(sys, stream_name, six.StringIO())
        try:
            yield getattr(sys, stream_name)
        finally:
            setattr(sys, stream_name, orig_stdout)

    def captured_stdout(self):
        """Capture the output of sys.stdout:
           with captured_stdout() as stdout:
               print("hello")
           self.assertEqual(stdout.getvalue(), "hello\n")

        Returns:
            GeneratorContextManager
        """
        return self.captured_output("stdout")
