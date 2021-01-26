from zipfile import ZipFile
import pandas as pd
import numpy as np
import voteFuncs as vf

import splitspy.nnet.nnet_algo as nnet_algorithm
import splitspy.outlines.outline_algo as outline_algorithm
import splitspy.nnet.distances as distances
from splitspy.splits.basic_split import split_dist
from splitspy.graph import draw

from subprocess import Popen


# Unzip all data
data_dir = 'voteData'
output_dir = 'voteData'
# Create a ZipFile Object and load sample.zip in it
with ZipFile(data_dir+'/voteData.zip', 'r') as zipObj:
   # Extract all the contents of zip file into same directory
   zipObj.extractall('voteData')


#Read in all voting data
Sall_votes = pd.read_csv(data_dir+'/Sall_votes_withPartyAndNames.csv')



#Distance matrix for 116th congress

cong = 116
Sall_votes_sub = Sall_votes[Sall_votes.congress == cong]

voteMat = vf.makeVoteMat(Sall_votes_sub)

labels, matrix = vf.makeDistMat(voteMat)
print('Pairwise Distances Calculated')


cycle, splits = nnet_algorithm.neighbor_net(labels, matrix)

print('Cycle and Splits Determined')


graph, angles = outline_algorithm.compute(labels, cycle, splits, rooted=False, out_grp="", alt=False)
print('Graph and Angles Determined')


fit = distances.ls_fit(matrix, split_dist(len(labels), splits))

im116 = 'test_outline.pdf'
draw.draw(output_dir+'/'+im116, graph, angles, fit, width = 1000, height = 800,m_left = 100, m_right = 100, m_top = 100, m_bot = 100, font_size = 12, scale_factor =5)
print('Graph Image Generated')

#Show plot
filename = output_dir+'/'+im116
Popen('open %s' % filename,shell=True)

#Add code for NEXUS output/SplitsTree5 compatible output



