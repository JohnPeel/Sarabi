
from __future__ import print_function
import os
from package import Package, PackageFile
from misc import ConfDict, EPackageNotFound, EAmbiguousAtom, ignored_paths
from download import DownloadLink
from strings import *

class Remote(dict):
  def __init__(self, parent, name, url, path):
    self.parent = parent
    self['name'] = name
    self['url'] = url
    self['path'] = path

    self.download = DownloadLink(url, path)
    self.download.process()
    
    self.packages = []
    self.update_packages()

  def get_packages(self, atom):
    valid_packages = []
    for package in self.packages:
      if package.valid_atom(atom):
        valid_packages.append(package)
    return valid_packages
  
  def has_package(self, atom):
    return (len(self.get_packages(atom)) > 0)
    
  def get_package(self, atom):
    valid_packages = self.get_packages(atom)
    vp_len = len(valid_packages)
    if vp_len < 1:
      raise EPackageNotFound()
    elif vp_len > 1:
      raise EAmbiguousAtom(valid_packages)
    else:
      return valid_packages[0]

  def update_packages(self):
    def process_package(path, catagory, package):
      filename = os.path.splitext(os.path.basename(path))[0]
      (file, version) = filename.split('-', 1)
      if (package == file):
        package = Package(self.parent, package, catagory, version, self['name'], path)
        self.packages.append(package)
      else:
        print('WARNING: ' + PACKAGE_INVALID_FILENAME % path)
    def process_package_dir(path, catagory, package):
      for file in os.listdir(path):
        process_package(os.path.join(path, file), catagory, package)
    def process_catagory_dir(path, catagory):
      for package_dir in os.listdir(path):
        process_package_dir(os.path.join(path, package_dir), catagory, package_dir)
    
    catagories = os.listdir(self['path'])
    for catagory in catagories:
      path = os.path.join(self['path'], catagory)
      if (os.path.isdir(path)) and (not (catagory in ignored_paths)):
        process_catagory_dir(path, catagory)

  def update(self):
    self.download.process(True)
    self.update_packages()