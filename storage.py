import os
from typing import List

def getRootStorageAbsPath() -> str:
    """
    * @desc: Returns the root path for storage folder
    * @return: Normalized path
    """
    return os.path.abspath('storage')

def enumrateFilenames() -> List:
    """
    * @desc: Return a list of all the file names in the storage
    * @return: List of file names
    """
    filenameList: List = []
    for dirpath, dirnames, filenames in os.walk(getRootStorageAbsPath()):
        for _, name in enumerate(filenames):
            filenameList.append('{}/{}'.format(dirpath, name))
    return filenameList

def numberOfFiles() -> int:
    """
    * @desc: Return number of files in the storage
    * @return: int -> Number of files
    """
    return len(enumrateFilenames())
