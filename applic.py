import yaml
import os 
from emailClient import SendMessage
from CompanyData import ContactDetails, CompanyData
from EmailConfig import EmailConfig
from EmailHandler import EmailHandler
from FileReader import FileReader
import argparse

sender="xaver.max.gruber@googlemail.com"
pathToDataFile=r"Model/Output.yaml"           #used in dummy creation writeDataToFile (for debugging)
databaseFile=r"./Model/CompanyDatabase.yaml"

def parseArguments():
    parser = argparse.ArgumentParser(description='Send emails automatically. Needed data structure: \n Model/<your_foldername>/Context.txt,\n  Model/<your_foldername>/Subject.txt, \nModel/General with GreetingFormal.txt, \nGreetingInformal.txt')
    parser.add_argument('--context','-ctxt', help='what the email is about, choose a name and put it as folder name under /Model/', required=True) 
    parser.add_argument('--function', '-f',
                    default=['all'],
                    nargs='*',
                    choices=['hr', 'team_lead', 'technical'], 
                    help='function of the contact within the company. Default is: %(default)s)') #argument can only be of item in choice list
    group = parser.add_mutually_exclusive_group(required=True) #need to either give argument --company or --companyTextList
    group.add_argument('--company', '-comp', action='extend', nargs='+', help=f'select companies to send email to. Write all to send to all companies') 
    group.add_argument('--companyTextList', '-compTxt', help='this function is currently not available') 
    
    args = parser.parse_args()

    return args
"""
    print(f"function: {args.function}")
    print(f"context: {args.context}")
    print(f"Company: {args.company}")
    print(f"CompanyTextList: {args.companyTextList}") """

 
def getContext(contextFromArgs):
    path_to_context_folder=f"./Model/{contextFromArgs}"
    if os.path.exists(path_to_context_folder) is True: #os.path.exists(os.path.join(os.getcwd(), fragment))
        return contextFromArgs
    else:
        raise Exception("context folder does not exist in ./Model/")

def getFunctionList(functionFromArgsList):
    if functionFromArgsList[0] == "all":
        return ['hr', 'team_lead', 'technical']
    else:
        return functionFromArgsList

def getCompanyList(args, company_dict):
    if args.companyTextList:
        raise("currently not possible to take a text file with companies to send emails to")
    if args.company is not None and "all" in args.company:
        complete_company_list=list(company_dict.keys())
        return complete_company_list
        #get all companies
    return [company.casefold() for company in args.company] #put companies as lower case in list
   
    


def main():

    #dummy data creation
    data=createDummyData()
    writeDataToFile(data) #for testing: Model/Output.yaml

    #Company Data with ContactDetails from file Model/Database.yaml
    dataFromFile=loadDataFromFile(databaseFile) #write function to verify data file by checking if all fields eg contacts, email, company name exist
    all_companies_data_dictionary=createInternalStructureFromFileData(dataFromFile)

    #parse arguments
    given_arguments=parseArguments()
    context=getContext(given_arguments.context)
    function_list= getFunctionList(given_arguments.function)
    company_list= getCompanyList(given_arguments, all_companies_data_dictionary)

    #put arguments in config object
    config = EmailConfig(company_list, function_list, context)
    print(config)

    #Model Data for email content
    fileReader = FileReader(config.context)
    modelDataObject = fileReader.createModelDataObject()

    #prepare content for email, as in handle email
    handler = EmailHandler(all_companies_data_dictionary, config, modelDataObject)
    companyNameWithFilteredContactsObjectsList=handler.getFilteredContactDetailsObjects()
    email_data_list = handler.iterateThroughCompaniesToCreateEmailDataObjects(companyNameWithFilteredContactsObjectsList)

    #TODO: before sending emails, create a temporary log file where the complete content of all the emails 
    # being sent are listed up with to, subject and content, user can check if its correct and
    # with (y/n) send all emails or abort

    sendMessages(email_data_list)


def createDummyData():

    contactDetails = {
        'contactFullName': 'TestKontaktMaennlich1',
        'contactNickName' : "NachnameMaennlich formality True sex M, English HR",
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
    company_name1="zuehlke"
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
    

def createInternalStructureFromFileData(company_list):

    company_dictionary={}
    for company in company_list:
        company_data_as_object, company_name= collectData(company)
        
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


def sendMessages(data_list):
    for email_data in data_list:
        to=email_data.to
        subject = email_data.subject
        content = email_data.content
        SendMessage(sender, to, subject, "", content)




if __name__ == '__main__':
    main()