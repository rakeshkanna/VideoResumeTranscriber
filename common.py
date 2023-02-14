import random
import re

def generatelabelsjson(my_file,jobLevels,jobfunctions,jobIndustries,jobTitles):
    offsets=[]
    labels=[]
    json_string =""
    for jobLevel in jobLevels:
        for match in re.finditer(jobLevel,my_file):
            print(match)
            if (match.start() not in offsets) and (jobLevel not in labels):
                labels.append(jobLevel)
                offsets.append(match.start())
                json_string+='{'
                json_string+='"category": "JobLevel",'
                json_string+=f'"offset":{match.start()},'
                json_string+=f'"length":{len(jobLevel)}'
                json_string+='},'
    for jobFunction in jobfunctions:
        for match in re.finditer(jobFunction,my_file):
            if (match.start() not in offsets) and (jobFunction not in labels):
                offsets.append(match.start())
                labels.append(jobFunction)
                json_string+='{'
                json_string+='"category": "JobFunction",'
                json_string+=f'"offset":{match.start()},'
                json_string+=f'"length":{len(jobFunction)}'
                json_string+='},'
    for jobIndustry in jobIndustries:
        for match in re.finditer(jobIndustry,my_file):
            if (match.start() not in offsets) and (jobIndustry not in labels):
                offsets.append(match.start())
                labels.append(jobIndustry)
                json_string+='{'
                json_string+='"category": "JobIndustry",'
                json_string+=f'"offset":{match.start()},'
                json_string+=f'"length":{len(jobIndustry)}'
                json_string+='},'
    for jobTitle in jobTitles:
        for match in re.finditer(jobTitle,my_file):
            if (match.start() not in offsets) and (jobTitle not in labels):
                    offsets.append(match.start())
                    labels.append(jobTitle)
                    json_string+='{'
                    json_string+='"category": "JobTitle",'
                    json_string+=f'"offset":{match.start()},'
                    json_string+=f'"length":{len(jobTitle)}'
                    json_string+='},'
    return json_string

def generateresume_fromSeed(seed_document,cleanNames,jobLevels,jobfunctions,jobIndustries,jobTitles):
    emaildomains = ["@live.com","@hotmail.com","@yahoo.com","@gmail.com"]
    for i in range(20):
        random_Name = random.choice(cleanNames)
        random_jobfunctions = ','.join(random.choices(jobfunctions,k=3))
        random_jobLevel = random.choice(jobLevels)
        random_jobTitle =random.choice(jobTitles)
        random_jobIndustries = ','.join(random.choices(jobIndustries,k=3))
        random_domain = random.choice(emaildomains)
        random_mobile = str(random.randint(9000000000,9999999999))
        document_path = "D:\\models\\Seed\\"+seed_document
        with open(document_path) as f:
            document = f.read()
        document = document.replace('[YourName]',random_Name).replace('[JobLevel]',random_jobLevel)
        document = document.replace('[JobTitle]',random_jobTitle).replace('[JobIndustry]',random_jobIndustries)
        document = document.replace('[Email]',random_Name.replace(" ","")+random_domain)
        document = document.replace('[Company]','Coforge')
        document= document.replace('[phone]', random_mobile)
        document = document.replace('[Experience]',str(random.randint(5,15))).replace('[JobFunction]',random_jobfunctions)
        gen_path = "D:\\models\\Resumes\\texts\\Samples\\"+seed_document+"_gen"+str(i)+".txt"
        with open(gen_path,'w') as f:
            f.write(document)

def getUserNameOffset(resumetext,nlp1):
    json_string=""
    docx1 = nlp1(resumetext)
    for i, token in enumerate(docx1.ents):
        if token.label_ =="PERSON":
            if(i==0):
                json_string+='{'
                json_string+='"category": "UserName",'
                json_string+=f'"offset":{token.start_char},'
                json_string+=f'"length":{len(token.text)}'
                json_string+='},'
                return json_string

def getEmailOffset(resumetext):
    json_string=""
    for match in re.finditer(r'[\w.+-]+@[\w-]+\.[\w.-]+', resumetext):
        json_string+='{'
        json_string+='"category": "Email",'
        json_string+=f'"offset":{match.start()},'
        json_string+=f'"length":{match.end()-match.start()}'
        json_string+='},'
    return json_string

def getPhoneOffset(resumtext):
    json_string = ""
    regex= r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))"
    for match in re.finditer(regex, resumtext):
        json_string+='{'
        json_string+='"category": "Phone",'
        json_string+=f'"offset":{match.start()},'
        json_string+=f'"length":{match.end()-match.start()}'
        json_string+='},'
    return json_string
