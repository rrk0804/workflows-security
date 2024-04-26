# workflows-security
Repository of code developed to analyze the security of software supply chains. 

## Contents and Description:
- **./Argus** - contains source code for the Argus project. The code was adapted from Purdue University's
            purs3lab. The code was modified to include descriptive error messages. Additionally, a
            script was added to run the tool on a list of top open source projects.
- **./results** - contains results obtained from running Argus on top repos. Also, contains results
              obtained from running supplementary scripts on top repos.
- **./analyze-actions.py** - script for checking if a repo is using linters, testers, or other SAST tools.
- **./analyze-environments.py** - script that extracts environments that the repo is deploying code in.
- **./analyze-pr.py** - script that checks if the repo contains ephemeral build environments.
