from dataclasses import dataclass


def main():
    pass



@dataclass
class ModelData:
    content: dict #dict for different language versions eg German, English
    subject: dict
    greetingFormal: dict #dict with GermanMale, GermanFemale, EnglishMale, EnglishFemale
    greetingInformal: dict #dict with GermanMale, GermanFemale, EnglishMale, EnglishFemale




if __name__ == '__main__':
    main()