# importing required modules 
from zipfile import ZipFile 
  
# specifying the zip file name 
file_name = "test.zip"
  
# opening the zip file in READ mode 
with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir() 
  
    # extracting all the files 
    zip.extractall()

    data = zip.read(test.zip)