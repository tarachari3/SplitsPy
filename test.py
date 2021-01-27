
#NEED TO PIP INSTALL FisherExact 

from zipfile import ZipFile
import pandas as pd
import numpy as np
import voteFuncs as vf

import splitspy.nnet.nnet_algo as nnet_algorithm
#import splitspy.outlines.outline_algo as outline_algorithm
#import splitspy.nnet.distances as distances
#from splitspy.splits.basic_split import split_dist, split_dist_sets
#from splitspy.graph import draw
#from splitspy.splits import splits_io

#from subprocess import Popen


# Unzip all data
data_dir = 'voteData'
output_dir = 'voteData'
# Create a ZipFile Object and load sample.zip in it
with ZipFile(data_dir+'/voteData.zip', 'r') as zipObj:
   # Extract all the contents of zip file into same directory
   zipObj.extractall('voteData')


#Read in all voting data
Sall_votes = pd.read_csv(data_dir+'/Sall_votes_withPartyAndNames.csv')



#Distance matrix for 116th congress (****CONVERT TO A makeVis FUNCTION****)

cong = 116
Sall_votes_sub = Sall_votes[Sall_votes.congress == cong]


voteMat = vf.makeVoteMat(Sall_votes_sub)

labels, matrix = vf.makeDistMat(voteMat)
print('Pairwise Distances Calculated')


cycle, splits = nnet_algorithm.neighbor_net(labels, matrix)
print('Cycle and Splits Determined')


# graph, angles = outline_algorithm.compute(labels, cycle, splits, rooted=False, out_grp="", alt=False)
# print('Graph and Angles Determined')


# fit = distances.ls_fit(matrix, split_dist(len(labels), splits))

# im116 = 'test_outline.pdf'
# draw.draw(output_dir+'/'+im116, graph, angles, fit, width = 1000, height = 800,m_left = 100, m_right = 100, m_top = 100, m_bot = 100, font_size = 12, scale_factor =5)
# print('Graph Image Generated')

# #Show plot
# filename = output_dir+'/'+im116
# Popen('open %s' % filename,shell=True)

# #Add code for NEXUS output/SplitsTree5 compatible output
# nexus_file = output_dir+'/dist_116th.nex'
# splits_io.print_splits_nexus(labels, splits, cycle, fit, filename=nexus_file)


# Calculate distances from 'center' for all members
demDists, repDists = vf.centerDists(labels, splits)

# Calculate distances from 'center' for list of congresses


#Within party analysis
members = ["SANDERS_B_Ind","WARREN_E_Dem","KLOBUCHAR_A_Dem","BOOKER_C_Dem","HARRIS_K_Dem"]
dem_votes = Sall_votes_sub[Sall_votes_sub.party_code != 200]

voteMat = vf.makeVoteMat(dem_votes)

# labels, matrix = vf.makeDistMat(voteMat)
# cycle, splits = nnet_algorithm.neighbor_net(labels, matrix)
# graph, angles = outline_algorithm.compute(labels, cycle, splits, rooted=False, out_grp="", alt=False)
# fit = distances.ls_fit(matrix, split_dist(len(labels), splits))
# imDem = 'dem116_outline.pdf'
# draw.draw(output_dir+'/'+imDem, graph, angles, fit, width = 1000, height = 800,m_left = 100, m_right = 100, m_top = 100, m_bot = 100, font_size = 12, scale_factor =5)

# filename = output_dir+'/'+imDem
# Popen('open %s' % filename,shell=True)


# disagree = vf.calcDisagree(voteMat, members)
#Plot aggreement with rest of party

# pvals = vf.calcSplitVotPval(voteMat, members)
#Plot p-values for ranking vote contribution to split

# rep_votes = Sall_votes_sub[Sall_votes_sub.party_code == 200]



