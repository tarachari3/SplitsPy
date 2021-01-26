from zipfile import ZipFile
import pandas as pd
import numpy as np
import voteFuncs as vf

import splitspy.nnet.nnet_algo as nnet_algorithm


# Unzip all data
data_dir = 'voteData'
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

#print(len(voteMat.index.values.tolist()))
labels, matrix = vf.makeDistMat(voteMat)
print('Pairwise Distances Calculated')
#print(matrix)
#print(type(matrix))

cycle, splits = nnet_algorithm.neighbor_net(labels, matrix)

print('Cycle and Splits Determined')
#print(splits)

#graph, angles = splitspy.outlines.outline_algo.compute(labels, cycle, splits, rooted=rooted, out_grp=out_grp, alt=alt)
#draw.draw(outfile, graph, angles, fit, win_width, win_height,m_left, m_right, m_top, m_bot, font_size)
