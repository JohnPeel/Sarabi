
from __future__ import print_function
import os
import pygit2
from misc import copytree

class DownloadLink(object):
  def __init__(self, url, path):
    self.url = url
    self.path = os.path.normpath(path)
    
    try:
      os.makedirs(os.path.normpath(os.path.join(self.path, '..')))
    except:
      pass 
      
  def do_git(self, update = False):
    # TODO: Write support for url@branch or url@sha
    if (not (os.path.exists(self.path))):
      repo = pygit2.clone_repository(self.url[4:], self.path)
    else:
      repo = pygit2.Repository(pygit2.discover_repository(self.path))

    if (update):
      repo.remotes[0].fetch()
      repo.create_reference('refs/remotes/origin/master', 'refs/heads/master', True)
      repo.checkout_head()
    return repo

  def do_github(self, update = False):
    # TODO: Write support for url@branch or url@sha
    self.url = 'git:https://github.com/%s.git' % self.url[7:]
    return self.do_git(update)

  def do_https(self, update = False):
    return None #FIXME: Write this...

  def do_http(self, update = False):
    return self.do_https(update)

  def do_file(self, update = False):
    path = self.url[5:]
    copytree(path, self.path)

  def process(self, update = False):
    call = getattr(self, 'do_%s' % self.url[:self.url.find(':')])
    return call(update)
