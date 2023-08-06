import os
import collections


def files_by_extensions(root_dir='.', level=2):
    results = collections.defaultdict(list)
 

    for dirName, subdirList, fileList in os.walk(root_dir):
        for fname in fileList:
            if fname.count('.') > level-1:
                ftype = '.'.join(fname.split('.')[-level:])
                results[ftype].append(os.path.join(dirName, fname)) 

    return results
