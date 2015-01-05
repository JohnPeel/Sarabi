
import os
import shutil
import stat
try:
    import yaml
    config_ext = '.yml'
except ImportError:
    import json as yaml
    config_ext = '.json'

from strings import *

ignored_paths = ['.git']

class EPackageNotFound(Exception):
  pass
class EAmbiguousAtom(Exception):
  def __init__(self, valid_packages):
    self.valid_packages = valid_packages
    message = PACKAGE_TOO_AMBIGUOUS % len(valid_packages)
    message += '\n\n'
    for package in valid_packages:
      message += '\n  '.join(package.info())
      message += '\n'
    message += '\n'
    
    super(EAmbiguousAtom, self).__init__(message)

def get_default_config(program):
  (path, executable) = os.path.split(program)
  return os.path.abspath(os.path.join(path, os.path.splitext(executable)[0] + config_ext))

def get_repo(repo):
  if (repo[:7] == 'github:'):
    return 'https://github.com/%s.git' % repo[7:]
  if (repo[:4] == 'git:'):
    return repo[4:]
  return repo

def parse_package_atom(package):
  remote = None
  if ('::' in package):
    (package, remote) = package.split('::', 2)

  catagory = None
  if ('/' in package):
    (catagory, package) = package.split('/', 2)

  version = None
  if ('-' in package):
    (package, version) = package.split('-', 2)

  return {
      'catagory': catagory,
      'name': package,
      'version': version,
      'remote': remote
    }

def listdir(dir):
  return [os.path.relpath(os.path.join(dp, f), dir) for dp, dn, fn in os.walk(dir) for f in fn]
  
def copytree(src, dst, symlinks = False, ignore = None):
  if not os.path.exists(dst):
    os.makedirs(dst)
    shutil.copystat(src, dst)
  lst = os.listdir(src)
  if ignore:
    excl = ignore(src, lst)
    lst = [x for x in lst if x not in excl]
  for item in lst:
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if symlinks and os.path.islink(s):
      if os.path.lexists(d):
        os.remove(d)
      os.symlink(os.readlink(s), d)
      try:
        st = os.lstat(s)
        mode = stat.S_IMODE(st.st_mode)
        os.lchmod(d, mode)
      except:
        pass
    elif os.path.isdir(s):
      copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)    

class ConfDict(dict):
  def __init__(self, filename = None, **kwds):
    super(ConfDict, self).__init__(**kwds)

    self.set_defaults()

    if filename and os.path.exists(filename):
      self.load(filename)
  
  def __del__(self):
    if hasattr(self, 'filename') and self.filename:
      self.save()

  def set_defaults(self):
    pass
  
  def load(self, filename):
    if (os.path.exists(filename)):
      self.filename = filename
      with open(filename, 'r') as file:
        self.update(yaml.load(file))

  def save(self, filename = None):
    if (not filename):
      filename = self.filename
    with open(filename, 'w') as file:
      if (config_ext == '.yml'):
        yaml.dump(dict(self), file, default_flow_style=False)
      else:
        yaml.dump(dict(self), file, indent=4, separators=(',', ': '))
