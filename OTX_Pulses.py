import filecmp
import difflib
import re 
import os
import subprocess
import requests

#Put your OTX API key in between the two apostrophe's on line 17

#this function uses OTX's API to download /u/AlienVault's latest posts, and extracts the IDs of /u/ALienVault's pulses in the most convoluted way humanly possible
def todays_IDs():
    #opens required files
    page_dump = open('page_dump.txt', 'w+')
    messy_todays_IDs = open('messy_todays_IDs.txt', 'w+') 

    #runs the API call, and saves the text body as page_dump
    headers = {'X-OTX-API-KEY': '',}
    response = requests.get('https://otx.alienvault.com/api/v1/pulses/user/AlienVault', headers=headers)
    page_dump.write(response.text)
    page_dump.close()
    
    #uses regex to extract the IDs from page_dump, saved them to messy_todays_IDs, then closes messy_todays_IDs, and page_dump, then deletes the page_dump file
    for line in page_dump:
        IDs = re.findall(r'(?<="id": ")(.*?)(?=")', line)
        messy_todays_IDs.write(str(IDs))
    page_dump.close()
    os.remove('page_dump.txt')
    messy_todays_IDs.close()

    #opens the messy_todays_IDs file, and removes the commas, square bracks, quotes, and lines that have less than 5 characters, leaving only the legitimate pulse IDs, 
    #then writes those pulse IDs to todays_IDs, closes both files, and deletes the messy_todays_IDs file
    #this finally leaves us with the file we will compare to our master list of already downloaded pulses
    messy_todays_IDs = open('messy_todays_IDs.txt', 'r')
    todays_IDs = open('todays_IDs', 'w+')    
    for line in messy_todays_IDs:
        todays_IDs.write(line.replace(',', '\n'))
    messy_todays_IDs.close()
    os.remove('messy_todays_IDs.txt')
    todays_IDs.close()

def compare_the_market():
    print('here we will compare the master list against todays_IDs')




todays_IDs()
