### analyze-actions.py
### Rajit Khatri (rrkhatri@purdue.edu)
### This script analyzes yaml files and checks if the
### repository is using testing libraries to check code
### pushed into the repo.

import re
import os
import sys

path_pattern = re.compile(".*/(.*)$")

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


def analyzeScript(file : str) -> list:
    """
    analyzeScript is a helper function that scans a
    workflow file to check if it is using linters, testers,
    or security vulnerability finders on source code.

    :params file: the actions file to analyze
    """
    FILEIN = open(file)
    scriptActions = []

    # Iterate through each line to see if any useful
    # reusable actions are present in the workflow:
    for line in FILEIN:
        if not isComment(line):

            # Iterate through all the actions:
            for action in actions:
                pattern = createPattern(action)

                if pattern.search(line):
                    action_write = re.search(path_pattern, action).group(1)
                    scriptActions.append(action_write)

    FILEIN.close()

    return scriptActions


def check_repo(repo : str):
    """
    check_repo is a helper function that runs the script on 
    all the repos in the current folder and returns whether 
    the script contains actions or not.

    :params repo: the repo to analyze
    """
    actions = set()
    if repoContainsWorkflows(repo):
        workflows = getWorkflowsInRepo(repo)
        for workflow in workflows:
            actions.update(analyzeScript(workflow))
    
    return list(actions)


def test():
    """
    test is a helper function that run tests to validate the 
    script. Use when you want to debug the script. 
    """
    
    print("Test for checking isComment()")
    str1 = "This is not a comment"
    print(str1)
    print(isComment(str1))
    print("-------------------------------------------")
    print()

    print("Test for checking isComment()")
    str2 = "# This is a comment"
    print(str2)
    print(isComment(str2))
    print("-------------------------------------------")
    print()

    print("Test for checking isComment()")
    str3 = "              # This is a comment"
    print(str3)
    print(isComment(str3))
    print("-------------------------------------------")
    print()

    print("Test for checking getAllRepos()")
    repos = getAllRepos()
    print(repos)
    print("-------------------------------------------")
    print()

    print("Test for checking repoContainsWorkflows()")
    for repo in repos:
        print(repoContainsWorkflows(repo))
    print("-------------------------------------------")
    print()

    print("Test for checking getWorkflowsInRepo()")
    for repo in repos:
        print(getWorkflowsInRepo(repo))
    print("-------------------------------------------")
    print()

    print("Test for checking analyzeScript()")
    for repo in repos:
        workflows = getWorkflowsInRepo(repo)
        for workflow in workflows:
            print(analyzeScript(workflow))
    print("-------------------------------------------")
    print()

    print("Comprehensive testing")
    repos = getAllRepos()
    for repo in repos:
        if repoContainsWorkflows(repo):
            workflows = getWorkflowsInRepo(repo)
            for workflow in workflows:
                print(analyzeScript(workflow))
    print("-------------------------------------------")
    print()


if __name__ == "__main__":

    if sys.argv[1] == "-d":
        test()
    else:
        output_file_1 = sys.argv[1]
        output_file_2 = sys.argv[2]
        FILEOUT_1 = open(output_file_1, "w")
        FILEOUT_2 = open(output_file_2, "w")

        print("Getting all repos in the current folder: ")
        repos = getAllRepos()

        print("Analyzing all repos: ")
        # Get actions present in each repo:
        for repo in repos:
            actions = check_repo(repo)
            if len(actions) > 0:
                repo_write = re.search(path_pattern, repo).group(1)
                FILEOUT_1.write(str(repo_write) + "\n")
                FILEOUT_2.write(str(repo_write) + " : " + ",".join(str(element) for element in actions) + "\n")
        
        FILEOUT_1.close()
        FILEOUT_2.close()

        print("Done!")