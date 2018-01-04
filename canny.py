# -*- coding: utf-8 -*-

import argparse
import cv2

def cannyEdge():
    global img, minT, maxT
    edge = cv2.Canny(img, minT, maxT)
    cv2.imshow("edges", edge)
    
def adjustMinT(v):
    global minT
    minT = v
    cannyEdge()
    
def adjustMaxT(v):
    global maxT
    maxT = v
    cannyEdge()

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename")
args = parser.parse_args()

img = cv2.imread(args.filename) #, cv2.IMREAD_GRAYSCALE
#img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.namedWindow("edges", cv2.WINDOW_NORMAL)
minT = 30
maxT = 150
cv2.createTrackbar("minT", "edges", minT, 255, adjustMinT)
cv2.createTrackbar("maxT", "edges", maxT, 255, adjustMaxT)

cannyEdge()
cv2.waitKey(0)
