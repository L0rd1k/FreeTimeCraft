import xml.etree.ElementTree as ET
import glob
import os, getopt, sys
import shutil


def getXmlFileInFolder(path):
    xmlFilesName = sorted(glob.glob(path + "/*.xml"))
    return xmlFilesName


def load_images_from_folder(path):
    try:
        os.mkdir("Images")
    except OSError:
        pass
    ext = ['png', 'jpg', 'gif', 'jpeg']
    files = list()
    [files.extend(glob.glob(path + '/*.' + e)) for e in ext]
    if len(files) > 0:
        for file in files:
            shutil.copy(file, "./Images/")


def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    filename = os.path.splitext(root.find('filename').text)[0]
    listPoints = list()
    [listPoints.append((key.find('x').text, key.find('y').text)) for key in root.findall('./object/polygon/pt')]
    try:
        os.mkdir("Points")
    except OSError:
        pass
    file_object = open("./Points/" + filename + ".txt", "w")
    [file_object.writelines(str(int(float(elem[0]))) + " " + str(int(float(elem[1]))) + "\n") for elem in listPoints]
    file_object.close()


def main(argv):
    arguments, values = getopt.getopt(argv, "p:", "Path")
    for arguments, values in arguments:
        if arguments in ("-p", "--Path"):
            path = values
            xmlFilesName = getXmlFileInFolder(path)
            load_images_from_folder(path)
            [parseXML(elem) for elem in xmlFilesName]


if __name__ == "__main__":
    main(sys.argv[1:])
