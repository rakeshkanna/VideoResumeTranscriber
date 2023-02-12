import random
import spacy

def generatelabelsjson(my_file,jobLevels,jobfunctions,jobIndustries,jobTitles):
    offsets=[]
    labels=[]
    json_string =""
    for jobLevel in jobLevels:
        result = my_file.find(jobLevel)
        if (result > 0) and (result not in offsets) and (jobLevel not in labels):
            labels.append(jobLevel)
            offsets.append(result)
            json_string+='{'
            json_string+='"category": "JobLevel",'
            json_string+=f'"offset":{result},'
            json_string+=f'"length":{len(jobLevel)}'
            json_string+='},'
    for jobFunction in jobfunctions:
        result = my_file.find(jobFunction)
        if (result>0) and (result not in offsets) and (jobFunction not in labels):
            offsets.append(result)
            labels.append(jobFunction)
            json_string+='{'
            json_string+='"category": "JobFunction",'
            json_string+=f'"offset":{result},'
            json_string+=f'"length":{len(jobFunction)}'
            json_string+='},'
    for jobIndustry in jobIndustries:
        result = my_file.find(jobIndustry)
        if (result>0) and (result not in offsets) and (jobIndustry not in labels):
            offsets.append(result)
            labels.append(jobIndustry)
            json_string+='{'
            json_string+='"category": "JobIndustry",'
            json_string+=f'"offset":{result},'
            json_string+=f'"length":{len(jobIndustry)}'
            json_string+='},'
    for jobTitle in jobTitles:
        result = my_file.find(jobTitle)
        if (result>0) and (result not in offsets) and (jobTitle not in labels):
            offsets.append(result)
            labels.append(jobTitle)
            json_string+='{'
            json_string+='"category": "JobTitle",'
            json_string+=f'"offset":{result},'
            json_string+=f'"length":{len(jobTitle)}'
            json_string+='},'
    return json_string

def generateresume_fromSeed(seed_document,cleanNames,jobLevels,jobfunctions,jobIndustries,jobTitles):
    emaildomains = ["@live.com","@hotmail.com","@yahoo.com","@gmail.com"]
    for i in range(10):
        random_Name = random.choice(cleanNames)
        random_jobfunctions = ','.join(random.choices(jobfunctions,k=3))
        random_jobLevel = random.choice(jobLevels)
        random_jobTitle =random.choice(jobTitles)
        random_jobIndustries = ','.join(random.choices(jobIndustries,k=3))
        random_domain = random.choice(emaildomains)
        random_mobile = str(random.randint(9000000000,9999999999))
        document_path = "D:\\models\\Resumes\\texts\\Samples\\"+seed_document
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
