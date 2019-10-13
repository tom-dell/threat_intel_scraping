import filecmp
import difflib
import re 
import os
import subprocess
import requests

#--------------------------------------------------------------
#If you are reading this, I'm sorry for what you are about to see
#--------------------------------------------------------------

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
    page_dump = open('page_dump.txt', 'r')
    for line in page_dump:
        IDs = re.findall(r'(?<="id": ")(.*?)(?=")', line)
        messy_todays_IDs.write(str(IDs))
    page_dump.close()
    messy_todays_IDs.close()

    #opens the messy_todays_IDs file, and removes the commas and replaces them with new lines. Removes the square brackets and apostrophes,
    messy_todays_IDs = open('messy_todays_IDs.txt', 'r')
    messy_todays_IDs1 = open('messy_todays_IDs1.txt', 'w+')   
    for line in messy_todays_IDs:
        messy_todays_IDs1.write(line.replace(',', '\n').replace('[', '').replace(']', '').replace('\'', '').replace(' ', ''))
    messy_todays_IDs.close()
    messy_todays_IDs1.close()    
    
    #this function removes any line that has less than 5 characters
    messy_todays_IDs1 = open('messy_todays_IDs1.txt', 'r')
    todays_IDs = open('todays_IDs.txt', 'w+')
    for line in messy_todays_IDs1:
        if(len(line) > 5):
            todays_IDs.write(line)
    messy_todays_IDs1.close()
    todays_IDs.close()

    #time to remove the insane amount of files i've created since I can't figure out variables
    os.remove('page_dump.txt')
    os.remove('messy_todays_IDs.txt')
    os.remove('messy_todays_IDs1.txt')

#this function will check the lines in todays_IDs against the master list, any IDs not in mater list will be fed to dl_and_push_to_es 
def compare_the_market():
    filtered_messy_IDs = open('filtered_messy_IDs.txt', 'w+')
    with open('masterlist.txt', 'r') as masterlist:
        with open('todays_IDs.txt', 'r') as messy_todays_IDs:
            difference = difflib.unified_diff(
                masterlist.readlines(),
                messy_todays_IDs.readlines(),
                fromfile='messy_todays_IDs',
                tofile='masterlist',
            )
            for line in difference:
                filtered_messy_IDs.write(line)
    filtered_messy_IDs.close()
    
#this function cleans the new_IDs file for use in the dl_and_push_to_es function
def clean_new_IDs():
    filtered_messy_IDs = open('filtered_messy_IDs.txt', 'r')
    filtered_todays_IDs = open ('filtered_todays_IDs.txt', 'w+')
    for line in filtered_messy_IDs:
        clean_IDs = re.findall(r'(?=\d\w)(.*)', line)
        if clean_IDs is not None: 
        #filtered_todays_IDs.write(str(clean_IDs) + '\n')
            print(clean_IDs)
    filtered_messy_IDs.close()
    filtered_todays_IDs.close()

#this function will create a .sh script with curl commands to download the json from OTX, and curl it to elasticsearch
#def dl_and_push_to_es():


todays_IDs()
compare_the_market()
clean_new_IDs()
