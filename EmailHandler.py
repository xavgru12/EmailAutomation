from dataclasses import dataclass
from EmailConfig import EmailConfig

def main():
    config = EmailConfig(['zhuelke'], ['hr'], r"Model/CatchUp/TextMale.txt", "Hallo", "Was ist der Stand?")
    handler = EmailHandler(dict(), config)
    #print(handler.emailConfig)
    companyNameWithFilteredContactsObjectsList=handler.getFilteredContactDetailsObjects()
    handler.iterateThroughCompaniesToCreateEmailDataObjects(companyNameWithFilteredContactsObjectsList)

#create text files for greeting, subject and textcontent
#in greeting.txt, versions of German, English, same for other .txts

@dataclass
class EmailHandler: #emailHandler is supposed to create EmailData objects
    data_dictionary: dict
    emailConfig: EmailConfig

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
        for company_data in company_list:
            self.createEmailDataObjects(company_data)
        
    def createEmailDataObjects(self, company):

        company_name = company[0]
        contact_objects = company[1]
        for contact in contact_objects:
            self.createTextFromTemplate(company_name, contact)
            #create subject
            #get receiver of email
            #create emailData object, maybe save objects in list of emailHandler class
        

    def createTextFromTemplate(self, company_name, contact):
        with open(self.emailConfig.emailContentFilepath, "r") as file:
            fileDummyData=file.read() #create function to choose English or German
        #print(fileDummyData)
        greeting=self.emailConfig.greeting #create function getGreeting to choose from language and as well formality
        subject = self.emailConfig.subject #create function to choose English or German
        message = f"{greeting} {contact.nick_name}"
        message=message+fileDummyData
        print()
        print()
        print()
        print("email content text:")
        print(message)

        #need a Parser that parses complete content and save it, give it to object emailConfig or create new one 
        #parser like this: Content.txt: #German in one line as marker and then content, for every language
        #greeting.txt #Formal and #Informal etc, get (r) correct sehr geehrte(r) for Male and Female


"""
        def each_chunk(stream, separator):

  buffer = ''
  while True:  # until EOF
    chunk = stream.read(CHUNK_SIZE)  # I propose 4096 or so
    if not chunk:  # EOF?
      yield buffer
      break
    buffer += chunk
    while True:  # until no separator is found
      try:
        part, buffer = buffer.split(separator, 1)
      except ValueError:
        break
      else:
        yield part
"""


    





if __name__ == '__main__':
    main()