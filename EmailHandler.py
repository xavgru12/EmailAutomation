from dataclasses import dataclass
from EmailConfig import EmailConfig

def main():
    config = EmailConfig(['zuehlke'], ['hr'], r"Model/CatchUp/TextMale.txt")
    handler = EmailHandler(dict(), config)
    print(handler.emailConfig)


@dataclass
class EmailHandler: #emailHandler is supposed to create EmailData objects
    data_dictionary: dict
    emailConfig: EmailConfig
    





if __name__ == '__main__':
    main()