from clubs.models import Club
from student_org_gov.tests_templates import TestModel

class TestClubModels(TestModel):
    def createModelData(cls):
        cls.club1 = Club.objects.create(
            full_name="FIRST",
            abbreviation="f",
        )
        cls.club2 = Club.objects.create(
            full_name="club with a long name here and spaces",
            abbreviation="longabbrvtoo",
        )
        cls.club3 = Club.objects.create(
            full_name="jacko",
            abbreviation="jj",
        )

    
    def test_club(self):
        self.assertModelCreation(
            {
                self.club1: {
                    "full_name": "FIRST",
                    "abbreviation": "f",
                    "url": "first"
                },
                self.club2: {
                    "full_name": "club with a long name here and spaces",
                    "abbreviation": "longabbrvtoo",
                    "url": "clubwithalongnamehereandspaces"
                },
                self.club3: {
                    "full_name": "jacko",
                    "abbreviation": "jj",
                    "url": "jacko"
                }
            }
        )
        self.assertModelFunction(
            function="__str__",
            data={
                self.club1: "FIRST",
                self.club2: "club with a long name here and spaces",
                self.club3: "jacko"
            }
        )