from dataclasses import dataclass
from EmailConfig import EmailConfig
from FileReader import FileReader
from ModelData import ModelData
from EmailData import EmailData

def main():
    config = EmailConfig(['zhuelke'], ['hr'], "CatchUp")
    fileReader = FileReader(config.context)
    modelDataObject = fileReader.createModelDataObject()
    print(modelDataObject)



    handler = EmailHandler(dict(), config, modelDataObject )
    companyNameWithFilteredContactsObjectsList=handler.getFilteredContactDetailsObjects()
    handler.iterateThroughCompaniesToCreateEmailDataObjects(companyNameWithFilteredContactsObjectsList)


@dataclass
class EmailHandler: #emailHandler is supposed to create EmailData objects
    data_dictionary: dict
    emailConfig: EmailConfig
    modelData: ModelData

    def getFilteredContactDetailsObjects(self):
        #company_list = []
        companyNameWithContactsList=[]
        for company in self.emailConfig.companiesToSend:
            companyNameWithContactsList.append(self.filterContactsByFunction(company))

        return companyNameWithContactsList


    def filterContactsByFunction(self, company):
        companyData=self.data_dictionary[company]
        company_name= companyData.name
        if not company_name == company:
            raise("dictionary data error")

        contactsToSend=[]
        for function in self.emailConfig.functionsToSend:
            contactsByFunction = companyData.contacts[function]
            contactsToSend.extend(contactsByFunction)

        return [company_name, contactsToSend]

    def iterateThroughCompaniesToCreateEmailDataObjects(self, company_list): #useDataToWriteText(self, company_list):
        email_data_list=[]
        for company_data in company_list:
            email_details_objects=self.createEmailDataObjects(company_data)
            email_data_list.extend(email_details_objects)

        return email_data_list


    def createEmailDataObjects(self, company):

        company_name = company[0]
        contact_objects = company[1]

        email_data_list=[]

        for contact in contact_objects:
            text = self.createTextFromTemplate(company_name, contact)
            subject = self.createSubjectFromTemplate(contact)
            receiver = contact.email
            email_data = EmailData(receiver, subject, text)
            email_data_list.append(email_data)

        return email_data_list


    def createTextFromTemplate(self, company_name, contact):
        #company_name not used for now, could use it in future

        language=contact.language #format is first letter is capital, eg English
        if contact.sex == 'm':
            sex = "Male"
        elif contact.sex == "f":
            sex = "Female"

       #modelData for greeting: dict expects key formatted like this: GermanMale
       

       #get correct greeting (language and sex)
        if contact.formality is True:
            greeting=self.modelData.greetingFormal[language+sex]
        elif contact.formality is False:
            greeting=self.modelData.greetingInformal[language+sex]

        #modelData for content: dict expects language, eg English
        content= self.modelData.content[language]

        text=f"{greeting} {contact.nick_name},\n{content}"

        return text

    def createSubjectFromTemplate(self, contact):
        language= contact.language                 #formatted like English
        subject = self.modelData.subject[language] #modeldata dict expects format: English
        
        return subject


if __name__ == '__main__':
    main()