# Resume Parser

Hi! Why spend money on third-party softwares or APIs, all you have to do is just download code and run it!. 
Here is the SIMPLE  and EFFICIENT **RESUME PARSER**


## Capabilities

 - [x] **FULL NAME :** Using detection of first and second proper noun in the resume using NLP.
 - [x] **MOBILE NUMBER :** Using regular expression finds an indian landline/mobile number.
 - [x] **EMAIL:** Using regular expression finds a valid email.
 - [x] **GENDER:** Using NLTK searches for gender related words.
 - [x] **DOB:** Using regular expression finds a Date of Birth.
 - [x] **Experience List :** Using regular expression traverses to this section and lists the titles of the experiences in the same order.
 - [x] **Education List :** Using regular expression traverses to this section and lists all the indian standard qualifications.

## Files
 - `new_parser.py` - Main Program
 - `1.pdf` - Demo Resume 1
 - `2.pdf` - Demo Resume 2
 
Isn't it Awsm, Just one file doing all the **magic!**

## How to Setup
**Dependencies**
 1. Python 3
 2. pip install html2text
 3. pip install spacy
 4. pip install difflib
 5. pip install pdftotext
 6. pip install urllib

## How To Run


> **Step 1 :** Place the file in the same folder as the program file.

> **Step 2 :** Open the terminal the run the below command.

`python3 new_parser.py <filename>`

Here's the Output you get:
```sequenceDiagram
{'Email': 'navneetpandey94@gmail.com', 'Mobile': '+91 9954961533', 'Name': 'Navneet Pandey', 'Gender (M/F)': None, 'DOB': None, 'Education List': ['MTech', 'BTech'], 'Experience List': [' Industrial Training at IPGCL.New Delhi', ' Area of training includes the Power Generation Station, Protection of Electrical Equip-', ' ment, Switch Yard, Safety Equipment, Backup Protection.', ' Industrial Training at Logicon Automation', ' Area of training includes the Basics of PLC and SCADA and Ladder Programming of', ' Allen Bradley PLC.']}
```
