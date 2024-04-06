from clubs.models import Club
from student_org_gov.tests_templates import TestModel
from users.models import RoleUser

class TestUserModels(TestModel):
    def createModelData(cls):
        cls.club = Club.objects.create(
            full_name="club",
            abbreviation="c",
            url="club"
        )
        cls.user1 = RoleUser.objects.create(
            username="testing123",
            role=RoleUser.Roles.BOARD_MEMBER,
            email="test@email.com",
            club=cls.club,
        )
        cls.user2 = RoleUser.objects.create(
            username="delta",
            email="fakeemail@a.c",
        )
        cls.user3 = RoleUser.objects.create(
            username="AAAAAAAAAAAAAAAAAAAAAAAAa",
            email="reallylongemailhere@hi.grandfinale",
            club=cls.club
        )

    
    def test_role_user(self):
        self.assertModelCreation(
            {
                self.user1: {
                    "username": "testing123",
                    "role": RoleUser.Roles.BOARD_MEMBER,
                    "email": "test@email.com",
                    "club": self.club
                },
                self.user2: {
                    "username": "delta",
                    "role": RoleUser.Roles.VIEWER,
                    "email": "fakeemail@a.c",
                    "club": None
                },
                self.user3: {
                    "username": "AAAAAAAAAAAAAAAAAAAAAAAAa",
                    "role": RoleUser.Roles.VIEWER,
                    "email": "reallylongemailhere@hi.grandfinale",
                    "club": self.club
                }
            }
        )
        self.assertModelFunction(
            function="has_admin_role",
            data={
                self.user1: False,
                self.user2: False,
                self.user3: False,
            }
        )
        self.assertModelFunction(
            function="has_board_role",
            data={
                self.user1: True,
                self.user2: False,
                self.user3: False,
            }
        )
        self.assertModelFunction(
            function="has_e_board_role",
            data={
                self.user1: False,
                self.user2: False,
                self.user3: False,
            }
        )
        self.assertModelFunction(
            function="__str__",
            data={
                self.user1: "testing123 (Board Member)",
                self.user2: "delta (Viewer)",
                self.user3: "AAAAAAAAAAAAAAAAAAAAAAAAa (Viewer)",
            }
        )

