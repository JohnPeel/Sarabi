
from __future__ import print_function
import os
import shutil
from misc import ConfDict, ignored_paths, copytree, listdir
from download import DownloadLink

class FileList(ConfDict):
  def __init__(self, files):
    self['files'] = files

class PackageFile(ConfDict):
  def __init__(self, name = '', description = '', uri  = '', files = {}, depends = []):
    self['name'] = name
    self['description'] = description
    self['uri'] = uri
    self['files'] = files
    self['depends'] = depends

class Package(dict):
  def __init__(self, parent, name, catagory, version, remote, package_file):
    self.parent = parent
    self['name'] = name
    self['catagory'] = catagory
    self['version'] = version
    self['remote'] = remote
    
    self.package_file = PackageFile()
    self.package_file.load(package_file)
  
  def info(self):
    return [
             self.get_atom(True), 
             'Name: %s' % self.package_file['name'], 
             'Description: %s' % self.package_file['description'],
             'Depends: %s' % self.package_file['depends']
           ]
  
  def get_atom(self, with_version=False, with_remote=True):
    return '%s/%s%s%s' % (self['catagory'], self['name'], '-' + self['version'] if with_version else '','::' + self['remote'] if with_remote else '') 

  def valid_atom(self, atom):
    def compare(item):
      return (not atom[item]) or (self[item] == atom[item])
    return compare('name') and compare('catagory') and compare('version') and compare('remote')

  def update(self):
    return self.uninstall(False) and self.install()

  def install(self):
    # FIXME: DEPENDS!!!
  
    path = os.path.normpath(os.path.join(self.parent.config['path'], 'packages', self.get_atom(True, False)))
    download = DownloadLink(self.package_file['uri'], path)
    download.process()
    # TODO: user patches?
    
    tmp_path = os.path.normpath(os.path.join(self.parent.config['path'], 'temp', self.get_atom(True, False)))
    try:
      shutil.rmtree(tmp_path)
    except:
      pass
    os.makedirs(tmp_path)

    for root, dirs, files in os.walk(path, True):
      for ignored_path in ignored_paths:
        if ignored_path in dirs:
          dirs.remove(ignored_path)
      
      for file in files:
        rel_file = os.path.relpath(os.path.join(root, file), path).replace('\\', '/')
        if (rel_file in self.package_file['files']):
          shutil.copy(os.path.join(root, file), os.path.join(tmp_path, self.package_file['files'][rel_file]))
      
      rel_root = os.path.relpath(root, path).replace('\\', '/')
      if (rel_root in self.package_file['files']):
        copytree(root, os.path.join(tmp_path, self.package_file['files'][rel_root]), ignore=shutil.ignore_patterns('.git'))
    
    filelist = FileList(listdir(tmp_path))
    filelist.save(os.path.join(path, self['name'] + '.filelist'))
    
    success = False
    try:
      copytree(tmp_path, self.parent.config['simba_path'])
      success = True
      shutil.rmtree(tmp_path)
    except:
      pass
    return success
    
  def uninstall(self, delete=True):
    path = os.path.normpath(os.path.join(self.parent.config['path'], 'packages', self.get_atom(True, False)))
    if os.exists(os.path.join(path, self['name'] + '.filelist')):
      filelist = FileList()
      filelist.load(os.path.join(path, self['name'] + '.filelist'))
      # FIXME: remove files in filelist.files
    
    if delete:
      pass #shutil.rmtree(path)