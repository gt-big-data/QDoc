import os

def loadLastStamp(name):
	path = 'stamps/'+name+'.txt'
	if os.path.isfile(path):
		f = open(path)
		txt = f.read()
		return float(txt)

	return 0

def saveLastStamp(name, stamp):
	path = 'stamps/'+name+'.txt'
	f = open(path,'w')
	f.write(str(stamp))