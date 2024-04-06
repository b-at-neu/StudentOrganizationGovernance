from django.urls import reverse

from users.models import RoleUser
from clubs.models import Club
from student_org_gov.tests_templates import TestView

############
# View Tests
############

class TestClubViews(TestView):
    def createModelData(cls):
        cls.club1 = Club.objects.create(
            full_name="test",
            abbreviation="test",
            url="test"
        )
        cls.club2 = Club.objects.create(
            full_name="wrong",
            abbreviation="nope",
            url="wrong"
        )


    def test_clubs_page(self):
        self.assertPageView(
            url="clubs",
            url_args={},
            template="clubs/clubs.html",
            context={ "clubs": [ self.club1, self.club2 ] },
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


    def test_club_page(self):
        self.assertPageView(
            url="club",
            url_args={
                "club_url": self.club1.url
            },
            template="clubs/club.html",
            context={ "club": self.club1 },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_constitution_page(self):
        constitution = self.club1.constitutions.last()

        self.assertPageView(
            url="constitution",
            url_args={
                "club_url": self.club1.url,
                "constitution_pk": constitution.pk
            },
            template="clubs/constitution.html",
            context={ 
                "club": self.club1,
                "constitution": constitution,
                "articles": list(constitution.articles.all())
            },
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


    def test_edit_constitution_page(self):
        constitution = self.club1.constitutions.last()

        self.assertPageView(
            url="edit_constitution",
            url_args={
                "club_url": self.club1.url,
            },
            template="clubs/edit_constitution.html",
            context={
                "club": self.club1,
                "constitution": constitution,
                "articles": list(constitution.articles.all())
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_create_club_page(self):
        self.assertPageView(
            url="create_club",
            url_args={
            },
            template="clubs/create_club.html",
            context={
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )

    
    def test_delete_constitution(self):
        self.assertPostView(
            url="delete_constitution",
            url_args={},
            redirect_url=reverse("club", kwargs={ "club_url": self.club1.url }),
            post_data={
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

    
    def test_delete_club(self):
        self.assertPostView(
            url="delete_club",
            url_args={},
            redirect_url=reverse("clubs"),
            post_data={
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


    def test_submit_constitution(self):
        self.assertPostView(
            url="submit_constitution",
            url_args={ "club_url": self.club1.url },
            redirect_url=reverse("club", kwargs={ "club_url": self.club1.url }),
            post_data={
                "constitution": self.club1.constitutions.last().pk
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_review_constitution_approve(self):
        self.assertPostView(
            url="review_constitution",
            url_args={},
            redirect_url=reverse("clubs"),
            post_data={
                "constitution": self.club1.constitutions.last().pk,
                "decision": 1,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
            ],
            allowed_access_roles=[
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )


    def test_review_constitution_denied(self):
        self.assertPostView(
            url="review_constitution",
            url_args={},
            redirect_url=reverse("clubs"),
            post_data={
                "constitution": self.club1.constitutions.last().pk,
                "decision": 0,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.E_BOARD,
            ],
            allowed_access_roles=[
                RoleUser.Roles.BOARD_MEMBER,
                RoleUser.Roles.ADMIN
            ],
            club_denied=None,
            club_allowed=None,
        )


    def test_save_constitution_edits(self):
        self.assertPostView(
            url="save_constitution_edits",
            url_args={ "club_url": self.club1.url },
            redirect_url=reverse("constitution", kwargs={ "club_url": self.club1.url, "constitution_pk": self.club1.constitutions.last().pk }),
            post_data={
                "constitution": self.club1.constitutions.last().pk,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_remove_article_constitution(self):
        self.assertPostView(
            url="remove_article_constitution",
            url_args={},
            redirect_url=reverse("edit_constitution", kwargs={ "club_url": self.club1.url }),
            post_data={
                "article": self.club1.constitutions.last().articles.first().pk,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                #RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_remove_section_constitution(self):
        self.assertPostView(
            url="remove_section_constitution",
            url_args={},
            redirect_url=reverse("edit_constitution", kwargs={ "club_url": self.club1.url }),
            post_data={
                "section": self.club1.constitutions.last().articles.first().sections.first().pk,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                #RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_add_article_constitution(self):
        self.assertPostView(
            url="add_article_constitution",
            url_args={},
            redirect_url=reverse("edit_constitution", kwargs={ "club_url": self.club1.url }),
            post_data={
                "constitution": self.club1.constitutions.last().pk,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )


    def test_add_section_constitution(self):
        self.assertPostView(
            url="add_section_constitution",
            url_args={},
            redirect_url=reverse("edit_constitution", kwargs={ "club_url": self.club1.url }),
            post_data={
                "article": self.club1.constitutions.last().articles.first().pk,
            },
            anon_user_access=False,
            denied_access_roles=[
                RoleUser.Roles.VIEWER,
                RoleUser.Roles.BOARD_MEMBER,
            ],
            allowed_access_roles=[
                RoleUser.Roles.E_BOARD,
                RoleUser.Roles.ADMIN
            ],
            club_denied=self.club2,
            club_allowed=self.club1,
        )
