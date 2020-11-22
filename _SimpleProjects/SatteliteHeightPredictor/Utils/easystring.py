import ntpath

def split_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)