from pathlib import Path
import os
import codecs
from pcu_json.json_configuration import setKeys
from pcu_json.json_parser import JSONParser
from pcu_json.json_parser import replaceExtension
from pcu_pdf.pcu_pdf import PDFParser

def pathExists(path):
	"""Check if a path exists.
	Parameter :
	path -- target path
	Return :
	true -- if path exists
	false -- if path does not exist
	"""
	pathfile = Path(path)
	return(pathfile.exists())

def isFile(path):
	"""Check if path represents a file.
	Parameter :
	path -- target path
	Return :
	true -- if path represents a file
	false -- if path does not represent a file
	"""
	file=Path(path)	
	return(file.is_file())

def isDirectory(path):
	"""Check if path represents a directory.
	Parameter :
	path -- target path
	Return :
	true -- if path represents a directory
	false -- if path does not represent a directory
	"""
	directory=Path(path)
	return(directory.is_dir())

def getFileList(directorypath):
	"""Return list of files contained in a directory and its subdirectories.
	Parameter :
	directorypath -- target directory path
	Return :
	filelist -- list of files contained in the directory and its subdirectories
	"""
	filelist=[] 
	originpath=os.getcwd() # current directory
	os.chdir(directorypath) # go to directory path
	thisdir = os.getcwd() # get directory path position
	for r, d, f in os.walk(thisdir): # recursively walk from directory path
		for file in f: 
			if file[-4:] == ".txt": # for each text file
				filelist.append(os.path.join(r, file)) # add to filelist
	os.chdir(originpath) # go back to original directory
	return filelist

def getContent(filepath):
	"""Return the textual content of a file.
	Parameter :
	filepath -- target file path
	Return :
	content - content of the file
	"""
	with open(filepath, 'r') as file:
  		content = file.read() # read file to get its content
	return content

def createTextFile(text,file):
	"""Create a text file with same filename as the original file and fill its content.
	Parameter :
	text -- content of the text file
	file -- original file represented by the text file created
	Return :
	textfile -- text file created from original file, with text as content
	"""
	#textfilename=file
	#pos = file.find('.') # beginning position of file format
	#if pos!=-1: # if file has an extension (".pdf", ".json", etc...) 
	#	textfilename = file[None:pos]+".txt" # get filename
	textfilename = replaceExtension(file, '.txt')
	textfile = open(textfilename, "a+") # create textfile
	textfile.write(text) # append content
	textfile.close() # close textfile
	return textfile


def getEquivalentTextfile(file):
	"""Get file's equivalent text file. 
	If file is a JSON, PDF, XML or HTML file, it creates the equivalent text file with the same content.
	Parameter :
	file -- original file
	Return :
	textfile -- equivalent text file
	"""
	print(file)
	print("_______")
	textfile=""
	if(file.endswith(".txt")):
		textfile=file # if file is already a text file, there is no change needed
	else:
		if(file.endswith(".json")): # if file is a JSON file
			setKeys("name_fr")
			textfile = JSONParser(file) # parse JSON file and create equivalent text file on the go
			reader = open(textfile,'r')
			content = reader.read()
			print(content)
		else :
			if(file.endswith(".pdf") or file.endswith(".xml") or file.endswith(".html")): # if file is compatible with Tika parser
				text = PDFParser(file) # parse file with Tika and get its textual content
				print(text)
				print("*****")
				textfile = createTextFile(text,file) # create equivalent text file from textual content and original file
			else:
				print("%s incompatible" % file) # otherwise, file format is incompatible
				pass
	return textfile	

if __name__ == '__main__':
	textfile = getEquivalentTextfile("/Users/zevio/Desktop/Desk/pcu_io/pcu_io/data/tika.pdf")
	print(textfile)