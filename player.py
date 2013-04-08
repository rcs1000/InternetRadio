import os
import time
from helpers import getPlaylist
status_file = 'status'

print('Internet Radio On: Awaiting Channel Instruction')

class mplayer:
  command = 'mplayer -slave -quiet -ao alsa '
  playing = False
  running = False

  def startUp(self, stream):
    import os,subprocess
    print self.command + stream
    self.mp = subprocess.Popen(self.command + stream, stdin=subprocess.PIPE, shell = True)
    self.playing = True
    self.running = True

  def loadChannel(self, stream):
    cmd = 'loadfile ' + stream + '\n'
    self.mp.stdin.write(cmd)
    self.playing = True

  def stopChannel(self):
    cmd = 'stop' + '\n'
    self.mp.stdin.write(cmd)
    self.playing = False
    self.running = False


class airplayer:
  # command = 
  playing = False
  running = False

  def startAirPi(self):
    os.system('shairport/shairport.pl -a AirPi &')
    self.playing = True
    self.running = True
    
  def stopAirPi(self):
    os.system('killall perl')
    self.playing = False
    self.running = False


def getToPlay():
  fh = open(status_file)
  output = fh.read()
  fh.close()
  return output

(mode, ino, dev, nlink, uid, gid, size, atime, last_modified_time, ctime) = os.stat(status_file)

mp = mplayer()
ap = airplayer()

while True:
  time.sleep(1)
  (mode, ino, dev, nlink, uid, gid, size, atime, new_last_modified_time, ctime) = os.stat(status_file)

  if new_last_modified_time != last_modified_time:
    last_modified_time = new_last_modified_time

    options = getPlaylist()
    choice = getToPlay()

    if choice == 'AirPlay Mode': 
      if ap.running == False:
        if mp.running == True and mp.playing == True:
          mp.stopChannel()

        ap.startAirPi()

    else:
      if ap.running == True:
        ap.stopAirPi()

      if mp.running == False:
        mp.startUp(options[choice])
      else:
        mp.loadChannel(options[choice])

