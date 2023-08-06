import abc


class AbstractJSON(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_data):
        return NotImplemented

    @abc.abstractmethod
    def to_json(self):
        return NotImplemented


class City(object):
    def __init__(self, city_name, state):
        self.city_name = city_name
        self.state = state


class Education(AbstractJSON):
    def __init__(self, school_name, degree, start_date, end_date, city):
        self.school_name = school_name
        self.degree = degree
        self.start_date = start_date
        self.end_date = end_date
        self.city = city

    @classmethod
    def from_json(cls, json_data):
        json_data['city'] = City(**json_data['city'])

        return cls(**json_data)

    def to_json(self):
        json_data = self.__dict__.copy()
        json_data['city'] = self.city.__dict__.copy()

        return json_data


class WorkExperience(AbstractJSON):
    def __init__(self, company_name, title, start_date, end_date, bullitons, city):
        self.company_name = company_name
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.bullitons = bullitons
        self.city = city

    @classmethod
    def from_json(cls, json_data):
        json_data['city'] = City(**json_data['city'])

        return cls(**json_data)

    def to_json(self):
        json_data = self.__dict__.copy()
        json_data['city'] = self.city.__dict__.copy()

        return json_data


class Person(AbstractJSON):
    def __init__(self, first_name, last_name, job_title, summary, skills, education, work_experience,
                 address, phone_number, email_address, linkedin_profile):
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.summary = summary
        self.skills = skills
        self.education = education
        self.work_experience = work_experience
        self.address = address
        self.phone_number = phone_number
        self.email_address = email_address
        self.linkedin_profile = linkedin_profile

    @classmethod
    def from_json(cls, json_data):
        education = [Education.from_json(x) for x in json_data['education']]
        work_experience = [WorkExperience.from_json(x) for x in json_data['work_experience']]
        json_data['education'] = education
        json_data['work_experience'] = work_experience

        return cls(**json_data)

    def to_json(self):
        json_data = self.__dict__.copy()
        education = [education.to_json() for education in self.education]
        work_experience = [work_experience.to_json() for work_experience in self.work_experience]
        json_data['education'] = education
        json_data['work_experience'] = work_experience

        return json_data.copy()
