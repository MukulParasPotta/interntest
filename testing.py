import io
import os
import re

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def parameterPrint(str):
    match_date= ""
    match_degree = ""
    reg_date = "((((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec))|((January)|(February)|(March)|(April)|(May)|(June)|(July)|(August)|(September)|(October)|(November)|(December)))(\s((1(st){0,1})|(2(nd){0,1})|(3(rd){0,1})|([0-9]{1,2}(th){0,1}))){0,1}\s?,{0,1}\s\d\d\d\d)|([0-9]{1,2}\s?[-.|\/]{1}\s?[0-9]{1,2}\s?[-.|\/]{1}\s?[0-9]{4})|(((1(st){0,1})|(2(nd){0,1})|(3(rd){0,1})|([0-9]{1,2}(th){0,1}))\s(((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec))|((January)|(February)|(March)|(April)|(May)|(June)|(July)|(August)|(September)|(October)|(November)|(December)))\s[0-9]{4})|(([0-9]{4}-)[0-9]{4})"
    reg_degree = "(Bachelor of Science)|(Bachelor of Engineering)|((Bachelor of Commerce)|(B.Com))|((Bachelor of Computer Application)|(BCA))|((Bachelor of Hotel Management)|(BHM))|((Bachelor of Business ((Management)|(Administration)))|(BBA))|((Bachelor of Law)|(LLB))|((Bachelor of Fashion Technology)|(BFT))|((Bachelor of Commerce)|(B.Com))|((Bachelor of Computer Application)|(BCA))|((Bachelor of Hotel Management)|(BHM))|((Bachelor of Business Management)|(BBA))|((Bachelor of Law)|(LLB))|((Bachelor of Technology)|(B.(\s){0,1}Tech))|((Bachelor of Medicine)|(MBBS))|(Bachelor of Arts)|((Master(s)? (degree|program)? (of|in) Science)|(MS))|((Master(s)? (degree|program)? (of|in) Engineering))|((Master(s)? (degree|program)? (of|in) Commerce)|(M.Com))|((Master(s)? (degree|program)? (of|in) Business ((Management)|(Administration)))|(MBA))|((Master(s)? (degree|program)? (of|in) Fine Arts)|(MFA))|((Master(s)? (degree|program)? (of|in) Computer Application)|(MCA))|((Master(s)? (degree|program)? in Management)|(MIM))|((Master(s)? (degree|program)? (of|in) Technology)|(M.\s{0,1}Tech))|((Master(s)? (degree|program)? (of|in) Arts))"
    match_date_obj = re.search(reg_date,str)
    if match_date_obj == None:
        print("date not found")
    else:
        match_date  = match_date_obj.group()
    match_degree_obj = re.search(reg_degree,str)
    if match_degree_obj == None:
        print("degree not found")
    else:
        match_degree = match_degree_obj.group()
    return [match_date,match_degree]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="VisionApiTest-b5708e0fda63.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'deg/degree/rr.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.text_detection(image=image)
labels = response.text_annotations

str_ig = ""
str_ig = labels[0].description

print(str_ig)
    
stri = str_ig.lower()
flag = (stri.find("degree") >= 0 or stri.find("master") >= 0 or stri.find("masters") >= 0 or stri.find("bachelors") >= 0 or stri.find("bachelor") >= 0 or stri.find("diploma") >= 0 or stri.find("doctor") >= 0) 

response = client.label_detection(image=image)
labels = response.label_annotations

stri = ""

#print('Labels:')
for label in labels:
    stri += " " + label.description

stri = stri.lower()
flag2 = stri.find("academic certificate") >= 0 or stri.find("diploma") >= 0 or stri.find("degree")>=0

if flag and flag2 :
    print("It is a Degree Certificate.")
    lis = parameterPrint(str_ig)
    print("DATE : ",lis[0],"\n","DEGREE : ",lis[1])
    
else :
    print("Not a Degree Certificate.")
    exit()



