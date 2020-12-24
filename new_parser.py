



import json
import urllib
import re, collections
import os
import pdftotext
import difflib
import subprocess
import spacy
from spacy.matcher import Matcher
from datetime import datetime
from dateutil import relativedelta
import docx
import requests
import html2text
import sys

h = html2text.HTML2Text()
h.ignore_links = True


# load pre-trained model

nlp = spacy.load('en_core_web_sm')
email = None
gender=None
mobile = None
name=None   
DOB = 0
degree = []
# initialize matcher with a vocab
edul = ['HighSchool','PreUniversity','Matriculation','BA', 'BArch', 'BBABMS', 'BCom', 'BDes', 'BEd', 'BElEd', 'BPEd', 'BPharm', 'BS', 'BSc', 'BTech', 'BE', 'BUMS', 'BAMS', 'BCA', 'BDS', 'BFA', 'BHM', 'BHMS', 'BVSC', 'CA', 'CS', 'Diploma', 'DM', 'Doctorate', 'Graduation', 'HigherSecondary', 'HSArts', 'HSCommerce', 'HSScience', 'ICWA', 'IntegratedPG', 'LLB', 'LLM', 'MA', 'MArch', 'MCh', 'Mcom', 'MDes', 'MEd', 'MPharm', 'MPhil', 'MSMSc', 'MTech', 'MBA', 'MBBS', 'MCA', 'MCM', 'MDS', 'MedicalMSMD', 'MFA', 'MVSC', 'PGDiploma', 'PGDM', 'PhD', 'PostGraduation', 'Primary', 'Seconday']


def input_file_lines(input_text):
	tokens = input_text.split("\n")
	words=re.split('\s+|\n', input_text)
	return tokens,words

def init(filename):

    ############################################################
    ### Convert pdf to txt with pdf miner and start a write file
    ############################################################

    # input the file name
    resume=""
    
    if filename == " ":
        return ("", "")   
    elif filename.endswith(".pdf"):
        with open(filename, "rb") as f:
            total = pdftotext.PDF(f)
            for page in total:
                resume+=page
    elif filename.endswith(".doc") or filename.endswith(".docx"):
        doc = docx.Document(filename)
        for para in doc.paragraphs:
            resume+=para.text
    else: 
        resume = readFile(filename)
        if filename.endswith(".html"):
            resume = h.handle(resume)
    # return resume as a string with different sections
    # print(resume)
    return resume



def main(resume):
    global gender,name,email,mobile,DOB,degree
    # initialize variables 
    # have the words as tokens in a list
    tokens,word_tokens = input_file_lines(resume)
    # word_tokens = tokenize1.input_file_words(resume,[])
    
    # print(edu,exp,pro,"lalala")
    MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'''
    MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'''
    MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r'|[1-9]|0[1-9]|1[0-2])'
    YEAR = r'(((20|19)\d{2}))'
    Date = r'([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/|\s|[,])([1-9]|0[1-9]|1[0-2]|'+ MONTH+ r')(\.|-|/|\s)([3-9][0-9]|[0][0-5]|19[0-9][0-9]|200[0-5])$'
    
    exp_ = []
    backup = []
    seen = 0
    prev=""
    span=None
    span2=None
    for j in range(len(tokens)):
        token = tokens[j]
        if re.search(r'E(xperience|XPERIENCE)(s|S)?|P(revious|REVIOUS) W(ork|ORK)(s|S)?|I(nternship|NTERNSHIP)(s|S)?',token):
            # print(token)
            seen = 1
            if len(backup)==0:
                backup=tokens[j+1:j+8]
        if seen and len(exp_)<7:
            # print(token)
            oldregex= r'(?P<fmonth>\w+.\d*)\s*(-|to)\s*(?P<smonth>\w+.\d+|present)'
            tryregex = r'((('+MONTH+r'\s+)?'+YEAR+r')|(('+MONTH+r'\s+)('+YEAR+r')?))\s*(-|to)\s*((('+MONTH+r'\s+)?'+YEAR+r')|\s\s+present$|^present\s\s+)'
            experience = re.search(
                tryregex,token,re.I)
            if experience:
                # print(experience)
                exps = token.replace(experience[0],"")
                if len(re.sub(r'\W+', '', exps))==0:
                    exps = prev+token.replace(experience[0],"")
                ends= re.split(r'\s+to\s+|\s*-\s*',experience[0])
                exp_.append({"title":re.sub(' +', ' ', exps),"start":ends[0],"end":ends[1]})
            else:
                trial = re.search(r'(('+MONTH+r'\s+)?'+YEAR+r')|\s\s+present$|^present\s\s+',token,re.I)
                if trial:
                    exps = token.replace(trial[0],"")
                    if len(re.sub(r'\W+', '', exps))==0:
                        exps = prev+token.replace(trial[0],"")
                    # print(exps)
                    exp_.append({"title":re.sub(' +', ' ', exps),"start":trial[0],"end":trial[0]})
                
        prev = token
        if name is None:
            nlp_text = nlp(token)
            matcher = Matcher(nlp.vocab)
            matcher.add('NAME', None, [{'POS': 'PROPN'}, {'POS': 'PROPN'}])
            matches = matcher(nlp_text)
            matcher2 = Matcher(nlp.vocab)
            matcher2.add('Fist Name', None, [{'POS': 'PROPN'}])
            matches2 = matcher2(nlp_text)
            for match_id, start, end in matches:
                span = nlp_text[start:end]
                break
            for match_id, start, end in matches2:
                span2 = nlp_text[start:end]
                break
            if span2 is not None:
                if span is not None:
                    if span2.text==span.text.split(" ")[0]:
                        name = span.text
                    else:
                        name = span2.text
                else:
                    name = span2.text
        if mobile is None:
            mobile= re.search("(?:(?:\+|0{0,2})91(\s*[\ -]*\s*)?|[0]?)?[789]\d{9}|(\+91|91)?(\s*[\ -]*\s*)?\d{5}([ -]?)(\d{5})|(\d[ -]?){10}\d$",token)
            if mobile is not None:
                mobile = mobile[0]
        if not DOB:
            DOB = re.search(Date,token,re.I)
            if DOB is not None:
                DOB = DOB[0]
    prev=""
    for j in range(len(word_tokens)):   
        token=word_tokens[j]
        if "@" in token and email is None:
            email = re.search(r'[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}',token)[0]
        if gender is None:
            if token in ["Female","female","girl","Girls","girls","girl's","Girl's","Girl","Woman","Women"]:
                gender = "Female"
            elif token in ["Male","male","Boy","boy","boys","boy's","Boys","Boy's","Man","Men"]:
                gender = "Male"
       
        new = re.sub('\W+','',prev+token)
        new2 = re.sub('\W+','',token)
        if new2 in edul:
            degree.append(new2)
            # print(new,token)
        elif  new in edul:
            degree.append(new)
            # print(new,prev+token)
        prev=token   

    if len(exp_)==0:
        for i in backup:
            if re.search('\w',i):
                exp_.append(re.sub("\s\s+|\n"," ",i))     
    # print ("Finished parsing.")
    return {"Email":email,"Mobile":mobile,"Name": name,"Gender (M/F)" :gender,"DOB":DOB,"Education List":list(set(degree)),"Experience List":exp_}
def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()



if __name__ == '__main__':
    fileName = sys.argv[1]
    resume = init(fileName)
    print(main(resume))
    
