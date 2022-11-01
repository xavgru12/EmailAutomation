from venv import create
import yaml
import os #create dir in sendEmail
import smtplib, ssl
#['zhuelke', 'Comet']
#company= [CompanyInfo, CompanyInfo]


def main():
    data=createDummyData()
    readData(data)
    sendEmail()

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


def readData(company_list):
    
    dirnameToCreate= "Model"
    if not os.path.exists(dirnameToCreate):
        os.makedirs(dirnameToCreate)
    with open("Model/Output.yaml", mode="wt", encoding="utf-8") as file:
        yaml.dump(company_list, file)


    with open("Model/Output.yaml", mode="r") as file:
        dataFromYaml = yaml.load(file, Loader=yaml.FullLoader)

    companyWithContacts= dataFromYaml




    # port = 465  # For SSL
    # smtp_server = "smtp.gmail.com"
    # sender_email = "xaver.max.gruber@googlemail.com"  # Enter your address
    # receiver_email = "xaver.max.gruber+TestEmail@gmail.com"  # Enter receiver address
    # password = input("Type your password and press enter: ")
    # message = """\
    # Subject: Hi there

    # This message is sent from Python."""

    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)





    def sendEmail(company, contact_dict):
        email_address= contact_dict['email']
        print("email: "+ email_address)
        sex= contact_dict['sex']
        name=contact_dict['contactname']

    for contactsByCompany in companyWithContacts:
        print("company name: ")
        companyName= contactsByCompany['CompanyName']
        print(companyName)
        print("all contacts:")
        
        contacts= contactsByCompany['contactInfo']
        print(contacts)
        for contact in contacts:
            sendEmail(companyName, contact)
        print("complete company info: ")
        print(contactsByCompany)
        print()
        print()
        print()


    #print("data from yaml:")
    #print(dataFromYaml)

def sendEmail():
    pass

if __name__ == '__main__':
    main()