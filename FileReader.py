from dataclasses import dataclass


def main():
    fileReader = FileReader("CatchUp")
    print(fileReader.context)
    data=fileReader.getFormalGreeting("./Model/General/GreetingFormal.txt")
    print(data)



@dataclass
class FileReader:
    context: str

    def createModelDataObject(self):
        formalGreetingDict = self.getFormalGreeting("./Model/General/GreetingFormal.txt")
        informalGreetingDict = self.getInformalGreeting("./Model/General/GreetingInformal.txt")
        contentDict = self.getContent("./Model/"+self.context+"/Content.txt")
        subjectDict = self.getSubject("./Model/"+self.context+"/Subject.txt")

    def getFormalGreeting(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def getInformalGreeting(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def getContent(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def getSubject(self, filepath):
        fileAsDict= self.parseFile(filepath)
        return fileAsDict

    def parseFile(self, filepath):
        content={}
        with open(filepath, mode="r") as file:
            buffer=""
            name=""
            for line in file: #really complicated logic, try with yield and next() to split up logic
                if '#' in line:
                    if buffer == "":
                        name=line.rstrip('\n').lstrip('#')
                        continue
                    if name:
                        content[name]=buffer
                        buffer=""
                    name=line.rstrip('\n').lstrip('#')
                    continue
                buffer+=line.rstrip('\n')

        return content

"""
                    #buffer+=line
                else=
            while "#" not in file:
                value = next(file).rstrip('\n')
                buffer+=value
            yield buffer
  
            next(file); next(file)  # ignore first two lines
            value = next(file).rstrip('\n')  # read what should be the first number
            while "#" not in value:#value != '#extra':  # not end-of-numbers marker
                buffer+=value
                yield value
                value = next(file).rstrip('\n')"""





if __name__ == '__main__':
    main()