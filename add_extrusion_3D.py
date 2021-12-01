################################################################################
## This script converts a G-code file (.gcode) with X and Y and Z motion only ##
## and output a G-code file (.gcode) with added extrusion commands            ## 

import argparse
import copy
import math

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--dist2extrusion', help = '3D printer dependent, extrusion value per mm, default: 0.519078')
	parser.add_argument('-u', '--under_extrusion', help = 'coefficient for under extrusion, default: 1')
	parser.add_argument('-f', '--filename', help = 'file name of the G-code')
	parser.add_argument('-r', '--raise_amount', help = 'raise needle for x mm after embedding, default: 5 mm')
	args = parser.parse_args()
	return args


def getCoordinate(input):
	tmp = input
	tmp = tmp.replace(" ","")
	# print(tmp)
	xIndex = list(range(tmp.index("X")+1, tmp.index("Y")))
	yIndex = list(range(tmp.index("Y")+1, tmp.index("Z")))
	if tmp.count("F") < 1:
		zIndex = list(range(tmp.index("Z")+1, len(tmp)))
	else:
		zIndex = list(range(tmp.index("Z")+1, tmp.index("F")))
	x = float(tmp[xIndex[0]:xIndex[-1]+1])
	y = float(tmp[yIndex[0]:yIndex[-1]+1])
	z = float(tmp[zIndex[0]:zIndex[-1]+1])
	return [x,y,z]


def main(args):
	file = args.filename if args.filename else 'conical_helix.gcode'
	dist2extrusion = args.dist2extrusion if args.dist2extrusion else 0.519078
	under_extrusion = args.under_extrusion if args.under_extrusion else 1.0
	dist2extrusion *= under_extrusion
	raise_amount = args.raise_amount if args.raise_amount else 5
	output = "updated_" + file


	with open(file) as f: 
		content = f.read()

	print("length of content = %d" % len(content))
	looper = content.split('\n')
	print("number of lines in content = %d" % len(looper))
	counter = 0
	for line in looper:
		if "startFlag" in line:
			beginLine = counter + 1
			originLine = beginLine
		elif "endFlag" in line:
			endLine = counter -1
		counter += 1
	### get origin coordinate
	origin = getCoordinate(looper[originLine])
	print("origin coordiante = ",origin)

	### adding extrusion
	clown = ""
	counter = 0
	lastX, lastY, lastZ = origin[0], origin[1], origin[2]
	extrusion = 0
	for line in looper:
		if counter >= beginLine and counter <= endLine:
			try:
				goTo = getCoordinate(line)
			except:
				print(line)
			goToX, goToY, goToZ = goTo[0], goTo[1], goTo[2]
			distance = math.sqrt((goToX - lastX)**2 + (goToY - lastY)**2 +  (goToZ - lastZ)**2)
			extrusion += distance * dist2extrusion
			adder = "   E"+str(extrusion)
			line = line.replace("   ", "")
			line = line.replace("  ", "") # Makerbot Replicas does NOT recognize space between XYZ and the numbers
			line += adder
			clown += line
			lastX, lastY, lastZ = goToX, goToY, goToZ
		else:
			if "(" in line or "M73" in line or ("G0" in line and "X" not in line) or "T1" in line or "M3" in line or "M9" in line or "F150" in line or "G1 Z" in line or "S6" in line or "G0 X" in line:
				line = ";" + line # skipping all lines that contains "(" or ")", due to the fact that they won't be recognized
			elif "F120" in line:
				line = "G1 " + line
			elif "G0" in line and "X" in line:
				line = line.replace("G0", "G1")
				line = line.replace("   ", "")
				line += " F50"
			line = line.replace("  ", "") # Makerbot Replicas does NOT recognize space between XYZ and the numbers
			clown += line
		clown += "\n"
		counter +=1
	# 
	print("total extrusion = ", extrusion / dist2extrusion, "mm")
	if raise_amount:
		extrusion += raise_amount * dist2extrusion
		raiseCommand = "G1   Z" + str(raise_amount) + "   E" + str(extrusion)
		clown += raiseCommand
	open(output, "w").write(clown)
	print("G-code updated", output)

if __name__ == "__main__":
	args = parse()
	main(args)


