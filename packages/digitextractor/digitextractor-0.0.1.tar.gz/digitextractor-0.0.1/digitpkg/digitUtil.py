def getSortedDictionaryImages(dictimages, index):
    sortedimgkeys =[dk for dk in dictimages.keys()]
    sortedimgkeys.sort()
    xdict = [dictimages[k] for k in sortedimgkeys][index]
    sortedimgkkeys = [dk for dk in xdict.keys()]
    sortedimgkkeys.sort()
    orderedImages = [xdict[k] for k in sortedimgkkeys]
    return orderedImages
