from dataclasses import dataclass
from ModelData import ModelData


def main():
    fileReader = FileReader("CatchUp")
    #print(fileReader.context)
    fileReader.createModelDataObject()



@dataclass
class FileReader:
    context: str

    def createModelDataObject(self):
        formalGreetingDict = self.getFormalGreeting("./Model/General/GreetingFormal.txt")
        informalGreetingDict = self.getInformalGreeting("./Model/General/GreetingInformal.txt")
        contentDict = self.getContent("./Model/"+self.context+"/Content.txt")
        subjectDict = self.getSubject("./Model/"+self.context+"/Subject.txt")

        modelData = ModelData(contentDict, subjectDict, formalGreetingDict,  informalGreetingDict)

        return modelData


    def getFormalGreeting(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def getInformalGreeting(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def getContent(self, filepath):
        fileAsDict= self.parseFile(filepath, "")
        return fileAsDict

    def getSubject(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def parseFile(self, filepath, buffer_strip="\n"):
        content={}
        with open(filepath, mode="r") as file:
            buffer=""
            name=""

            for line in file: 
                marker_line=self.checkIfMarkerLine(line, '#')

                if not marker_line:
                    buffer+=line.rstrip(buffer_strip)    #add line to buffer as it is no markerLine with '#'
                elif marker_line:
                    if name != "":                      #only add data to dictionary if name is not empty, eg at first markerLine in file
                        content[name]=buffer            # add buffer content to dict
                        buffer=""                       #reset buffer after it is put in content dictionary
                    name=line.rstrip('\n').lstrip('#')  #save name which will be added in dict next iteration

            content[name]=buffer                        #add last data in dict as for loop ended and no next iteration of loop available

        return content

    def checkIfMarkerLine(self, line, marker):
        if marker in line:
            return True
        else: 
            return False



if __name__ == '__main__':
    main()