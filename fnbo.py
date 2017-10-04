"""
    Author: Bob Little
    Date  : October 1st, 2017
    Description: A module to handle FNBO data.  Uses u2py functionality
    
    Files:
        FNBO.XREF
        
    Notes:
    This works only when U2 has a python license.  It also only works from a 
    command line and in the correct directory.
    On my machine, I have a UniVerse account set up as
    /usr/local/madev
    In this directory, I have a source directory:
    rdlpy
    From a command line, in the /usr/local/madev directory I can do
        /usr/uv/python/bin/python3
    Which puts me at a python command prompt:
        >>>
    Then:    
        >>> from rdlpy import fnbo
        >>> fnbo.findByArn(fnbo.textArn)
        >>>
        
"""
import u2py

fnboXrefFile = u2py.File("FNBO.XREF")
testArn = "1010955650293918"

def findByArn(arn):
    """
    Get a list of FNBO.XREF record ids for a specific ARN
    Args:
        idList - A single ARN
    Returns:
        A python list of FNBO.XREF records
    """   
    selList = u2py.List(0,fnboXrefFile,"ARN.IDX",arn)
    idList = []
    for item in selList:
        tid = selList.next()
        if tid != None:
            idList.append(tid)
    idList.pop()            
    recList = getTransactionList(idList)
    return recList

def findByMember(memberId):
    """
    Get a list of FNBO.XREF record ids for a specific member id.
    Args:
        idList - A single member id
    Returns:
        a python list of FNBO.XREF records
    """
    selList = u2py.List(0,fnboXrefFile,"MEMBER.ID.IDX",memberId)
    idList = []
    for item in selList:
        tid = selList.next()
        if tid != None:
            idList.append(selList.next())
    idList.pop()
    recList = getTransactionList(idList)
    return recList
    
def findByTransaction(transId):
    '''
    Get a specific FNBO.XREF record
    Calls getTransaction()
    Args:
        transId = The FNBO.XREF transaction id
    Returns:
        FNBO.XREF record
    '''
    return getTransaction(transId)
    
def getTransaction(transId):
    """
    Get a single FNBO.XREF record
    Args:
        id - a single FNBO.XREF id
    Returns:
        a single FNBO.XREF record as a python list
    """
    fnboXrefRec = fnboXrefFile.read(transId).to_list()
    return fnboXrefRec

def getTransactionList(idList):
    """
    Get a list of FNXO.XREF records
    Args:
        idList a list() of FNBO.XREF ids
    Returns:
        A list() of FNBO.XREF records
    """
    recList = []
    for transId in idList:
        xrefRec = getTransaction(transId)
        recList.append(xrefRec)
    return recList

def setTransaction(transId,transRec):
    """
    Write a transaction to FNBO.XREF
    Args:
        transId  = The FNBO.XREF transaction id
        transRec = The FNBO.XREF record to write
                   The transRec is a python-formatted list()
    Returns:
        Nothing
    """
    fnboXref = u2py.DynArray(transRec)
    fnboXrefFile.lock(transId,u2py.LOCK_EXCLUSIVE)
    fnboXrefFile.write(transId,transRec,0)
    return

print("module name: "+__name__)
