from dateutil.parser import *
str1 = '7.54am'
try:
  dt = parse(str1)
  print "Ney"
except:
  print 'Yay'