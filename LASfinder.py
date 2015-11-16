import sys
import laspy
import numpy
import getopt
import datetime
import math 
import re

def Modulus(p):
    return math.sqrt( p[0] * p[0] + p[1] * p[1] + p[2] * p[2] )

def CalcAngleSum(P, q):
    point1 = numpy.array([0,0,0])
    point2 = numpy.array([0,0,0])
    anglesum = 0;
    n = len(P)
    for i in range(0, n):
        #caclulate the points
        point1[0] = P[i][0] - q[0];
        point1[1] = P[i][1] - q[1];
        point1[2] = P[i][2] - q[2];
        
        point2[0] = P[(i+1)%n][0] - q[0];   
        point2[1] = P[(i+1)%n][1] - q[1];
        point2[2] = P[(i+1)%n][2] - q[2];
        
        #calculate moduli
        mod1 = Modulus(point1)
        mod2 = Modulus(point2)
                
        #check if we are on a node
        if(mod1 * mod2 <= 0.0000001):
            return math.pi * 2;
        else:
            #calculate the costheta
            costheta = (point1[0] * point2[0] + point1[1] * point2[1] + point1[2] * point2[2]) / (mod1 * mod2)
        anglesum += math.acos(min(1,max(costheta, -1)))
        
    return anglesum
        
def ParseBounds(vertsfile):
    #open vertlist file
    vert = open(vertsfile, 'r')
    vertstring = vert.read()
    vert.close()
    
    #parse vertlist
    vertlist = re.split(r']',vertstring)
    vertlist = [ re.sub(r'[\[\]\r\n]','', v) for v in vertlist ]
    vertlist = [ re.sub(r'(?<=.) +',',',v) for v in vertlist ]
    vertlist = [ re.sub(r' +','',v) for v in vertlist ]
    vertlist = [ re.split(r',', v) for v in vertlist ]
    vertlist = [ v for v in vertlist if not v[0] == '']
    vertlist = [ map(float, v) for v in vertlist ]
    
    return vertlist
    
def main(argv):
    
    inputfile = ''
    vertsfile = ''
    outputfile = ''

    #get the arguments
    try:
        opts, args = getopt.getopt(argv,"hi:v:o:")
    except getopt.GetoptError:
        print 'LASfinder.py -i <inputfile.las> -v <boundingVericiesFile> -o <outputfile.las>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'LASfinder.py -i <inputfile.las> -v <boundingVericiesFile> -o <outputfile.las>'
            sys.exit(1)
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-v"):
            vertsfile = arg
        elif opt in ("-o"):
            outputfile = arg
    
    #get the box verticies
    verts = ParseBounds(vertsfile)

    #open the las file
    ifile = laspy.file.File(inputfile, mode = "r")
    scale = ifile.header.scale[0]
    
    #calculate point in polygon
    keepPoints = [ p for p in ifile.points if CalcAngleSum(verts, [p[0][0]*scale,p[0][1]*scale,p[0][2]*scale]) >= math.pi * 2 ]

    #generate output file    
    if re.match(r'.*\.las', outputfile):
        ofile = laspy.file.File(outputfile,mode = "w", header = ifile.header)
        ofile.points = keepPoints
        ofile.close()
    else:
        ofile = open(outputfile, "w")
        print >> ofile, keepPoints
        ofile.close()
    ifile.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])

