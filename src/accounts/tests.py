from django.test import TestCase
from accounts.stable_matching.matcher import *
from accounts.models import *


class TestComparator(TestCase):
    fixtures = ['dump']
    def setUp(self):
        self.entities = Entity.objects.all()
        self.comparator = Comparator()

    def test_should_make_comparison(self):
        job_offer = ProposingRole(self.entities[2])
        applicant = AcceptingRole(self.entities[3])
        proximity = self.comparator.get_proximity(job_offer, applicant)
        print("Case 1", proximity)
        self.assertTrue(type(proximity) == type(0.0))

    def test_should_make_comparison2(self):
        job_offer = ProposingRole(self.entities[4])
        applicant = AcceptingRole(self.entities[5])
        proximity = self.comparator.get_proximity(job_offer, applicant)
        print("Case 2", proximity)
        self.assertTrue(type(proximity) == type(0.0))

    def test_should_make_comparison3(self):
        job_offer = ProposingRole(self.entities[6])
        applicant = AcceptingRole(self.entities[7])
        proximity = self.comparator.get_proximity(job_offer, applicant)
        print("Case 3", proximity)
        self.assertTrue(type(proximity) == type(0.0))


class TestPreferenceList(TestCase):
    fixtures = ['dump']

    def setUp(self):
        self.entities = Entity.objects.all()

    def test_build_pref_list(self):
        role = ProposingRole(self.entities[6])
        for applicant, proximity in role.preference_list:
            print(applicant.get_username(), proximity)
        self.assertIsNotNone(role.preference_list)


