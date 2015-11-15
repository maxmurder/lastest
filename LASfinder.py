import sys
import getopt
import numpy
import laspy
import re

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

    return vertlist
    
def main(argv):
    
    inputfile = ''
    vertsfile = ''
    outputfile = ''

    #get the arguments
    try:
        opts, args = getopt.getopt(argv,"hi:v:o:")
    except getopt.GetoptError:
        print 'LASfinder.py -i <inputfile.las> -v <boundingVericiesFile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'LASfinder.py -i <inputfile.las> -v <boundingVericiesFile> -o <outputfile>'
            sys.exit(1)
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-v"):
            vertsfile = arg
        elif opt in ("-o"):
            outputfile = arg
    
    #get the box verticies
    verts = ParseBounds(vertsfile)
    
    #open the 
    ifile = laspy.file.File(inputfile, mode = "r")
    
if __name__ == "__main__":
    main(sys.argv[1:])

