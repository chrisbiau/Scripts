#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os 
import datetime 
from shutil import copyfile
from shutil import copy
from shutil import rmtree

import PIL.Image as PILimage
from PIL.ExifTags import TAGS, GPSTAGS

import ffmpeg

from pprint import pprint # for printing Python dictionaries in a human-readable way


inputDir =r'C:\Users\chrib\Desktop\Camera'
outputDir=r'C:\Users\chrib\Desktop\CameraSorted'

def get_exif_creation_date(image_path):
    dateOfDay = None
    image = PILimage.open(fileFullPath)
    exif_data = image._getexif()

    if exif_data is not None:
        for tag, dateTime in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'DateTimeOriginal':
                #exemple date 2023:02:23 09:20:11 of value
                dateOfDay = datetime.datetime.strptime(dateTime, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d")
    
    return  dateOfDay


def get_mp4_creation_date(video_path):
    dateOfDay = None
    
    probe = ffmpeg.probe(video_path)["streams"]
    #pprint(probe)
    
    for item in probe:
        if 'tags' in item and 'creation_time' in item['tags']:
            creation_time = item['tags']['creation_time']
            #exemple date 2023-03-04T11:42:01.000000Z
            dateOfDay = datetime.datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")        
            break  # Sortez de la boucle une fois que vous avez trouvé "creation_time"

    return dateOfDay
 
def copyFileTo(filePath, outDir, dateDir):
    outputDirDest=outDir+"\\"+str(dateDir)+r" - TBD"
    print(f"{filePath} copy to {outputDirDest}")
    
    if not os.path.exists(outputDirDest):
        os.makedirs(outputDirDest,exist_ok=True)
   
    dstname = os.path.join(outputDirDest, file)
    copyfile(filePath, dstname)
    
if __name__ == "__main__":

    if os.path.exists(outputDir):
        rmtree(outputDir)

    # r=root, d=directories, f = files
    for r, d, f in os.walk(inputDir):
        for file in f:         
            fileFullPath=os.path.join(r, file)
                                   
            if fileFullPath.lower().endswith(('.jpg', '.jpeg')):
                creation_date = get_exif_creation_date(fileFullPath)
            elif fileFullPath.lower().endswith('.mp4'):
                creation_date = get_mp4_creation_date(fileFullPath)
            else:
                raise Exception(f"ERROR: Format de fichier non pris en charge: {fileFullPath}.")
                        
            if creation_date is None:
                raise Exception(f"ERROR: creation_date non trouvé : {creation_date}.")
            
            copyFileTo(fileFullPath, outputDir, creation_date)
             
           
                
#print('Image {0} does not image: {1}'.format(image_path, str(e))) 

