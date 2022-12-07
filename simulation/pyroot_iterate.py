import ROOT as root
import numpy as np


f = root.TFile("RealData.root")
myTree = f.Get("tree")
for entry in myTree:         
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     events = entry.events