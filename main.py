from patriotproperties import *
from laserfiche import *

lfp = open('C:\\Users\\Victor\\Documents\\lfp.txt', 'r')
repoID = '052ecf80'
customerID = '672803730'
username = 'vlomba'
password = lfp.readline()
lfp.close()

if __name__ == '__main__':
	writeAllLots(allowDuplicates=True)
