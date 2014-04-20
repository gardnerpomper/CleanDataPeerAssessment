##
## after sourcing this file, just type "run()" to execute
## This assumes that the "UCI HAR Dataset" is extracted and unzipped in the current directory
## the output is generated as "tidy.csv" in the current directory
##
run<-function() {
  ##
  ## extract the subset of columns and merge in the subjects and activities
  ## NOTE: this is an external python program. It must be executable (chmod +x merge.py)
  ## and it is set to run on OS/X (for linux, change the first line to "#!/bin/env python")
  ##
  system("./merge.py 'UCI HAR Dataset' > merged.csv ")
  ##
  ## load the merged data and
  ## calculate the mean of each subject/activity group
  ##
  ds<-read.csv("merged.csv")
  d2<-aggregate(ds[seq(3,81)],list(subject=ds$subject,activity=ds$activity),mean)
  ##
  ## write this out as the "tidy" dataset (tidy.csv"
  ##
  write.csv(d2,"tidy.csv",row.names=FALSE)
}
