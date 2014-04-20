#!/usr/bin/env python
import sys
import re
import os.path
import logging

def load_subjects(fp) :
    '''
    load a file of the subject id for each event
    '''
    subjectL = [l.strip() for l in fp.readlines()]
    return subjectL

def load_activities(fp,activityD):
    '''
    load a file of the subject id for each event
    '''
    activityL = [activityD[l.strip()] for l in fp.readlines()]
    return activityL

def load_names(fp) :
    '''
    read the file defining what each activity code means
    '''
    activityD = {}
    for line in fp:
        flds = line.strip().split()
        activityD[flds[0]] = flds[1]
    return activityD

def load_features(fp):
    '''
    load the file defining the column names
    and pull out just the ones for mean and std deviation
    '''
    featureD = {}
    #
    # ----- foreach line
    #
    re_dash = re.compile('-')
    re_other = re.compile('[()]')
    for line in fp:
        #
        # ----- split it into a column number and a column name
        #
        flds = line.strip().split()
        colno = int(flds[0])
        colnm = flds[1]
        #
        # ----- only keep column names that include "mean" or "std"
        #
        keep = False
        if colnm.find('mean') >= 0:
            keep = True
        elif colnm.find('std') >= 0:
            keep = True
        if( not keep): continue
        #
        # ----- make the column name valid by removing ()- characters
        # ----- and consistent by converting to lower case
        #
        colnm = re_other.sub('',colnm)
        colnm = re_dash.sub('_',colnm)
        featureD[colno] = colnm.lower()
    return featureD

def load_events(fp,subjectL,activityL,features,outFp):
    '''
    load the file of events and extract just the columns
    we are interested in. Merge them with the subject and activity
    and write to the supplied stream.
    ARGUMENTS:
    fp		- stream to read events from
    subjectL	- list of subject id for each event
    activityL	- list of activity for each event
    features	- sorted list of colnumsfor which columns to keep
    outFp	- stream to write output to
    '''
    #
    # ----- sort the features by column number
    #
    for lineno,line in enumerate(fp):
        cols = [ subjectL[lineno],activityL[lineno] ]
        flds = line.strip().split()
        cols.extend( [flds[colno] for colno in features] )
        outFp.write('%s\n' % ','.join(cols))
        #if lineno == 10: break

def filter(activityD, keepCols, dataDir, setName, outFp):
    '''
    filter the datasets from the specified set ("test" or "train")
    to the output stream, including only the columns specified in
    keepCols
    '''
    #
    # ----- get the base data structs from the training dir
    #
    subjectFile = '%s/subject_%s.txt' % (setName,setName)
    with open(os.path.join(dataDir,subjectFile),'r') as fp:
        subjectL = load_subjects(fp)
    logging.debug('subjectL = %s' % subjectL)

    activityFile = '%s/y_%s.txt' % (setName,setName)
    with open(os.path.join(dataDir,activityFile),'r') as fp:
        activityL = load_activities(fp,activityD)
    logging.debug('activityL = %s' % activityL)
    #
    # ----- filter training set to output stream
    #
    eventFile = '%s/X_%s.txt' % (setName,setName)
    with open(os.path.join(dataDir,eventFile),'r') as fp:
        load_events(fp,subjectL,activityL,keepCols,sys.stdout)

if __name__ == '__main__':
    logging.basicConfig(filename='merge.log',filemode='w',level=logging.DEBUG)
    #
    # ----- there should be one command line argument: the dataset directory
    # ----- ie "./UCI HAR Dataset"
    #
    nargs = len(sys.argv)
    if nargs != 2:
        sys.stderr.write('Usage: merge.py <datadir>')
        sys.exit(1)
    dataDir = sys.argv[1]
    #
    # ----- load the information common to both test and training
    # ----- (activity names and feature names)
    #
    with open(os.path.join(dataDir,'activity_labels.txt'),'r') as fp:
        activityD = load_names(fp)
    logging.debug('activityD = %s' % activityD)

    with open(os.path.join(dataDir,'features.txt'),'r') as fp:
        featureD = load_features(fp)
    logging.debug('featureD = %s' % featureD)
    #
    # ----- write header line
    #
    features = featureD.items()[:]
    features.sort()
    sys.stdout.write('%s,%s,%s\n'%('subject','activity',','.join(f[1] for f in features)))

    keepCols = [f[0] for f in features]
    #
    # ----- filter the training data
    #
    filter(activityD,keepCols,dataDir,'train',sys.stdout)
    #
    # ----- filter the test data
    #
    filter(activityD,keepCols,dataDir,'test',sys.stdout)
