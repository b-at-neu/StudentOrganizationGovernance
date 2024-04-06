from django.urls import reverse
from student_org_gov.tests_templates import TestView
from users.models import RoleUser
from clubs.models import Club


class TestBoardViews(TestView):
    def createModelData(cls):
        cls.club1 = Club.objects.create(
            full_name="club1",
            abbreviation="club1",
            url="club1"
        )
        cls.user1 = RoleUser.objects.create(
            username="A",
            role=RoleUser.Roles.VIEWER,
            club=cls.club1,
            email="test@email.com"
        )


    def test_users_overview_page(self):
        self.assertPageView(
            url="users",
            url_args={},
            template="users/users.html",
            context={ 'users': RoleUser.objects.all(), 'roles': RoleUser.Roles.choices, 'clubs': Club.objects.all() },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )

    
    def test_edit_role(self):
        self.assertPostView(
            url="edit_role",
            url_args={},
            redirect_url=reverse("users"),
            post_data={
                "user": self.user1.pk,
                "role": RoleUser.Roles.E_BOARD
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )


    def test_edit_club(self):
        self.assertPostView(
            url="edit_club",
            url_args={},
            redirect_url=reverse("users"),
            post_data={
                "user": self.user1.pk,
                "club": self.club1.pk
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )


    def test_edit_club_none(self):
        self.assertPostView(
            url="edit_club",
            url_args={},
            redirect_url=reverse("users"),
            post_data={
                "user": self.user1.pk,
                "club": "None"
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )


    def test_signup(self):
        self.assertPageView(
            url="signup",
            url_args={},
            template="users/signup.html",
            context={},
            anon_user_access=True,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            allowed_access_roles=[],
            club_denied=None,
            club_allowed=None,
        )


    def test_login(self):
        self.assertPageView(
            url="login",
            url_args={},
            template="users/login.html",
            context={},
            anon_user_access=True,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            allowed_access_roles=[],
            club_denied=None,
            club_allowed=None,
        )

    
    def test_logout(self):
        self.assertPostView(
            url="logout",
            url_args={},
            redirect_url=reverse("home"),
            post_data={},
            anon_user_access=False,
            denied_access_roles=[
            ],
            allowed_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )