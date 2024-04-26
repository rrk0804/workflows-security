#!/bin/bash

###############################################################
# Rajit Khatri (rrkhatri@purdue.edu)
# run_repos.sh
# Use this bash script to run the Argus static analyzer
# tool on a list of repositories specified by an excel sheet. 
###############################################################

# Initialize environment variables:
REPOS_COLLECTION_PATH=repos.dat
OUTPUT_FOLDER=./results

# Prepare the environment for running Argus:
docker-compose build

# Iterate through all the repos and run Argus on each one:
while read REPO WORKFLOW_PATH COMMIT_ID; do 

    # Run Argus and store the output in the results folder:
    docker-compose run argus --mode repo --url $REPO --output-folder $OUTPUT_FOLDER 

done < $REPOS_COLLECTION_PATH

exit 0