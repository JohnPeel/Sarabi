
from __future__ import print_function
import os
import yaml
from misc import YAMLDict

class Config(YAMLDict):
  def __init__(self, **kwds):
    super(Config, self).__init__(**kwds)

    # Defaults
    self['remotes'] = {'master': 'github:JohnPeel/SarabiRepo'}
    self['world'] = []
    self['path'] = '.sarabi_info'
    self['simba_path'] = '' # Current Directory

    if kwds.has_key('configfile'):
      self.load(kwds['configfile'])

  def info(self):
    print("Data Path: %s\nSimba Path: %s" % (self['path'], self['simba_path']))
    print("Remotes -")
    for name, item in self['remotes'].iteritems():
      print("  %s: %s" % (name, item))
    print("World: %s" % " ".join(self['world']))