import urllib.request
import filecmp
import difflib
import re 

#site = urllib.request.urlretrieve('https://www.circl.lu/doc/misp/feed-osint/', 'day1.txt')

def cleanFile(file):
    rfile = open(file, 'r')
    
    #i = 1
    for line in rfile:
        t = re.search(r'(?<=json">)(.*)(?=\<\/a>)', line)
        if t is not None:
            print(t.group(0))
        #print(str(i) + " - " + line)
        #i+=1
    rfile.close()



def compare():
    result = filecmp.cmp('day1.txt', 'day2.txt')
    if result == True:
        print ('yes')
    else:
        for line in difflib.unified_diff(open('day1.txt').readlines(), open('day2.txt').readlines(), n=0):
            print(str(line))

cleanFile('prac.txt')
