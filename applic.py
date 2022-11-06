import yaml
import os #create dir in sendEmail
from emailClient import SendMessage
from CompanyData import ContactDetails, CompanyData

sender="xaver.max.gruber@googlemail.com"
pathToDataFile=r"Model/Output.yaml"
emailContentFile = r"Model/CatchUp/TextMale.txt"

def main():

    #dummy data creation
    data=createDummyData()
    writeDataToFile(data)


    dataFromFile=loadDataFromFile(pathToDataFile) #write function to verify data file by checking if all fields eg contacts, email, company name exist
    all_companies_data_dictionary=createInternalStructureFromFileData(dataFromFile)
    print(all_companies_data_dictionary)

    #in order to send emails, need objects of CompanyData and Model/ text files for email content.
    #write class called EmailContent and give it object of CompanyData(all_companies_data_dictionary) and text files
    #functions methods to create new temp txt file with salutation and name company in text etc..


# """
#     dataFromFile=loadDataFromFile()
#     contacts=extractContactsFromData(dataFromFile)
#     iterateOverContactsToSendEmail(contacts)
#     #contacts=readDataFromFile(data)
#     #sendEmail(contacts)"""

def createDummyData():

    contactDetails = {
        'contactFullName': 'TestKontaktMaennlich1',
        'contactNickName' : "Herr NachnameMaennlich",
        'email': 'xaver.max.gruber+test1@gmail.com',
        'sex': 'm',
        'function' : 'HR',
        'language' : 'English',
        'formality' : True 

    }

    contactDetails3 = {
        'contactFullName': 'TestKontaktWeiblich3',
        'contactNickName' : "Vorname NachnameWeiblich",
        'email': 'xaver.max.gruber+test3@gmail.com',
        'sex': 'f',
        'function' : 'HR',
        'language' : 'German',
        'formality' : False 


    }

    contactDetails4 = {
        'contactFullName': 'TestKontaktWeiblich4',
        'contactNickName' : "Frau NachnameWeiblich",
        'email': 'xaver.max.gruber+test4@gmail.com',
        'sex': 'f',
        'function' : 'Technical',
        'language' : 'German',
        'formality' : True 

    }

    contactDetails2 = {
        'contactFullName': 'TestKontaktMaennlich2',
        'contactNickName' : "Vorname NachnameMaennlich",
        'email': 'xaver.max.gruber+test2@gmail.com',
        'sex': 'm',
        'function' : 'TeamLead',
        'language' : 'English',
        'formality' : False

    }
    #lastEdited would be useful when data is in a a database, for now it is a local file
    company_name1="zhuelke"
    company_name2="Swisson"
    contactList = [contactDetails, contactDetails2]
    contactList2 = [contactDetails3, contactDetails4]
    companyData = {
        'CompanyName': company_name1,
        'Contacts': contactList
    }
    companyData2 ={
        'CompanyName': company_name2,
        'Contacts': contactList2

    }
    company_list = [companyData, companyData2]
    return company_list


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
    email_address= contact_dict['email'] 
    print("email: "+ email_address)
    sex= contact_dict['sex']
    name=contact_dict['contactname']

def writeDataToFile(company_list):
    dirnameToCreate= "Model"
    if not os.path.exists(dirnameToCreate):
        os.makedirs(dirnameToCreate)
    with open("Model/Output.yaml", mode="wt", encoding="utf-8") as file:
        yaml.dump(company_list, file)


def loadDataFromFile(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError('cannot open data file')
    with open(file_path, mode="r") as file:
        try:
            return yaml.load(file, Loader=yaml.FullLoader)

        except yaml.YAMLError as e:
            print(e)
            raise
    
"""
    with open("Model/Output.yaml", mode="r") as file:
        dataFromYaml = yaml.load(file, Loader=yaml.FullLoader)

    companyWithContacts= dataFromYaml
    return companyWithContacts"""

def createInternalStructureFromFileData(company_list):

    company_dictionary={}
    for company in company_list:
        company_data_as_object, company_name= collectData(company)
        #print(company_data_as_object)
        
        if company_name not in company_dictionary:
            company_dictionary[company_name]= company_data_as_object
        else:
            print(company_name+" found twice.")
            raise Exception("Same company was found twice in data file. Remove the double from file.")
    
    return company_dictionary

def collectData(company):
    
    #get company name
    company_name=str(company['CompanyName']).casefold()
    if company_name == "":
        raise Exception("no company name was found in data file. Check file")
    
    #get contacts data
    contact_list=company['Contacts']

    #structure for ContactDetails objects
    contact_dictionary=dict(hr=[], team_lead=[], technical=[])

    #create ContactDetails objects and structure them via function dictionary
    for contact in contact_list:
        contact_object = constructContactDetailsObject(contact)
        contact_dictionary[contact_object.function].append(contact_object)

    #create CompanyData object
    company_data_object=CompanyData(company_name, contact_dictionary)

    return company_data_object, company_name

def constructContactDetailsObject(contact):
        full_name=contact['contactFullName']
        nick_name=contact['contactNickName']
        email=contact['email']
        sex=getContactSex(contact['sex'])
        function=getContactFunction(contact['function'])
        language=contact['language']
        formality=contact['formality']

        return ContactDetails(full_name, nick_name, email, sex, function, language, formality)

def getContactFunction(functionFromDataFile):

    if functionFromDataFile == 'HR':
        return 'hr'
    elif functionFromDataFile == 'TeamLead':
        return 'team_lead'
    elif functionFromDataFile == 'Technical':
        return 'technical'

def getContactSex(sexFromDataFile):

    if sexFromDataFile == 'm':
        return 'm'
    elif sexFromDataFile == 'f':
        return 'f'



def extractContactsFromData(companyWithContacts):
    contact_list=[]
    for contactsByCompany in companyWithContacts:
        print("company name: ")
        companyName= contactsByCompany['CompanyName']
        print(companyName)
        
        contacts= contactsByCompany['Contacts']
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

if __name__ == '__main__':
    main()