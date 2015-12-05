from accounts.models import Entity, Skill

CAPACITY = 1


class Comparator(object):
    def __init__(self):
        self.skills = list(Skill.objects.all())
        self.distances = {}

    def eval(self, role):
        role_skills = list(role.get_skills())
        role_skills_vector = {role_skill.skill.name: self.get_skill_value(role_skill) for role_skill in role_skills}
        for skill in self.skills:
            role_skills_vector[skill.name] = role_skills_vector.get(skill.name, 0)
        return role_skills_vector, len(role_skills)

    def get_proximity(self, requirement, offer):
        req_id = requirement.id
        off_id = offer.id
        cached = self.distances.get((req_id, off_id), None)
        if cached:
            return cached
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
        result = round(proximity/coeff, 2)
        self.distances[(req_id, off_id)] = result
        return result

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
    __last_id = 0

    def __init__(self, entity):
        self.__entity = entity
        self.match = None
        self.comparator = Comparator()
        self.id = AcceptingRole.__last_id
        AcceptingRole.__last_id += 1

    def prefers(self, comparable):
        current = self.comparator.get_proximity(self, self.match)
        proposed = self.comparator.get_proximity(self, comparable)
        return proposed > current

    def get_username(self):
        return self.__entity.user_profile.user.username

    def get_skills(self):
        return self.__entity.userskill_set.all()

    def save_match(self):
        if self.match:
            self.__entity.match = self.match.get_entity()
            self.__entity.save()


class ProposingRole(object):
    __last_id = 0

    def __init__(self, entity, receivers, **kwargs):
        self.__entity = entity
        self.id = ProposingRole.__last_id
        ProposingRole.__last_id += 1
        self.capacity = CAPACITY
        self.last_proposal = 0
        self.comparator = Comparator()
        self.receivers = receivers
        self.preference_list = self.__build_preference_list()

    def __build_preference_list(self):
        pref_list = sorted(self.receivers[:], key=lambda receiver: self.comparator.get_proximity(self, receiver), reverse=True)
        return pref_list

    def get_skills(self):
        return self.__entity.userskill_set.all()

    def get_username(self):
        return self.__entity.user_profile.user.username

    def get_next(self):
        self.last_proposal += 1
        return self.preference_list[self.last_proposal - 1]

    def get_entity(self):
        return self.__entity


class Matcher(object):
    def __init__(self):
        self.jobs = Entity.objects.filter(user_profile__is_employer=True).exclude(skills=None)
        self.applicants = Entity.objects.filter(user_profile__is_employer=False).exclude(skills=None)
        self.receivers = [AcceptingRole(applicant) for applicant in self.applicants]
        self.proposers = [ProposingRole(job, self.receivers) for job in self.jobs]
        self.jobs_count = len(self.proposers)
        self.applicants_count = len(self.receivers)
        self.not_matched = self.proposers[:]

    def run(self):
        while len(self.not_matched):
            proposer = self.not_matched[0]
            receiver = proposer.get_next()

            if receiver.match is None:
                receiver.match = proposer
                proposer.capacity -= 1
            elif receiver.prefers(proposer):
                old_match = receiver.match
                old_match.capacity += 1
                self.not_matched.append(old_match)
                receiver.match = proposer
                proposer.capacity -= 1

            if proposer.last_proposal >= self.applicants_count or proposer.capacity == 0:
                self.not_matched.remove(proposer)
        self.save_matching()

    def print_matching(self):
        for receiver in self.receivers:
            receiver_name = receiver.get_username()
            match_name = "nobody" if not receiver.match else receiver.match.get_username()
            print("{} has matched {}".format(receiver_name, match_name))

    def save_matching(self):
        for receiver in self.receivers:
            receiver.save_match()