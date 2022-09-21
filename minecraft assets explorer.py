from os import getenv,listdir,system
import json
import traceback
from shutil import *
from time import sleep

def createFolders(folders, path):
    if len(path)==1:
        folders[path[0]] = ""
        return folders
    if not path[0] in folders:
        folders[path[0]]={}
    folders[path[0]]=createFolders(folders[path[0]], path[1:len(path)])
    return folders

def naviguate(folder, jsonDict, path=""):
    print()
    choice = len(folder)
    while True:
        print()
        print("Select an element by entering his index (enter -1 to go back), elements marked with ... are folders")
        for i in range(len(folder)):
            print(str(i),"..."*(not not folder[list(folder.keys())[i]])+"\t"+list(folder.keys())[i])
        choice = int(input(path+"> "))
        if choice==-1: return
        selection = list(folder.keys())[choice]
        if not folder[selection]:
            sha = jsonDict['objects'][path+selection]['hash']
            print("\nFile hash :",sha)
            system("mkdir "+getenv("userprofile")+"\\Documents\\Minecraft")
            copyfile(appdata+"\\.minecraft\\assets\\objects\\"+sha[0:2]+"\\"+sha, getenv("userprofile")+"\\Documents\\Minecraft\\"+selection)
            print("File extracted into",appdata+"\\Documents\\Minecraft\\"+selection)
            sleep(2)
        else: naviguate(folder[selection], jsonDict, path+selection+"/")

appdata=getenv("appdata")
try:
    versions = listdir(appdata+"\\.minecraft\\assets\\indexes")
    choice = ""
    while (choice+".json") not in versions:
        print("Please choose a version between the following :")
        for i in range(len(versions)):
            print("\t"+versions[i][0:-5])
        choice = input("> ")
    print("Establishing directories tree...")
    elements = open(appdata+"\\.minecraft\\assets\\indexes\\"+choice+".json")
    elements = json.load(elements)
    folders = {}
    for i in elements['objects']:
        folders = createFolders(folders, i.split("/"))
    naviguate(folders, elements)
except Exception as error:
    traceback.print_exc()
    print("An error occured, check if Minecraft is installed")