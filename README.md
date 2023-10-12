# pa-scraper
## What is this?
TAs get assigned a number of students to grade their programming assignments. However, the submission website LATTE does not provide a way to download these files all at once. This script automates the process of downloading all the files from LATTE. It also provides a summary of the number of students who submitted their assignments and a list of students who did not submit their assignments.
## How to run
### 1. Clone repository
- Create a folder and navigate to the folder in your terminal/shell paste the following commands:
```
  git init 
  git clone https://github.com/MingCWang/pa-scraper.git
```
- Install dependencies
```
  python -m venv .venv OR python3 -m venv .venv
  . .venv/bin/activate OR . .venv/scripts/activate (for windows)
  pip install -r requirements.txt 
```
### 2. Configure settings
- in the `script.sh` file, set the following variables including the quotes:

```
export PWD='' # Your Brandeis login password
export UNAME='' # Your Brandeis login username
export DOWNLOAD_DIR='' # The directory you want to download the files to e.x. /Users/username/Desktop/PA1
```
- in the `emails.txt` file, add the emails of the students who you are assigned to like so.
```
student1@brandeis.edu
student2@brandeis.edu
.
.
.

```
### 3. Run the script
1. Navigate to your terminal/shell and run the following command:
```
  bash script.sh
```
2. You should see chrome being opened, complete the DUO authentication. 
3. The script will direct you to course COSI 12B, click on the PA folder so you can see this button. (if you are not in this course, you can change the course name scraper file.)
<img width="310" alt="Screen Shot 2023-10-11 at 11 59 45 PM" src="https://github.com/MingCWang/pa-scraper/assets/73949957/d4e2b269-887f-45fe-abff-21e446c03a78"> 

4. Click enter in the terminal to start downloading the files.
5. The script should start downloading the files to the directory you specified in the `DOWNLOAD_DIR` variable.

## Result
After making sure you have all the files in the specified directory, the script will prompt you to press enter. After you press enter, the script will print out the following result:

```
==========================================


Duration: 37.5 seconds
Students: 11
Submissions: 11
Late submissions: 
['student@brandeis.edu: 20 hours 43 mins late', 'student2@brandeis.edu: 1 day 21 hours late']
No submission: 0
No submission emails:
[]
        
==========================================

```
## If you have any suggestions feel free to open an issue or email mingshihwang@brandeis.edu