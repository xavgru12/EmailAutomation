from dataclasses import dataclass

def main():
    pass


@dataclass
class EmailConfig:
    companiesToSend: list
    functionsToSend: list
    emailContentFilepath: str
    greeting: str
    subject: str





if __name__ == '__main__':
    main()