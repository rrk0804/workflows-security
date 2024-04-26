### analyze-pr.py
### Rajit Khatri (rrkhatri@purdue.edu)
### This script analyzes yaml files and checks if the
### repository is using ephemeral build environments 
### to temporarily deploy builds to the cloud

import re 
import os
import sys

path_pattern = re.compile(".*/(.*)$")

def getAllRepos() -> list:
    """
    getAllRepos returns a list of all repos in the current
    directory.
    """
    current_dir = "."

    return [os.path.join(current_dir, o) \
             for o in os.listdir(current_dir) \
             if os.path.isdir(os.path.join(current_dir, o))]


def repoContainsWorkflows(repo : str) -> bool:
    """
    repoContainsWorkflows is a helper function that checks 
    if the repo contains workflow files.

    :params repo: the repo to check
    """ 
    # Get all the directories in the repo:
    directories = [os.path.join(repo, o) \
                    for o in os.listdir(repo) \
                    if os.path.isdir(os.path.join(repo, o))]
    
    # Check if the repo contains a workflow folder:
    if (repo + "/.github") in directories:
        github_dirs = [os.path.join(repo + "/.github", o) \
                        for o in os.listdir(repo + "/.github") \
                        if os.path.isdir(os.path.join(repo + "/.github", o))]
        
        if (repo + "/.github/workflows") in github_dirs:  
            return True
        else:
            return False
    
    return False


def getWorkflowsInRepo(repo : str) -> list:
    """
    getWorkflowsInRepo is a helper function that gets 
    the workflow files in the repo.

    :params repo: the repo to check
    """ 
    # Get the contents of the .github/workflows directory
    path = os.path.join(repo, ".github", "workflows")
    workflows = [os.path.join(repo, ".github", "workflows", o) \
                  for o in os.listdir(path) if str(o).endswith("yml") \
                  or str(o).endswith("yaml")]

    return workflows


def isComment(line: str) -> bool:
    """
    isComment is a helper function that checks whether
    the line inputted into the function is a comment.

    :params line: the line to check
    """
    pattern = re.compile("^\s*#")

    if pattern.search(line):
        return True
    
    return False


def analyze_workflow(file : str):
    """
    analyze_workflow is a helper function that checks if 
    the workflow file creates ephemeral environments and 
    temporarily deploys builds to the new environment.

    :params file: the workflow file to analyze
    """
    cloud_providers = ["terraform", "kubernetes"]

    # Open the file:
    FILEIN = open(file)

    # Check if the file is triggered by a pull request:
    pr_trigger = False
    for line in FILEIN:
        if not isComment(line):
            if "pull_request" in line.lower():
                pr_trigger = True
                break
    
    # Check if the file contains instructions for deploying
    # the build to the cloud:
    if pr_trigger:
        for line in FILEIN:
            if not isComment(line):
                for provider in cloud_providers:
                    if provider in line:
                        FILEIN.close()
                        return True
        return False
    else:
        return False


def check_repo(repo : str, output_file : str):
    """
    check_repo is a helper function that runs the script on 
    all the repos in the current folder and returns whether 
    the script contains actions or not.

    :params repo: the repo to analyze
    :params output_file: the file to write the results to
    """
    FILEOUT = open(output_file, "w")
    result = False
    if repoContainsWorkflows(repo):
        workflows = getWorkflowsInRepo(repo)
        for workflow in workflows:
            if analyze_workflow(workflow):
                workflow_write = re.search(path_pattern, workflow).group(1)
                FILEOUT.write(workflow_write + "\n")
                result = True
    
    FILEOUT.close()


    return result

def test():
    """
    test is a helper function that run tests to validate the 
    script. Use when you want to debug the script. 
    """
    # Check if the repo is triggered by pull requests:
    print("Comprehensive testing")
    repos = getAllRepos()
    print(repos)
    for repo in repos:
        if repoContainsWorkflows(repo):
            workflows = getWorkflowsInRepo(repo)
            for workflow in workflows:
                print(analyze_workflow(workflow))
    print("-------------------------------------------")
    print()


if __name__ == "__main__":

    if sys.argv[1] == "-d":
        test()
    else:
        output_file_1 = sys.argv[1]
        output_file_2 = sys.argv[2]
        FILEOUT_2 = open(output_file_2, "w")

        print("Getting all repos in the current folder: ")
        repos = getAllRepos()

        print("Analyzing all repos: ")
        # Get actions present in each repo:
        for repo in repos:
            containsEnvironment = check_repo(repo, output_file_1)
            if containsEnvironment:
                repo_write = re.search(path_pattern, repo).group(1)
                FILEOUT_2.write(repo_write + "\n")
        
        FILEOUT_2.close()

        print("Done!")