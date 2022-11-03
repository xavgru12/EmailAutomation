import yaml
import os #create dir in sendEmail, already imported by emailClient
from emailClient import SendMessage
#import emailClient

sender="xaver.max.gruber@googlemail.com"

def main():
    data=createDummyData()
    #exampleReadDataFromStructure(data)
    writeDataToFile(data)
    dataFromFile=loadDataFromFile()
    contacts=extractContactsFromData(dataFromFile)
    iterateOverContactsToSendEmail(contacts)
    #contacts=readDataFromFile(data)
    #sendEmail(contacts)

def createDummyData():

    contactInfo = {
        'contactname': 'TestKontaktMaennlich1',
        'email': 'xaver.max.gruber+test1@gmail.com',
        'sex': 'm'

    }

    contactInfo3 = {
        'contactname': 'TestKontaktWeiblich3',
        'email': 'xaver.max.gruber+test3@gmail.com',
        'sex': 'f'

    }

    contactInfo4 = {
        'contactname': 'TestKontaktWeiblich4',
        'email': 'xaver.max.gruber+test4@gmail.com',
        'sex': 'f'

    }

    contactInfo2 = {
        'contactname': 'TestKontaktMaennlich2',
        'email': 'xaver.max.gruber+test2@gmail.com',
        'sex': 'm'

    }
    company_name1="zhuelke"
    company= [contactInfo, contactInfo2]
    #print(company)
    contacts = [contactInfo, contactInfo2]
    contacts2 = [contactInfo3, contactInfo4]
    companies = {
        'CompanyName': company_name1,
        'contactInfo': contacts
    }
    companies2 ={
        'CompanyName': company_name1,
        'contactInfo': contacts2

    }
    company_list = [companies, companies2]
    return company_list


# company_list = [companies, companies2]
# completeCompanies = ["Companies: ", company_list]


def readDataFromFile(company_list):
    
    dirnameToCreate= "Model"
    if not os.path.exists(dirnameToCreate):
        os.makedirs(dirnameToCreate)
    with open("Model/Output.yaml", mode="wt", encoding="utf-8") as file:
        yaml.dump(company_list, file)


    with open("Model/Output.yaml", mode="r") as file:
        dataFromYaml = yaml.load(file, Loader=yaml.FullLoader)

    companyWithContacts= dataFromYaml
    return companyWithContacts

def contactInfoOutput(company, contact_dict):
    email_address= contact_dict['email'] #important info for now is just
    print("email: "+ email_address)
    sex= contact_dict['sex']
    name=contact_dict['contactname']

def writeDataToFile(company_list):
    dirnameToCreate= "Model"
    if not os.path.exists(dirnameToCreate):
        os.makedirs(dirnameToCreate)
    with open("Model/Output.yaml", mode="wt", encoding="utf-8") as file:
        yaml.dump(company_list, file)


def loadDataFromFile():
    with open("Model/Output.yaml", mode="r") as file:
        dataFromYaml = yaml.load(file, Loader=yaml.FullLoader)

    companyWithContacts= dataFromYaml
    return companyWithContacts

def extractContactsFromData(companyWithContacts):
    contact_list=[]
    for contactsByCompany in companyWithContacts:
        print("company name: ")
        companyName= contactsByCompany['CompanyName']
        print(companyName)
        
        contacts= contactsByCompany['contactInfo']
        contact_list.extend(contacts)
    
    return contact_list

def iterateOverContactsToSendEmail(contacts):
    for contact in contacts:
        takeDataToSendEmail(contact, "CatchUp")

def exampleReadDataFromStructure(companyWithContacts):
    for contactsByCompany in companyWithContacts:
        print("company name: ")
        companyName= contactsByCompany['CompanyName']
        print(companyName)
        print("all contacts:")
        
        contacts= contactsByCompany['contactInfo']
        print(contacts)
        for contact in contacts:
            contactInfoOutput(companyName, contact)
        print("complete company info: ")
        print(contactsByCompany)
        print()
        print()
        print()


    #print("data from yaml:")
    #print(dataFromYaml)

def sendMaleEmail(base_path,email):

        
        with open(base_path+"/TextMale.txt","r") as file:
            text=file.read()
                
        with open(base_path+"/SubjectMale.txt","r") as file:
            subject=file.read()

        if text is not None and subject is not None:
            SendMessage(sender, email, subject, "", text)
            

def sendFemaleEmail(base_path, email):
        with open(base_path+"/TextFemale.txt","r") as file:
            text=file.read()

        with open(base_path+"/SubjectFemale.txt","r") as file:
            subject=file.read()

        if text is not None and subject is not None:
            SendMessage(sender, email, subject, "", text)
            #SendMessage(sender, to, subject, msgHtml, msgPlain)
    


def takeDataToSendEmail(contact_dict, folder_name):
    base_path="./Model/"+folder_name
    if not os.path.exists(base_path):
        raise("Folder could not be found")

    email_address= contact_dict['email']
    name= contact_dict['contactname']
    sex=contact_dict['sex']
    print("email will be sent to: "+email_address)
    if email_address is not None and name is not None:
        if sex is "f":
            sendFemaleEmail(base_path, email_address)
        elif sex is "m":
            sendMaleEmail(base_path, email_address)
        else:
            raise("unknown sex type")
    else:
        raise("missing data")
        
    
    #SendMessage(sender, to, subject, msgHtml, msgPlain)

if __name__ == '__main__':
    main()