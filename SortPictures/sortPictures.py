#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os 
import datetime 
from shutil import copyfile
from shutil import copy
from shutil import rmtree
import PIL.Image as PILimage



inputDir =r'D:\Users\Bureautique\Desktop\SaveKris2\Camera'
outputDir=r'D:\Users\Bureautique\Desktop\SaveKris2\CameraSorted'

SplitTypes = []

def getAllExt(directory):
    for r, d, f in os.walk(directory):
        for file in f:
            SplitTypes.append(file.split(".")[-1])
    print(sorted(set(SplitTypes)) )


def getCreationTimeInFileName(filename):
    if "-" in filename:
        r = filename.split("-")[1]
    elif "_" in filename:
        r = filename.split("_")[0]
    else:
        r = None

    return r


if __name__ == "__main__":

    if os.path.exists(outputDir):
        rmtree(outputDir)

    getAllExt(inputDir)

    # r=root, d=directories, f = files
    for r, d, f in os.walk(inputDir):
        for file in f:         
                fileFullPath=os.path.join(r, file)
                try:
                     
                    img = PILimage.open(fileFullPath)
                    exif = img.getexif()
                    creation_time = exif.get(36867)
                    if creation_time is not None:
                        result = datetime.datetime.strptime(creation_time, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d")
                    else:
                        result = getCreationTimeInFileName(file)
                except Exception as e:
                    result = getCreationTimeInFileName(file) 

                print(fileFullPath+ " > " +  str(result))
                outputDirDest=outputDir+"\\"+str(result)+r" - TBD"

                if not os.path.exists(outputDirDest):
                    os.makedirs(outputDirDest,exist_ok=True)
               
                dstname = os.path.join(outputDirDest, file)


                copyfile(fileFullPath, dstname)

