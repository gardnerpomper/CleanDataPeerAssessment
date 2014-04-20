CleanDataPeerAssessment
=======================

This is the peer assessement project for coursera's "Getting and
Cleaning Data" in the Data Science track.

# Problem description

The assignment is to generate a "tidy" data set from raw data. The raw
data is available here:

https://d396qusza40orc.cloudfront.net/getdata%2Fprojectfiles%2FUCI%20HAR%20Dataset.zip 

The tidy data consists of 1 record for each subject/activity
group. The record contains an entry for each of the original raw data
columns that represent either the mean or standard deviation of
original measurements. Each column in the tidy dataset will be the
mean of all the values for that column in that group.

To illustrate, the original data set contains a column called
"tBodyAcc-mean()-X". That column will be converted to
"tbodyacc_mean_x" and the mean will be taken for all values of subject
1 with activity WALK. The mean of all the values for subject 1 and
activity JUMP will also be calculated, and so on.

# Implementation

The repository contains the following files:
* README.md - this file
* merge.py - python script to extract relevant columns and prepend subject and activity
* run_analysis.R - overall script to run merge.py and calculate the tidy.csv file

# Execution

1. The dataset (link shown above) should be downloaded to the current
   directory and unzipped. This will create a "UCI HAR Dataset" directory
   tree in the current directory.
2. source("run_analysis.R") in the R environment
3. execute the "run()" function

