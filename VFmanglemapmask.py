import configparser
import argparse
import os
import mmap


# What am I trying to do?
# * Have extracted height/displacement/mask maps.
# * TODO - write them to the correct path now (raw/)
# * TODO Extract textures, and write them to the correct path (bmp/)
# * TODO Modify project file to match up paths

# material_textures.data contains the texture data
# Textures are ordered in the material_textures the same order that they're stored.

def main():
    args=argParser()
    #print(args)

    #We need to work out if we list, extract or replace.
    if args.action == 'list':
        do_list(args)
    elif args.action == 'extract':
        do_extract(args)
    elif args.action == 'replace':
        do_replace(args)

def do_list(args):
    project = projectParser(args.source)
    # Run through and extract fileIDs, start, filenames
    fileIDs = extractFileID(project, args.source)
    print("ID\t\t\t\t\tSize\t\tOriginal Filename")
    for entry in fileIDs:
        print("%s\t%s\t%s" % (entry['id'].encode('utf8'), entry['length'], entry['filename'].encode('utf8')))

def do_replace(args):
    project = projectParser(args.source)
    # Run through and extract fileIDs, start, filenames
    fileIDs = extractFileID(project, args.source)
    # Check the ID exists
    fID = find(fileIDs, 'id', args.id)
    if fID == -1:
        print("Couldn't find that ID in the bundle - try using list to find the IDs")
        quit()
    fID = fileIDs[fID]

    try:
        fsize = os.path.getsize(args.file)
    except:
        print("Error opening %s for read, does it exist?" % args.file)
        quit()

    if fsize != fID['length']:
        print("Map data is the wrong size! Expected %d bytes, but found %d bytes" % (fID['length'], fsize))
        quit()

    #Now do the tricky bit.
    # MMap the input file
    # Need to fix this properly.
    try:
        fin = open(args.file, 'r+b')
        mmfin = mmap.mmap(fin.fileno(),0)
    except:
        print("Error opening %s for read, something went wrong!" % args.file)
        mmfin.close()
        fin.close()
        quit()

    # MMap the output file, and yes, r+ is correct?!?
    try:
        fout = open(args.source + "bundle.dat", 'r+b')
        mmfout = mmap.mmap(fout.fileno(), 0)
    except:
        print("Error opening %s for write, something went wrong!" % (args.source + "bundle.dat"))
        mmfin.close()
        fin.close()
        mmfout.close()
        fout.close()
        quit()

    #calc where we're working
    sp = fID['start']
    ep = fID['start']+fID['length']
    #This is the overwrite
    mmfout[sp:ep] = mmfin[0:fID['length']]
    # and we're done.
    mmfout.close()
    mmfin.close()
    fout.close()
    fin.close()
    print("Just replaced %s section with %s file." % (os.path.basename(fID['filename']), os.path.basename(args.file)))




def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def do_extract(args):
    project = projectParser(args.source)
    # Run through and extract fileIDs, start, filenames
    fileIDs = extractFileID(project, args.source)
    extractFiles(fileIDs, args)


    # need to open the file (bundle.dat)
    # then run through each item and extract
def extractFiles(fileIDs, args):
    filename = args.source + "bundle.dat"
    try:
        binFile = open(filename, "rb")
    except:
        print("Error opening file %s" % filename)
        quit()

    for item in fileIDs:
        fname = os.path.basename(item["filename"])
        print("Extracting %s (was %s)" % (fname, item["filename"]))
        binFile.seek(item["start"],0)
        chunk = binFile.read(item["length"])
        # write out chunk to new file
        try:
            fname = os.path.join(args.output, fname)
            outBin = open(fname, "wb")
        except:
            print("Error opening %s for write" % fname)
            quit()
        outBin.write(chunk)
        outBin.close()
    binFile.close()

def extractFileStarts(project, sourceDir):
    fileIDs = []
    for item in project["Bundle"]:
        Id = item.split('.')[1]
        fileIDs.append({"id": Id, "start": int(project["Bundle"][item]), "length": 0, "filename": ""})
    outputList = sorted(fileIDs, key  = lambda fileIDs: fileIDs['start'])
    # Figure out section sizes
    stopPoint=getFileSize(sourceDir + "bundle.dat")
    for cnt in range(len(outputList)-1,-1, -1):
        outputList[cnt]["length"] = stopPoint - outputList[cnt]["start"]
        stopPoint = outputList[cnt]["start"]
    return outputList

def getFileSize(filename):
    try:
        binFile = open(filename,"rb")
        binFile.seek(0,2)
        num_bytes = binFile.tell()
        binFile.close()
    except:
        print("Error handling file %s" % filename)
        quit()
    return num_bytes

def extractFileID(project, source):
    fileIDs = extractFileStarts(project, source)
    # How do I match fileIDs to id of the file?
    for section in project:
        id=""
        file=""
        for item in project[section]:
            if "id" == item:
                id = project[section][item]
            if "file" == item:
                file = project[section][item]
        if file and id:
            test = next(item for item in fileIDs if item['id'] == id)
            test['filename'] = file
    return(fileIDs)

def projectParser(sourceDir):
    config = configparser.ConfigParser()
    if not config.read(sourceDir + "project.dat"):
        print("Can't read project.dat from %s" % sourceDir)
        quit()
    return config

def argParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands', dest='action')

    extract_p = subparsers.add_parser("extract", help='Extract the heightmap data files from VF bundle.')
    list_p =  subparsers.add_parser("list",help='Lists heightmap data from a VF bundle.')
    replace_p =  subparsers.add_parser("replace", help='Replaces an existing heightmap')

    list_p.add_argument('source',
                        help='Source bundle- Directory containing Voxel Farm bundle (bundle.dat)')

    extract_p.add_argument('source',
                           help='Source bundle- Directory containing Voxel Farm bundle (bundle.dat)')
    extract_p.add_argument('output', help = 'Output directory for extracted maps')


    replace_p.add_argument('source',
                        help='Source bundle- Directory containing Voxel Farm bundle (bundle.dat)')
    replace_p.add_argument('id', help = 'ID of map to replace')
    replace_p.add_argument('file', help = 'Filename of replacement map')

    args = parser.parse_args()
    return args

def search_dictionaries(key, value, list_of_dictionaries):
    return [element for element in list_of_dictionaries if element[key] == value]

main()


