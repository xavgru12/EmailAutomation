from dataclasses import dataclass
from typing import List #initialize list with type

def main():
    my_data = ContactDetails('Xaver Gruber', 'Xaver', 'xaver.max.gruber@googlemail.com', 'm', 'TeamLead', 'German', False)
    print(my_data.full_name)
    my_company = CompanyData('Xavers Company', dict(team_lead=[my_data]))
    print(type(my_company.contacts['team_lead']))


@dataclass
class ContactDetails:
    full_name: str
    nick_name: str
    email: str
    sex: str
    function: str
    language: str 
    formality: bool 

@dataclass
class CompanyData:
    name: str
    contacts: dict(hr = List[ContactDetails], team_lead = List[ContactDetails], technical = List[ContactDetails])
    #initialize dict like this: dict(One = 70, Two = 45, Three = 75, Four = 83, Five = 9 )

if __name__ == '__main__':
    main()