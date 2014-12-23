
from __future__ import print_function
import os
import pygit2
from package import Package
from misc import get_repo, YAMLFile

class PackageList(YAMLFile):
  def set_defaults(self):
    self['checksum'] = ''

class Remote(dict):
  def __init__(self, name, url, path):
    self['name'] = name
    self['url'] = url
    self['path'] = path

    self.url = get_repo(url)
    if (not (os.path.exists(self['path']))):
      self.repo = pygit2.clone_repository(self.url, self['path'])
    else:
      self.repo = pygit2.Repository(pygit2.discover_repository(self['path']))

    self.packages = PackageList()
    self.packages.load(os.path.join(self.repo.path, 'sarabi_packages'))
    self.update_packages()

  def has_package(self, package):
    return False # FIXME: ...

  def update_packages(self):
    if (self.packages['checksum'] != str(self.repo.head.target)):
      
      self.packages['checksum'] = str(self.repo.head.target)
      self.packages.save(os.path.join(self.repo.path, 'sarabi_packages'))

  def update(self):
    if (self.repo):
      self.repo.remotes[0].fetch()
      self.repo.create_reference('refs/remotes/origin/master', 'refs/heads/master', True)
      self.repo.checkout_head()
      self.update_packages()