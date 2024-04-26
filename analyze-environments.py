### analyze-environments.py
### Rajit Khatri (rrkhatri@purdue.edu)
### This script analyzes yaml files and checks if the 
### repository is using testing libraries to check code
### pushed into the repo.

import re
import os

actions = ["irongut/CodeCoverageSummary", "lirantal/is-website-vulnerable", "lunarmodules/busted", "cypress-io/github-action", "reactivecircus/android-emulator-runner",
           "google-github-actions/auth", "Legit-Labs/legitify", "aquasecurity/trivy-action", "sonarsource/sonarcloud-github-action", "MobSF/mobsfscan",
           "actions/dependency-review-action", "step-security/harden-runner", "gaurav-nelson/github-action-markdown-link-check", "test-summary/action", "kishikawakatsumi/xcresulttool",
           "lunarmodules/luacheck", "DeterminateSystems/magic-nix-cache-action", "zaproxy/action-baseline", "mikepenz/action-junit-report", "projectdiscovery/nuclei-action",
           "projectdiscovery/nuclei-action", "mszostok/codeowners-validator", "WPO-Foundation/webpagetest-github-action", "treebeardtech/nbmake-action", "andstor/file-existence-action",
           "tonybaloney/pycharm-security", "GitGuardian/ggshield-action", "jfrog/frogbot", "1Password/load-secrets-action", "aws-actions/aws-secretsmanager-get-secrets", 
           "super-linter/super-linter", "anc95/ChatGPT-CodeReview", "crate-ci/typos", "codecov/codecov-action", "mattzcarey/code-review-gpt", 
           "sturdy-dev/codeball-action", "creyD/prettier_action", "reviewdog/action-eslint", "microsoft/gpt-review", "aws-actions/codeguru-reviewer", 
           "ZedThree/clang-tidy-review", "cpp-linter/cpp-linter-action", "crazy-max/ghaction-virustotal", "microsoft/security-devops-action", "re-actors/alls-green"]


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


def createPattern(action : str) -> re.Pattern:
    """
    createPattern is a helper function that generates a regex
    pattern to check if a workflow is using a specific reusable
    action.
    
    :params action: the action to look for
    """
    return re.compile("^\s*uses:\s*" + action)


def get_environments(file : str) -> list:
    """
    get_environments is a helper function that gets all the 
    environments that are used in a yaml script. 

    :params file: the file to analyze
    """
    pattern1 = re.compile("^\s*environment:")
    pattern2 = re.compile("^\s*name:\s*(\w*)")
    found_environment = False
    FILEIN = open(file)
    environments = []

    # Iterate through each line to see if any environments
    # are used in the workflow file:
    for line in FILEIN:
        if not isComment(line):

            if pattern1.search(line):
                found_environment = True

            if pattern2.search(line) and found_environment:
                environments.append(pattern2.search(line).group(1))
                found_environment = False

    return environments


def group_environments(workflows : list):
    """
    group_environments is a helper function that groups together 
    all the environments in the repo.

    :params workflows: list containing the environments of each workflow
    """
    envs = set()
    for environments in workflows:
        envs.update(environments)

    return list(envs)


if __name__ == "__main__":

    print("Comprehensive testing for environments only")
    repos = getAllRepos()
    for repo in repos:
        if repoContainsWorkflows(repo):
            workflows = getWorkflowsInRepo(repo)
            for workflow in workflows:
                print(get_environments(workflow))
    print("-------------------------------------------")
    print()
