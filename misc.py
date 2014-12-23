
import os
try:
    import yaml
    config_ext = '.yml'
except ImportError:
    import json as yaml
    config_ext = '.json'

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

class YAMLFile(dict):
  def __init__(self, filename = None, **kwds):
    super(YAMLFile, self).__init__(**kwds)

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
