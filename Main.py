import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

#Booleans, switch them on quickly to turn on print statements throughout.
debug = False
#debug = True

df = pd.read_csv('CleanedData.csv', index_col=0)

# rebuildLists takes in a master list, usually two values conjoined together,
# and spits out two lists that are split. Honestly only used to make the X and Y lists
# for the plotting parts of the matplotlib functions
# input: List similar to [[X,Y],[X,Y],[X,Y],[X,Y]]
# output: lists similar to [X.X.X.X] & [Y,Y,Y,Y]
def rebuildLists(zMaster):
	if(debug):
		print("Rebuilding now!\n")
	zChildOne, zChildTwo = [], []
	for i in range(len(zMaster)):
		zChildOne.append(zMaster[i][0])
		zChildTwo.append(zMaster[i][1])
	return zChildOne, zChildTwo

# parseCoord takes in a string object, meant to resemble a
# (XX.XXXX, YY.YYYY) format, and returns them both as float
# values. This is because the dataframe's "Location " column '
# is in a string fromat, cause, y'know... why make it easy?
def parseCoord(Str):
	tempStr = ""
	for X in range(len(Str)):
		if Str[X] == "(":
			continue
		elif Str[X] == ",":
			strOne = tempStr #Finished first number
			tempStr = ""
		elif Str[X] == " ":
			continue
		elif Str[X] == ")":
			strTwo = tempStr #Finished second number
		else:
			tempStr = tempStr + Str[X] #Add the actual unit to the string
	return float(strOne), float(strTwo)
	
# This is the function that should handle building the graphs themelves.
# The first bit, up until the end of the lastt elif statement is getting a range 
# of values for the graph's sake, like the x axis and y axis. It also populates '
# the lists containing the xCordinates and y cordinates.
# FYI xList, yList
def buildGraph(start, stop):
				#XMIN    XMAX   YMIN    YMAX
	ranges = [20000, -20000, 20000, -20000]
	xyList = []
	for X in range(start, stop):
		xCord, yCord = parseCoord(df["Location "][X])
		xyList.append([xCord, yCord])
		#checking to see new maxes and mins
		if xCord < ranges[0]:
			ranges[0] = xCord
		elif xCord > ranges[1]:
			ranges[1] = xCord
		if yCord < ranges[2]:
			ranges[2] = yCord
		elif yCord > ranges[3]:
			ranges[3] = yCord
	if(debug):
		print(ranges)
	
	#Calling to make the X & Y lists for the plotting functions
	xList, yList = rebuildLists(xyList)
	
	#Where your algorithm will most likely be called, yall can ignore my garbage here
	scaler = StandardScaler()
	X_scaled = scaler.fit_transform(xyList)
	dbscan = DBSCAN(eps=0.123, min_samples = 5)
	clusters = dbscan.fit_predict(X_scaled)
	# plot the cluster assignments
	plt.scatter(xList, yList, c=clusters, cmap="plasma")
	plt.xlabel("X cordinate")
	plt.ylabel("Y cordinate")
	plt.axis([ranges[0], ranges[1], ranges[2], ranges[3]])
	return ranges

#Running the functions down here
buildGraph(0,1000)

plt.show()