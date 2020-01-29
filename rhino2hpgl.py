#this script assumes rhino units set to inches
#and the drawing scaled to the size of the paper
#(a 10" long line in the model will plotted at 10" long on the paper)
#everything is drawn with pen 1 or 2, depending on the lay
#hpgl file saved in the same folder as this script called "outputxxxxx.hpgl" where xxxxx is a random series of numbers
import rhinoscriptsyntax as rs
import random
#hpglOut = file('./output'+str(random.randint(100000000,999999999))+'.hpgl', 'w')
#print hpglOut.tell()

hpglOut = file('C:\Users\William\Documents\hpgl\output'+str(random.randint(100000000,999999999))+'.hpgl', 'w')
allCurves =rs.ObjectsByType(4)

hpglOut.write('IN;\n')
#hpglOut.write('SP1;\n')

#first explode anypolycurves (that aren't polylines) -- an exception I forgot to mention in class
for curve in allCurves:
	if rs.IsPolyCurve(curve) and rs.CurveDegree (curve) >= 2 :
		rs.ExplodeCurves (curve, True)

allCurves =rs.ObjectsByType(4)

curvesByLayers = [[] for _ in range(6)]

for curve in allCurves:
	if rs.ObjectLayer(curve)=="1":
		curvesByLayers[0].append(curve)
	elif rs.ObjectLayer(curve)=="2":
		curvesByLayers[1].append(curve)
	elif rs.ObjectLayer(curve)=="3":
		curvesByLayers[2].append(curve)
	elif rs.ObjectLayer(curve)=="4":
		curvesByLayers[3].append(curve)
	elif rs.ObjectLayer(curve)=="5":
		curvesByLayers[4].append(curve)
	elif rs.ObjectLayer(curve)=="6":
		curvesByLayers[5].append(curve)
print len(curvesByLayers[0])

for idx, pencurves in enumerate(curvesByLayers):
	if not pencurves: continue
	pen = idx + 1
	hpglOut.write('SP'+str(pen)+';\n')
	for curve in pencurves:
		if rs.CurveDegree (curve) == 1: #polyline or line
			points=rs.CurveEditPoints(curve) #works for polyline or line
			#print 'line'
		elif rs.CurveDegree (curve) == 2 or rs.CurveDegree (curve) == 3: #curvy curve
			points = rs.DivideCurveLength(curve, .025)
			print 'curvy'
		if not points:
			#print 'found one very tiny curve, which is not exported'
			continue #means skip this iteration of the loop and go right to the next curve
		#pen up to the first point on line
		x = points[0][0]
		y = points[0][1]
		hpglOut.write('PU'+str(int(x*1000))+','+str(int(y*1000))+';\n')
		#pen down to every subsequent point
		i=1
		while i<len(points):
			x = points[i][0]
			y = points[i][1]
			hpglOut.write('PD'+str(int(x*1000))+','+str(int(y*1000))+';\n')
			i=i+1

hpglOut.write('SP0;\n')
hpglOut.close()

		