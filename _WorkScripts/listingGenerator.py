import os
import getopt
import sys


def f_generate_listing_docs_file(input_file, output_file):
    f_w = open(output_file + "Generated_doc.pdf", "w")
    for subdir, dirs, files in os.walk(input_file):
        dirs.sort()
        files.sort()
        for filename in files:
            file_path = subdir + os.sep + filename
            if file_path.endswith(".cpp") or file_path.endswith(".h"):
                print(file_path)
                f_r = open(file_path, "r")
                for x in f_r:
                    f_w.write(x)
                f_r.close()
    f_w.close()


def main(argv):
    input_file = ""
    output_file = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('generate.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--help':
            print('generate.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    f_generate_listing_docs_file(input_file, output_file)


if __name__ == '__main__':
    main(sys.argv[1:])

