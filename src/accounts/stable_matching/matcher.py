from queue import Queue
from accounts.models import Entity, Skill
from math import sqrt

CAPACITY = 5


class Comparator(object):
    def __init__(self):
        self.skills = list(Skill.objects.all())

    def eval(self, role):
        role_skills = list(role.get_skills())
        role_skills_vector = {role_skill.skill.name: self.get_skill_value(role_skill) for role_skill in role_skills}
        for skill in self.skills:
            role_skills_vector[skill.name] = role_skills_vector.get(skill.name, 0)
        return role_skills_vector, len(role_skills)

    def get_proximity(self, requirement, offer):
        req_vector, coeff = self.eval(requirement)
        off_vector, _ = self.eval(offer)
        proximity = 0.0
        for skill_name in req_vector:
            if req_vector[skill_name] == 0:
                continue
            elif off_vector[skill_name] >= req_vector[skill_name]:
                proximity += off_vector[skill_name]
            else:
                proximity += 2*off_vector[skill_name] - req_vector[skill_name]

        return round(proximity/coeff, 2)

    def get_skill_value(self, userskill):
        value = userskill.level**2
        type = userskill.skill.type
        if type == Skill.LANGUAGE:
            value *= 3.0
        elif type == Skill.FRAMEWORK:
            value *= 2.0
        elif type == Skill.LIBRARY:
            value *= 1.0
        elif type == Skill.TECHNOLOGY:
            value *= 0.8
        elif type == Skill.OS or type == Skill.TOOL:
            value *= 0.5
        return value


class AcceptingRole(object):
    def __init__(self, entity):
        self.__entity = entity
        self.__matches = None

    def prefers(self, comparator, comparable):
        pass

    def get_username(self):
        return self.__entity.user_profile.user.username

    def get_skills(self):
        return self.__entity.userskill_set.all()


class ProposingRole(object):
    def __init__(self, entity, **kwargs):
        self.__entity = entity
        self.__is_employer = entity.user_profile.is_employer
        self.capacity = CAPACITY
        self.last_proposal = 0
        self.comparator = Comparator()
        self.preference_list = self.__build_preference_list()

    def __build_preference_list(self):
        counterparts = Entity.objects.filter(user_profile__is_employer=not self.__is_employer)
        counterparts_roles = []
        for counterpart in counterparts:
            role = AcceptingRole(counterpart)
            proximity = self.comparator.get_proximity(self, role)
            counterparts_roles.append((role, proximity))
        pref_list = sorted(counterparts_roles, key=lambda agent: agent[1], reverse=True)
        return pref_list

    def get_skills(self):
        return self.__entity.userskill_set.all()

    def get_username(self):
        return self.__entity.user_profile.user.username


class Matcher(object):
    def __init__(self):
        self.queue = Queue()
        self.jobs = Entity.objects.filter(user_profile__is_employer=True)
        self.applicants = Entity.objects.filter(user_profile__is_employer=False)

