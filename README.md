# lastest

Author: Clayton Campbell
Date: 15-11-2015

Simple python script to find .las points within a bounding polygon.
Created as part of a code challenge for SarPoint.

Usage:
    LASfinder.py -i <inputfile.las> -v <boundingVericiesFile> -o <outputfile.las>
    
    Takes a .las file and a polygon verticies text file (see out.txt) as input. Outputs
    a plaintext file of points in X,Y,Z format.
