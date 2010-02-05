#!/usr/bin/env python
# encoding: utf-8
"""
gitSave.py

Created by Daniel O'Donovan on 2010-01-21.
Copyright (c) 2010 University of Cambridge. All rights reserved.
"""

import os

from git import Git, Repo

# git error exceptions (not functions)
from git import InvalidGitRepositoryError, NoSuchPathError, GitCommandError

# import askString popup 
from memops.gui.DataEntry import askString

class GitHandler(object):
  """ 
  Git backend using GitPython:
    Similar to the rcsfield gitcore code
  """
  def __init__(self, repoLocation, debug=False):
    self.repoLocation = os.path.normpath(repoLocation)
    self.repo = None
    self.debug = debug

    self.initiate()

  def initiate(self):
    """ Initiate git repository (or access current) at repoLocation """
    if not os.path.exists(self.repoLocation):
        os.makedirs(self.repoLocation)

    try:
      repo = Repo(self.repoLocation)
    except (InvalidGitRepositoryError, NoSuchPathError, GitCommandError):
      if self.debug: print 'Repository not found at %s:\ncreating repo' % (self.repoLocation)
      git = Git(self.repoLocation)
      git.init()
      repo = Repo(self.repoLocation)

    self.repo = repo

  def commitAll(self):
    """ 
    commit ALL current changes to local git repo 
      In the long term, we should probably choose what to track
    """
    if not self.repo:
      self.initiate()

    repo = self.repo

    try:
      repo.git.add( os.path.join(self.repoLocation, '.') )
    except:
      raise
    message = askString( 'git commit -m', 'Please enter your git commit message (blank for default)')
    if not message:
      repo.git.commit(message='Auto git commit CCPN project')
    else:
      repo.git.commit(message=message)

def p( txt ):
  print txt

# Register all Callbacks with appropriate functions
def registerInit( top ):
  """ Init git repo """
  pass
  # top.registerCallback( 'init', lambda project: gitInit( project ) )

def registerSave( top ):
  """ Save git repo """
  top.registerCallback( 'save', lambda project: gitSave( project ) )

def registerClose( top ):
  """ Close using git """
  pass
  # top.registerCallback( 'close', lambda project: p( '*** CLOSE ***') )

# Functions for handling the git repos
# def gitInit( project ):
#   """ gitInit """
#   dataRepository = project.memopsRoot.findFirstRepository(name='userData')
#   
#   print 'init or open git repo at %s' % (dataRepository.url.dataLocation)
#   git = GitHandler( dataRepository.url.dataLocation, debug=True )
#   git.initiate()

def gitSave( project ):
  """ gitSave """
  dataRepository = project.memopsRoot.findFirstRepository(name='userData')
  print 'Commiting to git repo at %s' % (dataRepository.url.dataLocation)
  git = GitHandler( dataRepository.url.dataLocation, debug=True )
  git.commitAll()


# this function needs to be imported from the macro to init all Callbacks
def initGitRepoSave( argServer ):

  top = argServer.parent

  try:
    registerInit( top )
    registerSave( top )
    registerClose( top )

    print 'CCPN Git save routines initialised'

  except:

    print 'Couldn\'t start CCPN Git routines'

# def initGitRepoSave( top ):
# 
#   registerInit( top )
#   registerSave( top )
#   registerClose( top )
# 
#   print 'git Init/Save/Close set'


if __name__ == '__main__':

  print 'gitSave Macro: You probably don\'t want to call this from the command line!'

