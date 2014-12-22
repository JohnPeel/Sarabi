
from __future__ import print_function
import yaml

class FileList(dict):
  pass # Could be pulled from git, or get files and create? hmmm...

class PackageFile(dict):
  def __init__(self, name, description, repo, branch = 'master', commit = 'HEAD', files = {}, depends = []):
    self.parent_repo = parent_repo
    self['name'] = name
    self['description'] = description
    self['repo'] = repo
    self['branch'] = branch
    self['commit'] = commit
    self['files'] = files
    self['depends'] = depends

  def load(self, fileio):
    self = yaml.load(fileio)

class Package(dict):
  def __init__(self, name, catagory = None, version = None, remote = None, data = None):
    self['name'] = name
    self['catagory'] = catagory
    self['version'] = version
    self['remote'] = remote
    self.data = data

  def valid_atom(self, atom):
    def compare(item):
      return (not atom[item]) or (self[item] == atom[item])
    return compare('name') and compare('catagory') and compare('version') and compare(remote)

  def update(self):
    # Update repo, create new filelist, compare and update
    pass

  def install(self):
    # Pull repo, get files, and create filelist
    # Could also look for user patches?
    pass

  def uninstall(self):
    # Check filelist, remove files, delete repo
    pass