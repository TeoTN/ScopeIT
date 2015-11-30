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
        print(proximity)
        self.assertTrue(type(proximity) == type(0.0))

