import re
import datetime 
from . import textMiner
from .models import Document



def getMail(raw_text):
    
    try:
            mail=re.search('\w+.\w+@\w+.\w+',raw_text).group()
            mail=[i for i in mail.split(' ') if '@' in i]
            mail=mail[0]
            print('---> Mail: '+mail)
            
    
    except:
        
        mail='none'
        print('---> Mail '+mail)
    
    return mail


def getName(raw_text):
    
    try:
            name=re.search(r'((?<= nome )|(?<= name )|(?<=nome:)|(?<=name:)|(?<=nome :)|(?<=name :))(\s*)(\w+\s+\w+)',raw_text).group()
            name=re.search('\w+\s+\w+',name).group()
            print('---> Name: '+name)
            
    except:
            name=getMail(raw_text)
            print('---> Name: '+name)
    
    return name


def getCompany(raw_text):
    
    try:
        
        company=re.search(r'((?<=azienda)|(?<=company)|(?<=azienda:)|(?<=company:)|(?<=azienda :)|(?<=datore di lavoro:)|(?<=company :)|(?<=presso )|(?<=datore di lavoro ))(\s*)(\w+)',raw_text).group()
        company=re.search('\w+',company).group()
        print('---> Company: '+company)
            
    except:
        
        company='None'
        print('---> Company: '+company)
    
    return company


def getJt(raw_text):
    
    keys=['(?<=tipo di impiego)','(?<=tipo di impiego:)','(?<=attuale posizione:)','(?<=attuale posizione:)',
              '(?<=posizione attuale:)','(?<=attuale posizione ricoperta:)','(?<=attuale posizione ricoperta: )',
              '(?<=ruolo attuale:)','(?<=ruolo attuale)','(?<=ruolo attuale )']
        
    try:
        
        jt=re.search(r'('+keys[0]+'|'+keys[1]+'|'+keys[2]+'|'+keys[3]+'|'+keys[4]+'|'+keys[5]+'|'+keys[6]+'|'+keys[7]+'|'+keys[8]+'|'+keys[9]+')(\s*)(\w+\s*\w+)',raw_text).group()
#       j=re.search('\w+',j).group()
        print('---> Job Title: '+jt)
    except:
        
        jt='None'
        print('---> Job Title: '+jt)
    
    return jt 


def getMobile(raw_text):
    
    try:
        
        mobile=re.search('(3\d\d/\d\d\d\d\d\d\d)|(3\d\d-\d\d\d\d\d\d\d)|(3\d\d\d\d\d\d\d\d\d)|(3\d\d\s\d\d\d\d\d\d\d)|(3\d\d\s\d\d\s\d\d\s\d\d\d)|(3\d\d\s\d\d\d\s\d\d\d\d)',raw_text).group()
        print('---> Mobile: '+mobile)

    except:
            mobile=0
            print('---> Mobile: '+str(mobile))
    
    return mobile


def getLocation(raw_text):
    
    try:
        location=re.search(r'(((?<=via )(.*)\d[–,-,_,,,/] \d* \w*)|((?<=via )(.*)\d [–,-,_,,,/] \w*)|((?<=via )(.*)\d[–,-,_,,,/] \w*)|((?<=via )(.*)\d*\n\d*\w*\s*\w*))',raw_text[:500]).group().split(' ')[-1]
        # loc=re.search(r'(((?<=via )(.*)\d [-,_,,,/] \w*)|((?<=via )(.*)\d[-,_,,,/] \w*)|((?<=via )(.*)\d*\n\d*\w*\s*\w*))',rr[:500]).group().split(' ')[-1]
        print("---> Location: "+location)
        
    except:
        location='none'
        print("Error in the location function!!!")
    
    return location


def getAge(raw_text):

    try:
        age=re.search(r'((\d\d/\d\d/\d\d\d\d)|(\d\d-\d\d-\d\d\d\d)|(\d\d/\d\d/\d\d))',raw_text[:1000]).group()
        if re.search(r'(\d\d\d\d)',age)!=None:
            age=re.search(r'(\d\d\d\d)',age).group()
        else:
            age='19'+age[-2:]
        age=datetime.date.today().year-datetime.date(int(age),6,1).year
        print('---> Age: '+str(age))
            
    except:
        age=0
        print("Error in the age function!!!")
    
    return age
            

def getEducation(raw_text):
    
    education=[]
    for i in ['laurea','bachelor','master degree','laureato','laureata']:
        if i in raw_text:
            education.append(i)
    if len(education)>0:
        education='University'
    else:
        education='Other'
    print('---> Education : '+education)
    return education
        

def getTags(raw_text):
    
    corpus=[textMiner.tokenizedText(i.l) for i in Document.objects.all()]
    tokens=textMiner.tokenizedText(raw_text)
    tags=textMiner.getTag(corpus,tokens)
    return tags
       

def getAuthor(documentInstance):
    
    return documentInstance.author


    




    
    