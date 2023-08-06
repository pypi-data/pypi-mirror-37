"""This module allows for the copying of files into other directories"""
import pathlib
import shutil
import sys

import click

from ..logger import Logger

class Copier(Logger):
    """
    Copier takes in a files and directories to copy to and copies the file into those directories

    :param config: Config given from the Click context\n
    :param source_file: File to copy\n
    :param destination_directories: Directories to copy file to\n
    :param name: Name to save the file in the destination directory\n
    :param force: Flag to force copy all files regardless of conflicts\n
    :param interactive: Flag to interactively copy conflicting files. Has precedence over force\n
    :param readFile: Name of the file from which to read directories\n
    """
    def __init__(self, config, source_file, destination_directories, destination_name, force, interactive, read_file):
        super().__init__(config)

        if destination_directories == () and read_file == '':
            self._error('Destination Directories cannot be empty without specifying a file to read. Got "{}"'
                        .format(destination_directories))
            sys.exit(1)
        elif force and interactive:
            self._warn('Specified both interactive and force flag. '
                       'Force flag will be ignored.')

        if destination_directories != ():
            self.destination_directories = list(
                map(lambda destination_directory:
                    pathlib.Path(destination_directory), destination_directories))
        else:
            self.source_file = pathlib.Path(read_file)
            content = self.__read_source_file()
            dirs = content.splitlines()
            self.destination_directories = list(
                map(lambda destination_directory: pathlib.Path(destination_directory), dirs))

        self.source_file = pathlib.Path(source_file)
        self.destination_filename = self.source_file.name if destination_name is None else destination_name

        self.force = force
        self.interactive = interactive

    def execute(self):
        """
        Execute the copy utility.

        :return: None.
        """
        for destination_directory in self.destination_directories:
            if destination_directory.name == '*':  # Windows does not expand this
                self.destination_directories += [entity for entity in destination_directory.parent.iterdir()]
                continue
            if destination_directory.is_file():
                dest_file_path = destination_directory
            elif destination_directory.is_dir():
                dest_file_path = destination_directory.joinpath(self.destination_filename)
            else:
                # Do we want to handle symlinks?
                self._warn('Destination must be a file or directory: {}'.format(destination_directory.as_posix()))
                continue

            self.__write_file(dest_file_path)


    def __read_source_file(self):
        """
        Read the content of the source file.

        :return: String content of the source file.
        """
        self._verbose('Reading source file {}'.format(self.source_file))
        with click.open_file(self.source_file.as_posix(), 'r') as file:
            content = file.read()
        return content

    def __write_file(self, dest_path):
        """
        Write the file.
        Takes into consideration force and interactive flags.
        Interactive flag will take precedence over force.

        :param dest_path: Path of file to write.
        :return: None
        """
        dest_posix_path = dest_path.as_posix()
        source_path = pathlib.Path(self.source_file)

        def copy():
            if source_path.is_file():
                shutil.copy(source_path.as_posix(), dest_posix_path)
            elif source_path.is_dir():
                shutil.copytree(source_path.as_posix(), dest_posix_path)
            else:
                self._warn('Unsupported source. Source must be a file or directory')

        if dest_path.exists():
            if self.interactive:
                write_allowed = click.confirm(
                    click.style('Do you want to overwrite this {}?'.format(dest_posix_path), fg='yellow'))
            elif self.force:
                write_allowed = self.force
            else:
                self._warn('File {} exist. If you want to copy anyways, use `--force` flag.'.format(dest_posix_path))
                return
            if write_allowed:
                self._verbose('Overwriting file {}'.format(dest_posix_path))
                copy()
            else:
                self._verbose('Overwriting was disallowed')
        else:
            self._verbose('Writing new file {}'.format(dest_posix_path))
            copy()
