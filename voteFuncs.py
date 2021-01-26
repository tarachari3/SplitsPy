from scipy.spatial.distance import pdist, squareform
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
    df['name'] = [convertName(i) for i in df['name']]

    df[nameID] = [str(i) +'_'+ str(j) for i, j in zip(df['name'], df['party'])] 

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



