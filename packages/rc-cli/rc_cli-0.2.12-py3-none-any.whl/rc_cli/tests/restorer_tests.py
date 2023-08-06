import unittest

import os
import pathlib
import json


setup_path = pathlib.Path(os.path.dirname(os.path.relpath(__file__)))

from rc_cli.restore import restorer

from rc_cli.gitlab.groups_api import GroupsApi
from rc_cli.gitlab.projects_api import ProjectsApi
from rc_cli.gitlab.users_api import UsersApi
from unittest.mock import MagicMock
from unittest.mock import patch

import requests
import click
from click.testing import CliRunner

class RestorerTests(unittest.TestCase):

    def setUp(self):
        self.restore_directory = './restoreDirectory'
        self.group_name = 'testGroup'
        self.prefixes = (('prefix1'), ('prefix2'))
        self.token = '123456789'
        self.stage_mode = True
        self.config = ""

    def create_restorer(self, user):
        return restorer.Restorer(self.config, self.restore_directory, self.group_name, self.prefixes, self.token, user,self.stage_mode)

    def create_files(self):
      os.mkdir('repo_dir_with_prefix')
      os.mkdir('repo_dir_with_prefix/prefix1_test')
      os.mkdir('repo_dir_with_prefix/test1')
      open('repo_dir_with_prefix/test.txt', 'w')
      os.mkdir('repo_dir_without_prefix')
      os.mkdir('repo_dir_without_prefix/test1')
      os.mkdir('repo_dir_without_prefix/test2')
      open('repo_dir_without_prefix/test3.txt', 'w')

    def test_get_restorable_projects_some_user_with_prefix(self):
      user = 'Something'

      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = 'repo_dir_with_prefix'
        rest = self.create_restorer(user)
        rest._verbose = MagicMock()
        rest._Restorer__get_project_components = MagicMock(return_value=(None, 'Something'))

        ret = rest._Restorer__get_restorable_projects()

        rest._verbose.assert_called()
        self.assertEqual(rest._Restorer__get_project_components.call_count, 1)
        self.assertEqual(len(ret), 1)

    def test_get_restorable_projects_no_user_with_prefix(self):
      user = None
      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = 'repo_dir_with_prefix'
        rest = self.create_restorer(user)
        rest._verbose = MagicMock()
        rest._Restorer__get_project_components = MagicMock(return_value=(None, 'Something'))

        ret = rest._Restorer__get_restorable_projects()

        rest._verbose.assert_called()
        self.assertEqual(rest._Restorer__get_project_components.call_count, 0)
        self.assertEqual(len(ret), 1)

    def test_get_restorable_projects_no_user_no_prefix(self):
      user = None
      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = 'repo_dir_without_prefix'
        rest = self.create_restorer(user)
        rest._verbose = MagicMock()
        rest._Restorer__get_project_components = MagicMock(return_value=(None, 'Something'))

        ret = rest._Restorer__get_restorable_projects()

        rest._verbose.assert_called()
        self.assertEqual(rest._Restorer__get_project_components.call_count, 0)
        self.assertEqual(len(ret), 0)

    @patch(__name__ + '.GroupsApi.search_groups')
    def test_get_parent_group_bad_status(self, search_groups):
        search_groups.return_value=(None, 1000)
        rest = self.create_restorer(None)
        rest._error = MagicMock('Not Important')

        header = 'Header'

        try:
            rest._Restorer__get_parent_group(header)
            self.fail()
        except:
          rest._error.assert_called_with('Could not find group testGroup')
          self.assertTrue(True)

    @patch(__name__ + '.GroupsApi.search_groups')
    def test_get_parent_group_no_group_in_headers(self, search_groups):

      dict = json.loads(json.dumps({"name": 'Nope'}))
      groups = []
      groups.append(dict)

      search_groups.return_value=(groups, requests.codes.ok)

      rest = self.create_restorer(None)
      rest._error = MagicMock()

      header = {}
      header['Fail one'] = 'Group 1'
      header['Fail two'] = 'Group 2'

      try:
        rest._Restorer__get_parent_group(header)
        self.fail()
      except:
        search_groups.assert_called_with('testGroup', header)
        rest._error.assert_called_with('Group testGroup does not exists')
        self.assertTrue(True)

    @patch(__name__ + '.GroupsApi.search_groups')
    def test_get_parent_group_success(self, search_groups):

      dict = json.loads(json.dumps({"name": self.group_name}))
      groups = []
      groups.append(dict)

      search_groups.return_value = (groups, requests.codes.ok)

      rest = self.create_restorer(None)
      rest._verbose = MagicMock(return_value = 'None')

      header = {}
      header['Fail one'] = 'Group 1'
      header[self.group_name] = 'Group 2'

      ret = rest._Restorer__get_parent_group(header)

      self.assertEqual(ret, dict)

    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_projects_to_restore_invalid_status(self, get_group_projects):
      get_group_projects.return_value = (None, 1000)

      rest = self.create_restorer(None)
      rest._error = MagicMock()

      header = {'Test': 'Test'}
      path = pathlib.Path()
      paths = {path}

      try:
        rest._Restorer__get_projects_to_restore(paths, 'Group 1', header)
        self.fail()
      except:
        rest._error.assert_called_with('Failed to find projects for parent_group')

    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_projects_to_restore_1_project(self, get_group_projects):

      dict = json.loads(json.dumps({"name": 'Project 1'}))
      dict2 = json.loads(json.dumps({"name": 'Project 2'}))
      jsonList = [dict, dict2]

      get_group_projects.return_value=(jsonList, requests.codes.ok)

      rest = self.create_restorer(None)
      rest._success = MagicMock()
      rest._warn = MagicMock()
      rest._verbose = MagicMock()
      rest._Restorer__get_repository_name_from_path = MagicMock(side_effect=['Project 1', 'Nope'])

      header = {'Test': 'Test'}
      paths = {'path1', 'path2'}
      ret = rest._Restorer__get_projects_to_restore(paths, 'Group 1', header)

      rest._success.assert_called()
      rest._warn.assert_called()
      rest._verbose = MagicMock()
      self.assertTrue(ret.__contains__('path2') != ret.__contains__('path1'))

    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_projects_to_restore_2_project(self, get_group_projects):

      dict = json.loads(json.dumps({"name": 'Project 1'}))
      dict2 = json.loads(json.dumps({"name": 'Project 2'}))
      jsonList = [dict, dict2]

      get_group_projects.return_value=(jsonList, requests.codes.ok)

      rest = self.create_restorer(None)
      rest._success = MagicMock()
      rest._warn = MagicMock()
      rest._verbose = MagicMock()
      rest._Restorer__get_repository_name_from_path = MagicMock(side_effect=['Nope', 'Nope'])

      header = {'header1': 'header2'}
      paths = {'path1', 'path2'}
      ret = rest._Restorer__get_projects_to_restore(paths, 'Group 1', header)

      rest._success.assert_called()
      rest._warn.assert_not_called()
      rest._verbose.assert_called()
      self.assertTrue(ret.__contains__('path2') and ret.__contains__('path1'))

    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_projects_to_restore_0_project(self, get_group_projects):

      dict = json.loads(json.dumps({"name": 'Project 1'}))
      dict2 = json.loads(json.dumps({"name": 'Project 2'}))
      jsonList = [dict, dict2]

      get_group_projects.return_value=(jsonList, requests.codes.ok)

      rest = self.create_restorer(None)
      rest._success = MagicMock()
      rest._warn = MagicMock()
      rest._verbose = MagicMock()
      rest._Restorer__get_repository_name_from_path = MagicMock(side_effect=['Project 1', 'Project 2'])

      header = {'header1': 'header2'}
      paths = {'path1', 'path2'}
      ret = rest._Restorer__get_projects_to_restore(paths, 'Group 1', header)

      rest._success.assert_called()
      rest._warn.assert_called()
      rest._verbose.assert_called()
      self.assertEqual(ret, [])

    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_projects_to_restore_0_current_projects(self, get_group_projects):

      get_group_projects.return_value=([], requests.codes.ok)

      rest = self.create_restorer(None)
      rest._success = MagicMock()
      rest._warn = MagicMock()
      rest._verbose = MagicMock()

      rest._Restorer__get_repository_name_from_path = MagicMock(side_effect=['Project 1', 'Project 2'])

      header = {'header1': 'header2'}
      paths = {'path1', 'path2'}
      ret = rest._Restorer__get_projects_to_restore(paths, 'Group 1', header)

      rest._success.assert_called()
      rest._warn.assert_not_called()
      rest._verbose.assert_called()
      self.assertTrue(ret.__contains__('path2') and ret.__contains__('path1'))

    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_projects_to_restore_0_paths(self, get_group_projects):

      get_group_projects.return_value=([], requests.codes.ok)

      rest = self.create_restorer(None)
      rest._success = MagicMock()
      rest._warn = MagicMock()
      rest._verbose = MagicMock()
      rest._Restorer__get_repository_name_from_path = MagicMock(side_effect=['Project 1', 'Project 2'])

      header = {'header1': 'header2'}
      paths = {}

      ret = rest._Restorer__get_projects_to_restore(paths, 'Group 1', header)

      rest._success.assert_called()
      rest._warn.assert_not_called()
      rest._verbose.assert_called()
      self.assertEqual(ret, [])

    def test_restore_from_backup_no_projects(self):

      rest = self.create_restorer(None)
      rest._verbose = MagicMock()

      header = {'header1': 'header2'}
      projects_to_restore = {}
      parent_group_id = 'Group 1'

      ret = rest._Restorer__restore_from_backup(parent_group_id, projects_to_restore, header)
      rest._verbose.assert_called()
      self.assertEqual(ret, [])


    #-------------------------------------IMPORTANT----------------------------------------------------#
    ## Possible Bug found.  If the nested function get_user_object returns null, then the code will fail
    @patch(__name__ + '.UsersApi.search_user_by_username')
    def test_configue_project_bad_search_user_response(self, search_user_by_username):

      user1 = {"username": 'user', 'password': 'pass'}

      user2 = {'username': 'no', 'password': 'yes'}
      data = [user1, user2]

      search_user_by_username.return_value=(data, 1000)

      rest = self.create_restorer(None)
      rest._verbose = MagicMock()
      rest._error = MagicMock()
      header = {'header1': 'header2'}
      master_one = {'id': 'Master 1'}
      masters = [master_one]

      project_data = {('Master 1', 'User 1'), ('Dummy', 'User 2')}
      try:
        ret = rest._Restorer__configure_projects(masters, project_data, header)
        self.fail()
      except:
        rest._verbose.assert_called()
        rest._error.assert_called()

    @patch(__name__ + '.UsersApi.search_user_by_username')
    def test_configue_project_username_not_available(self, search_user_by_username):

      user1 = {"username": 'user', 'password': 'pass'}

      user2 = {'username': 'no', 'password': 'yes'}
      data = [user1, user2]

      search_user_by_username.return_value=(data, requests.codes.ok)

      rest = self.create_restorer(None)
      rest._verbose = MagicMock()
      rest._warn = MagicMock()
      header = {'header1': 'header2'}
      master_one = {'id': 'Master 1'}
      masters = [master_one]

      project_data = {('Master 1', 'User 1'), ('Dummy', 'User 2')}
      try:
        ret = rest._Restorer__configure_projects(masters, project_data, header)
        self.fail()
      except:
        rest._verbose.assert_called()
        rest._warn.assert_called()

    @patch(__name__ + '.UsersApi.search_user_by_username')
    @patch(__name__ + '.ProjectsApi.add_member')
    @patch(__name__ + '.ProjectsApi.get_protected_branches')
    @patch(__name__ + '.ProjectsApi.unprotect_branch')
    @patch(__name__ + '.ProjectsApi.get_branches')
    @patch(__name__ + '.ProjectsApi.protect_branch')
    @patch(__name__ + '.ProjectsApi.default_branch')
    def test_configure_project_complete(self, default_branch, protect_branch, get_branches, unprotect_branch,
                                        get_protected_branches, add_member, search_user_by_username):
    # def test_configure_project_complete(self, search_user_by_username, add_member, get_protected_branches, unprotect_branch,
    #                                     get_branches, protect_branch, default_branch):

      user1 = {"username": 'robotadmin', 'password': 'pass', 'id': 'adminId'}

      user2 = {'username': 'no', 'password': 'yes', 'id': 'user2Id'}
      data = [user1, user2]

      search_user_by_username.return_value = (data, requests.codes.ok)

      branch = {'name': 'master'}

      branch2 = {'name': 'other'}

      branch3 = {'name': 'feedback'}

      branches = [branch, branch2, branch3]

      add_member.side_effect=[("success", requests.codes.ok), ('fail', requests.codes.created), ("success", requests.codes.ok), ('fail', requests.codes.created)]
      get_protected_branches.side_effect=[(branches, requests.codes.ok), (branches, 1000)]
      unprotect_branch.side_effect=[('success', requests.codes.no_content), ('fail', 1000)]
      get_branches.side_effect=[(branches, requests.codes.ok), (branches, 1000)]
      protect_branch.side_effect=[('success', requests.codes.created), ('fail', 1000)]
      default_branch.side_effect=[(branches, requests.codes.ok), (branches, 1000)]

      rest = self.create_restorer(None)
      rest._verbose = MagicMock()
      rest._error = MagicMock()
      rest._success = MagicMock()
      rest._warn = MagicMock()
      rest._success
      header = {'header1': 'header2'}
      master_one = {'id': 'Master 1'}
      masters = [master_one]

      project_data = [{'id':'Master 1', 'user':user1}, {'id':'Dummy', 'user':user2}]

      ret = rest._Restorer__configure_projects(masters, project_data, header)

      rest._verbose.assert_called()
      rest._error.assert_called()
      rest._success.assert_called()
      rest._warn.assert_called()
      self.assertEqual(protect_branch.call_count, 2)
      rest._success.assert_called_with('Finished configuring all restored projects')

    #The below test fails because the filesystem does not like naming files with :
    # def test_write_restore_json(self):
    #
    #   rest = self.create_restorer(None)
    #   rest._success = MagicMock()
    #   rest._verbose = MagicMock()
    #
    #   user1 = {
    #     'id': 'id1',
    #     'name': 'name1',
    #     'user': 'user1'
    #   }
    #
    #   user2 = {
    #     'id': None,
    #     'name': 'name2',
    #     'user': 'user2'
    #   }
    #
    #   user3 = {
    #     'id': 'id3',
    #     'name': None,
    #     'user': 'user3'
    #   }
    #   project_data = [user1, user2, user3]
    #
    #   runner = CliRunner()
    #   with runner.isolated_filesystem():
    #     rest._Restorer__write_restore_json(project_data)
    #     rest._success.assert_called()
    #     rest._verbose.assert_called()

    def test_get_project_components(self):
      rest = self.create_restorer(None)
      rest._Restorer__get_repository_name_from_path = MagicMock(return_value='assignment-moor')
      ret = rest._Restorer__get_project_components('path')
      self.assertEqual(('assignment', 'moor'), ret)

    def test_get_repository_name_from_path(self):
      rest = self.create_restorer(None)
      path1 = pathlib.Path('moor.git')
      path2 = pathlib.Path('moor')
      self.assertEqual('moor', rest._Restorer__get_repository_name_from_path(path1))
      self.assertEqual('moor', rest._Restorer__get_repository_name_from_path(path2))

    def test_execute_no_directory(self):
      rest = self.create_restorer(None)
      rest._verbose = MagicMock()
      rest._error = MagicMock()

      try:
        rest.execute()
        self.fail()
      except:
        rest._verbose.assert_called()
        rest._error.assert_called()
        rest._error.assert_called_with('The restore_directory is not a directory')

    def test_execute_no_parent_group(self):
      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = 'repo_dir_with_prefix'
        rest = self.create_restorer(None)
        rest._verbose = MagicMock()
        rest._error = MagicMock()

        restorableProjects = ['One', 'Two']

        rest._Restorer__get_restorable_projects = MagicMock(return_value=restorableProjects)
        rest._Restorer__get_parent_group = MagicMock(return_value=None)
        try:
          rest.execute()
          self.fail()
        except:
          rest._verbose.assert_called()
          rest._error.assert_not_called()

    def test_execute_no_projects_to_restore(self):
      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = 'repo_dir_with_prefix'
        rest = self.create_restorer(None)
        rest._verbose = MagicMock()
        rest._error = MagicMock()
        rest._warn = MagicMock()

        restorableProjects = ['One', 'Two']

        parent_group = {
          'id': 'Group'
        }

        projects_to_restore = []

        rest._Restorer__get_restorable_projects = MagicMock(return_value=restorableProjects)
        rest._Restorer__get_parent_group = MagicMock(return_value=parent_group)
        rest._Restorer__get_projects_to_restore = MagicMock(return_value=projects_to_restore)
        try:
          rest.execute()
          self.fail()
        except:
          rest._verbose.assert_called()
          rest._error.assert_not_called()
          rest._warn.assert_called()

    @patch(__name__ + '.GroupsApi.get_group_members')
    def test_execute_bad_status_code(self, get_group_members):
      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = '../test_directories/repo_dir_with_prefix'


        get_group_members.return_value=(['Master 1'], 1000)
        rest = self.create_restorer(None)
        rest._verbose = MagicMock()
        rest._error = MagicMock()

        restorableProjects = ['One', 'Two']

        parent_group = {
          'id': 'Group'
        }

        projects_to_restore = ['Project 1', 'Project 2']

        rest._Restorer__get_restorable_projects = MagicMock(return_value=restorableProjects)
        rest._Restorer__get_parent_group = MagicMock(return_value=parent_group)
        rest._Restorer__get_projects_to_restore = MagicMock(return_value=projects_to_restore)
        rest._Restorer__restore_from_backup = MagicMock(return_value=None)

        try:
          rest.execute()
          self.fail()
        except:
          rest._verbose.assert_called()
          rest._error.assert_called()

    @patch(__name__ + '.GroupsApi.get_group_members')
    def test_execute_success(self, get_group_members):
      runner = CliRunner()
      with runner.isolated_filesystem():
        self.create_files()
        self.restore_directory = 'repo_dir_with_prefix'


        get_group_members.return_value=(['Master 1'], requests.codes.ok)
        rest = self.create_restorer(None)
        rest._verbose = MagicMock()
        rest._error = MagicMock()
        rest._success = MagicMock()

        restorableProjects = ['One', 'Two']

        parent_group = {
          'id': 'Group'
        }

        projects_to_restore = ['Project 1', 'Project 2']

        rest._Restorer__get_restorable_projects = MagicMock(return_value=restorableProjects)
        rest._Restorer__get_parent_group = MagicMock(return_value=parent_group)
        rest._Restorer__get_projects_to_restore = MagicMock(return_value=projects_to_restore)
        rest._Restorer__restore_from_backup = MagicMock(return_value=None)

        rest._Restorer__configure_projects = MagicMock()
        rest._Restorer__write_restore_json = MagicMock()

        try:
          rest.execute()
        except:
          rest._verbose.assert_called()
          rest._error.assert_not_called()
          rest._success.assert_called()