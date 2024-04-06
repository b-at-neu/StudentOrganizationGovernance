from student_org_gov.tests_templates import TestView
from users.models import RoleUser

############
# View Tests
############

class TestBoardViews(TestView):
    def createModelData(cls):
        pass

    def test_home(self):
        self.assertPageView(
            url="home",
            url_args={},
            template="home/home.html",
            context={},
            anon_user_access=True,
            denied_access_roles=[],
            allowed_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )