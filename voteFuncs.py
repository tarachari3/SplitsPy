from splitspy.splits.basic_split import split_dist, split_dist_sets
import splitspy.outlines.outline_algo as outline_algorithm
import splitspy.nnet.distances as distances
from splitspy.graph import draw
from splitspy.splits import splits_io

from scipy.spatial.distance import pdist, squareform
from FisherExact import fisher_exact
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import compress
from subprocess import Popen

import warnings
warnings.filterwarnings("ignore")

def convertParty(partyCode):
    """
    Parameters :
    partyCode : Party code number for member
    Returns :
    Str name for party affiliation
    """
    if partyCode == 100:
        return "Dem"
    elif partyCode == 200:
        return "Rep"
    else:
        return "Ind"

def convertVote(castCode):
    """
    Parameters :
    castCode : Code for vote type cast by member
    Returns :
    Real value (0, 0.5, or 1.0) for vote cast
    """
    if int(castCode) <= 3:
        return 1.0
    elif int(castCode) <= 6:
        return 0.0
    else:
        return 0.5


def convertName(name):
    """
    Parameters :
    name : Member's name (str)
    Returns :
    spltispy/NEXUS compatible name
    """
    comma = name.find(',')
    new = name[0:comma+3]

    new = new.replace("'","")
    new = new.replace("(","")
    new = new.replace(", ","_")
    new = new.replace(" ","_")

    return new



def makeVoteMat(df, nameID = 'plotID'):
    """
    Parameters :
    df : Raw, unmodified input vote pandas dataframe
    Returns :
    In-place modified dataframe, so names are splitspy/NEXUS compatible and votes are mapped to real values 0, 0.5, 1.0
    """

    df['party'] = [convertParty(i) for i in df['party_code']]
    df['vote'] = [convertVote(i) for i in df['cast_code']]
    df['fixName'] = [convertName(i) for i in df['name']]

    df[nameID] = [str(i) +'_'+ str(j) for i, j in zip(df['fixName'], df['party'])] 

    voteMat = df.pivot(index= nameID, columns='rollnumber', values='vote')

    #Remove members with na votes
    voteMat = voteMat.dropna(axis=0)

    return voteMat


def makeDistMat(df, names = 'plotID', metric='cityblock'):
    """
    Parameters :
    df : Compatible (format-wise) input vote pandas dataframe
    Returns :
    Distance matrix between all members
    """

    dist = squareform(pdist(df.values, 'cityblock')).tolist()
    labels = list(df.index.values.tolist())


    return labels, dist


def calcDisagree(voteMat, members):
    """
    Parameters :
    voteMat : Dataframe of votes from labeled members
    members : Set of members to split from rest of labels
    Returns :
    Dataframe with percent disagreement for all rollcall votes and shared vote by the members
    """

    labels = list(voteMat.index.values.tolist())
    disagree = pd.DataFrame()

    # Find pos of members in labels
    pos = [labels.index(m) for m in members]

    # Find cols where all pos have same vote
    subMat = voteMat.iloc[pos,:]
    bools = list(subMat.eq(subMat.iloc[0, :], axis=1).all(0))

    # Remove rows not in members, and filter cols
    allPos = range(0,len(labels))
    nonMems = [i not in pos for i in allPos]

    filtMat = voteMat.iloc[nonMems,bools]
    toCompMat = subMat.iloc[:,bools]

    # Calc frac agreement in rest of members
    boolMat = filtMat.eq(toCompMat.iloc[0, :], axis=1)
    fracAgree = boolMat.sum(axis=0)/len(nonMems)

    # Save Frac, Rollcall, Vote
    disagree['Frac'] = list(np.array(fracAgree))
    disagree['Rollcall'] = list(boolMat.columns)
    disagree['Vote'] = np.array(toCompMat.iloc[0, :])



    return disagree

#def plotDisagree(agreeMat,)


def calcSplitVotPval(voteMat, members):
    """
    Parameters :
    voteMat : Dataframe of votes from labeled members
    members : Set of members to split from rest of labels
    Returns :
    Dataframe of raw p-values for contribution of each rollcall vote (feature) to split and associate vote rollcall no.
    """

    labels = list(voteMat.index.values.tolist())
    # Find pos of members in labels
    pos = [labels.index(m) for m in members]
    allPos = range(0,len(labels))
    nonMems = [i not in pos for i in allPos]

    pvals = [0]*len(voteMat.columns)
    rollcalls = list(voteMat.columns)

    pval_df = pd.DataFrame()

    for i in range(0,len(voteMat.columns)):

        memVotes = voteMat.iloc[pos,i]
        nonMemVotes = voteMat.iloc[nonMems,i]

        memZero = sum(list(memVotes == 0.0))
        memHalf = sum(list(memVotes == 0.5))
        memOne = sum(list(memVotes == 1.0))

        nonMemZero = sum(list(nonMemVotes == 0.0))
        nonMemHalf = sum(list(nonMemVotes == 0.5))
        nonMemOne = sum(list(nonMemVotes == 1.0))



        pvalue = fisher_exact([[memZero, memHalf,memOne], [nonMemZero, nonMemHalf,nonMemOne]])
        pvals[i] = pvalue 

    pval_df['pval'] = pvals
    pval_df['Rollcall'] = rollcalls 

    return pval_df

# def plotFishers()

def centerDists(labels, splits):
    """
    Parameters :
    voteMat : Dataframe of votes from labeled members
    Returns :
    Two vectors, one for each set of center distances (for members on either side of 'center' split)
    """

    reps = ['_Rep' in i for i in labels]
    dems = ['_Rep' not in i for i in labels]
    taxPos = range(1,len(labels)+1)

    demDists = split_dist_sets(list(compress(taxPos, dems)), list(compress(taxPos, reps)), splits)
    repDists = split_dist_sets(list(compress(taxPos, reps)), list(compress(taxPos, dems)), splits)

    return demDists, repDists

# def plotCenterDists()

# def plotTimeDists()


# def makeVis(labels,cycle,splits,outfilePhylo,outfileNexus,width....):






