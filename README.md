# pa-scraper
## What is this?
TAs get assigned a number of students to grade their programming assignments. However, the submission website LATTE does not provide a way to download these files all at once. This script automates the process of downloading all the files from LATTE. It also provides a summary of the number of students who submitted their assignments and a list of students who did not submit their assignments.
## How to run
### 1. Install dependencies
```
  python -m venv .venv # or python3.10 / python3 if this gives you an error
  . .venv/bin/activate # or . .venv/scripts/activate if you are on windows
  pip install -r requirements.txt 
```
### 2. Configure settings
in the `script.sh` file, set the following variables:

```
export PWD='' # Your Brandeis login password
export UNAME='' # Your Brandeis login username
export DOWNLOAD_DIR='' # The directory you want to download the files to
export PA_NAME='' # The name of the PA you want to download, has to be the same as the name of the PA on LATTE
```
### 3. Run the script
```
  bash script.sh
```
You should see chrome being opened, complete the DUO authentication. The script should start downloading the files to the directory you specified in the `DOWNLOAD_DIR` variable.

## Result
After making sure you have all the files in the specified directory, the script will prompt you to press enter. After you press enter, the script will print out the following result:

```
==========================================

Duration: 19.5 seconds
Students: 15
Submissions: 14
No submission: 1
No submission emails:
['student@brandeis.edu']
        
==========================================

```
## If you have any suggestions feel free to open an issue or email mingshihwang@brandeis.edu