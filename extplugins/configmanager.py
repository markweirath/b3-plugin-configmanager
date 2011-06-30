#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2005 www.xlr8or.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Changelog:
#

__version__ = '1.0.0'
__author__  = 'xlr8or'

import b3
import threading
import time
import os
import b3.events
import os.path

# from os.path
# isfile(path)
#    Return True if path is an existing regular file. This follows symbolic links, so both islink() and isfile() can be true for the same path.
#--------------------------------------------------------------------------------------------------
class ConfigmanagerPlugin(b3.plugin.Plugin):
  _map = None
  _mappath = None
  _gametype = None
  _gametypepath = None
  _typeandmap = None
  _typeandmappath = None
  _mainconfpath = ''
  _confpath = ''
  _modpath = ''
  _exec_delay = 15 # seconds after roundstart to execute the config
  _disablechecking = False


  def onStartup(self):
    """\
    Initialize plugin settings
    """
    # Register our events
    self.verbose('Registering events')
    self.registerEvent(b3.events.EVT_GAME_ROUND_START)

    self.debug('Started')


  def onLoadConfig(self):
    # load our settings
    self.verbose('Loading config')
    
    try:
        self._disablechecking = self.config.getbool('settings', 'disablechecking')
    except:
        pass

    self._confpath = self.console.getCvar('fs_homepath')
    if self._confpath != None:
      self._confpath = self._confpath.getString()
    
    self._modpath = self.console.getCvar('fs_game')
    if self._modpath != None:
      self._modpath = self._modpath.getString()
    else:
      self._modpath = 'main'

    # Not really needed but to make sure we don't get stuck in the CoD root dir.
    if self._modpath == '':
      self._modpath = 'main'

    self._confpath += '/' + self._modpath + '/'
    self.debug('GameConfigPath: %s' %(self._confpath))


  def onEvent(self, event):
    """\
    Handle intercepted events
    """
    if event.type == b3.events.EVT_GAME_ROUND_START:
      c = self.console.game
      self._typeandmap = 'b3_%s_%s.cfg' % (c.gameType, c.mapName)
      self._typeandmappath = '%sb3_%s_%s.cfg' % (self._confpath, c.gameType, c.mapName)
      self.debug('Type and Map Config: %s' %(self._typeandmappath))
      self._gametype = 'b3_%s.cfg' % (c.gameType)
      self._gametypepath = '%sb3_%s.cfg' % (self._confpath, c.gameType)
      self.debug('Gametype Config: %s' %(self._gametypepath))
      self._mainconfpath = '%sb3_main.cfg' % (self._confpath)
      self.debug('Main Config: %s' %(self._mainconfpath))
     
      t1 = threading.Timer(self._exec_delay, self.checkConfig)
      t1.start()
      

  def checkConfig(self):
    """\
    Check and run the configs
    """
    if not self._disablechecking:
        if os.path.isfile(self._typeandmappath):       # b3_<gametype>_<mapname>.cfg
          self.console.write('exec %s' % self._typeandmap)
          self.debug('Executing %s' %(self._typeandmappath))
        elif os.path.isfile(self._gametypepath):       # b3_<gametype>.cfg
          self.console.write('exec %s' % self._gametype)
          self.debug('Executing %s' %(self._gametypepath))
        elif os.path.isfile(self._mainconfpath):       # b3_main.cfg
          self.console.write('exec b3_main.cfg')
          self.debug('Executing %s' %(self._mainconfpath))
        else:
          self.debug('No matching configs found.')
    else:
        # forcing to execute configs even if they do not exist (remote B3 installs)
        self.console.write('exec b3_main.cfg')
        self.debug('Forcing %s' %(self._mainconfpath))
        # this method runs in a separate thread, so time.sleep() will not affect B3 core behavior
        time.sleep(1)
        self.console.write('exec %s' % self._gametype)
        self.debug('Forcing %s' %(self._gametypepath))
        time.sleep(1)
        self.console.write('exec %s' % self._typeandmap)
        self.debug('Forcing %s' %(self._typeandmappath))


if __name__ == '__main__':
  print '\nThis is version '+__version__+' by '+__author__+' for BigBrotherBot.\n'

