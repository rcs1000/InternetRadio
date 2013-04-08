import json

def getPlaylist():

  with open('playlist.json', 'rb') as fp:
    data = json.load(fp)

  fp.close()
  return data
