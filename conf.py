
from __future__ import print_function
import os
from misc import ConfDict

class Config(ConfDict):
  def set_defaults(self):
    self['remotes'] = {'master': 'github:JohnPeel/SarabiRepo'}
    self['world'] = []
    self['path'] = '.sarabi_info'
    self['simba_path'] = '.'

  def info(self):
    print("Data Path: %s\nSimba Path: %s" % (self['path'], self['simba_path']))
    print("Remotes -")
    for name, item in self['remotes'].items():
      print("  %s: %s" % (name, item))
    print("World: %s" % " ".join(self['world']))
