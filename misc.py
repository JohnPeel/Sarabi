
import os
import yaml

def get_default_config(program):
  (path, executable) = os.path.split(program)
  return os.path.abspath(os.path.join(path, os.path.splitext(executable)[0] + '.yml'))

def get_repo(repo):
  if (repo[:7] == 'github:'):
    return 'https://github.com/%s.git' % repo[7:]
  if (repo[:4] == 'git:'):
    return repo[4:]

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

class YAMLDict(dict):
  def load(self, filename):
    if (os.path.exists(filename)):
      with open(filename, 'r') as file:
        self = yaml.load(file)

  def save(self, filename):
    with open(filename, 'w') as file:
      yaml.dump(dict(self), file, default_flow_style=False)
