import urllib.request
import filecmp
import difflib
import re 
import os
import subprocess

#this function cleans the download of the webpage, so only the json file names remain, then saves it as daily.txt
def cleanFile(file):
    rfile = open(file, 'r+')
    tfile = open("daily.txt", "w+")
    for line in rfile:
        t = re.search(r'(?<=json">)(.*)(?=\<\/a>)', line)
        if t is not None:
            tfile.writelines(t.group(0) + '\n')
    rfile.close()
    tfile.close()

#this function compares the main file (dld_circle_osint_feed), with the second file (daily), and writes all missing json file names to download.txt
def compare():
    result = filecmp.cmp('dld_circle_osint_feed.txt', 'daily.txt')
    d = open('messy_download.txt', 'w+')
    if result == True:
        print ('Nothing to download')
    else:
        for line in difflib.unified_diff(open('dld_circle_osint_feed.txt').readlines(), open('daily.txt').readlines(), n=0):
            d.writelines(str(line))
    d.close()

#this function will clean the messy download file resulting in a text of commands to run to download the missing files
def cleanMDL():
    mdl = open('messy_download.txt', 'r')
    dl = open('download.sh', 'w+')
    a = open('dld_circle_osint_feed.txt', 'a')
    for line in mdl:
        t = re.search(r'(?<=\+)[^m](.*)(.json)', line)
        if t is not None:
            a.writelines(t.group(0) + '\n')
            dl.writelines("wget https://www.circl.lu/doc/misp/feed-osint/" + t.group(0) + " -P /home/circl_osint_feed/" + '\n' + '''curl -X POST "localhost:9200/circl_osint_feed/_doc/" -H 'Content-Type: application/json' --data-binary "@/home/circl_osint_feed/''' + t.group(0) + '''"''' + "\n")
    mdl.close()
    dl.close()
                

#the script downloads the webpage (as dump), cleans it and saves it as daily, then compares the main file with the daily file, then deletes dump

site = urllib.request.urlretrieve('https://www.circl.lu/doc/misp/feed-osint/', 'dump.txt')
cleanFile('dump.txt')
compare()
os.remove('dump.txt')
cleanMDL()
os.remove('messy_download.txt')
os.remove('daily.txt')
#os.chmod('download.sh', 0o775)
#subprocess.run('./download.sh')
#os.remove('download.sh')
