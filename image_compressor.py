import os
from re import A
from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener
import shutil
import time

register_heif_opener()
FILE_COUNTER = 0
def resize(fileObject):
	width, height = fileObject.size
	isLandscape = width>height
	if isLandscape:
		minWidth = 1920
		minHeight = 1080
	else:
		minWidth = 1080
		minHeight = 1920

	if width<minWidth or height<minHeight:
		return None
	else:
		widthRatio = width/minWidth
		heightRatio = height/minHeight
		ratio = min(widthRatio,heightRatio)

		fileObject = fileObject.resize((int(fileObject.size[0]/ratio),int(fileObject.size[1]/ratio)),Image.Resampling.LANCZOS)
	return fileObject

def createFolderForFile(savedFilePath):
	folderToCreate = os.path.dirname(savedFilePath)
	if not os.path.exists(folderToCreate):
		os.makedirs(folderToCreate)

def saveImage(filePath,savedFilePath):
	try:
		fileObject = Image.open(filePath)
	except UnidentifiedImageError:
		saveFile(filePath,savedFilePath)
		return
	
	fileObject = resize(fileObject)
	if fileObject is None:
		saveFile(filePath,savedFilePath)
		return
	else:
		createFolderForFile(savedFilePath)
		fileObject.save(savedFilePath, format='jpeg', optimize=True, quality=80, lossless=False)

def saveFile(filePath,savedFilePath):
	createFolderForFile(savedFilePath)
	shutil.copyfile(filePath, savedFilePath)	# dst: C:/Users/acgab/Desktop/image_compressor/drive_images/filename.jpg

def saveAllImages(path, rootPath, newRootPath):
	global FILE_COUNTER
	files = os.listdir(path)
	for file in files:
		fullPath = path + "/" + file
		if os.path.isdir(fullPath):
			saveAllImages(fullPath, rootPath, newRootPath)
		elif os.path.isfile(fullPath): 
			_, fileExtension = os.path.splitext(fullPath)

			newPath = fullPath.replace(rootPath,newRootPath)
			if fileExtension.upper() in ['.JPG','.JPEG','.PNG']:
				saveImage(fullPath,newPath)
			elif fileExtension.upper() in ['.HEIC']:
				newPath = newPath.replace('.HEIC','.jpeg')
				saveImage(fullPath,newPath)
			else:
				saveFile(fullPath,newPath)
			FILE_COUNTER += 1

start = time.time()
rootPath = "C:/temp/drive_image"
newRootPath = "C:/temp/optimized"
saveAllImages(rootPath,rootPath,newRootPath)
end = time.time()
print(end - start)
print(f"number of processed files: {FILE_COUNTER}")