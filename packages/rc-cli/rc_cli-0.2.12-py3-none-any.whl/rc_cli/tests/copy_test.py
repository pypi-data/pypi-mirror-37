import unittest

import os
import pathlib
import json

setup_path = pathlib.Path(os.path.dirname(os.path.relpath(__file__)))

from rc_cli.utils.copier import Copier
from rc_cli.client import *

from unittest.mock import MagicMock
from unittest.mock import patch

import requests
import click
from click.testing import CliRunner
from subprocess import call

class CopierTests(unittest.TestCase):

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_init_no_dest_or_file(self, error, verbose):
        try:
            copier = Copier(None, 'test.txt', (), None, False, False, '')
            self.fail()
        except:
            error.assert_called()

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_init_dest_no_file(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            copier = Copier(None, 'test.txt', ('dir1',), None, False, False, '')
            self.assertEqual(copier.destination_directories[0].name, 'dir1')

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_init_no_dest_with_file(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir1')
            copier = Copier(None, 'test.txt', (), None, False, False, 'dirs.txt')
            self.assertEqual(copier.destination_directories[0].name, 'dir1')

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_init_with_dest_and_file(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'test.txt', ('dir1',), None, False, False, 'dirs.txt')
            self.assertEqual(copier.destination_directories[0].name, 'dir1')

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_init_destination_name(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'test.txt', ('dir1',), 'name', False, False, 'dirs.txt')
            self.assertEqual(copier.destination_filename, 'name')

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_read_file(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'dirs.txt', ('dir1',), 'name', False, False, 'dirs.txt')
            contents = copier._Copier__read_source_file()
            self.assertEqual(contents, 'dir2')

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_write_file_not_exist(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'dirs.txt', ('dir1',), 'name', False, False, 'dirs.txt')
            contents = copier._Copier__write_file(pathlib.Path('new.txt'))
            self.assertTrue(os.path.exists('new.txt'))

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    def test_write_dir_not_exist(self, verbose, error):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dir1/dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'dir1', ('dir1',), 'name', False, False, 'dirs.txt')
            contents = copier._Copier__write_file(pathlib.Path('new'))
            self.assertTrue(os.path.isdir('new'))
            self.assertTrue(os.path.exists('new'))
            self.assertTrue(os.path.exists('new/dirs.txt'))

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    @patch(__name__ + '.Copier._warn')
    def test_write_file_exist_no_interactable_force(self, verbose, error, warn):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'dirs.txt', ('dir1',), 'name', False, False, 'dirs.txt')
            contents = copier._Copier__write_file(pathlib.Path('test.txt'))

            with click.open_file('test.txt', 'r') as f:
                content = f.read()

            self.assertEqual(content, '')
            warn.assert_called()

    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._error')
    @patch(__name__ + '.Copier._warn')
    def test_write_file_exist_no_interactable_force(self, verbose, error, warn):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            open('test.txt', 'w')
            with open('dirs.txt', 'w') as f:
                f.write('dir2')
            copier = Copier(None, 'dirs.txt', ('dir1',), 'name', True, False, 'dirs.txt')
            contents = copier._Copier__write_file(pathlib.Path('test.txt'))

            with click.open_file('test.txt', 'r') as f:
                content = f.read()

            self.assertEqual(content, 'dir2')


    @patch(__name__ + '.Copier._warn')
    @patch(__name__ + '.Copier._verbose')
    @patch(__name__ + '.Copier._Copier__write_file')
    def test_execute(self, warn, verbose, write):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            os.mkdir('fileDir')
            open('fileDir/test.txt', 'w')
            os.mkdir('src')
            copier = Copier(None, 'dirs.txt', ('dir1',), 'name', True, False, 'dirs.txt')
            copier._Copier__write_file = MagicMock()
            copier.destination_directories = [pathlib.Path('fileDir/*'), pathlib.Path('dir1')]
            copier.execute()
            self.assertEqual(copier._Copier__write_file.call_count, 2)

    @patch(__name__ + '.Copier._warn')
    @patch(__name__ + '.Copier._verbose')
    def test_client(self, warn, verbose):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.mkdir('dir1')
            with open('dirs.txt', 'w') as file:
                file.write('dir1')
            open('test.txt', 'w')
            #runner.invoke(cli, ['copy', 'test.txt', '-r', 'dirs.txt'], catch_exceptions=False)
            runner.invoke(cli, ['copy', 'test.txt', '-r', 'dirs.txt'], catch_exceptions=False)
            self.assertTrue(os.path.exists('dir1/test.txt'))