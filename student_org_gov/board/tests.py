import time

from clubs.models import Club, Constitution
from student_org_gov.tests_templates import TestView
from users.models import RoleUser

############
# View Tests
############

class TestBoardViews(TestView):
    def createModelData(cls):
        # Create clubs
        cls.club1 = Club.objects.create(
            full_name="test1",
            abbreviation="test1"
        )
        cls.club2 = Club.objects.create(
            full_name="test2",
            abbreviation="test2"
        )
        cls.club1.save()
        cls.club2.save()

        # Delete default generated const for club1
        cls.club1.constitutions.all().last().delete()

        # Create constitutions
        cls.const1 = cls.club1.create_constitution({
            "article1": [
                "section1",
                "section2"
            ],
            "article2": [
                "section3"
            ]
        })
        cls.const1.status = Constitution.Status.APPROVED
        cls.const1.save()
        time.sleep(0.0001)
        cls.const2 = cls.club1.create_constitution({
            "article1": [
                "section1",
                "different section"
            ],
            "article2": [
                "section3"
            ]
        })
        cls.const2.status = Constitution.Status.SUBMITTED
        cls.const2.save()


    def test_board_overview_page(self):
        self.assertPageView(
            url="board",
            url_args={},
            template="board/board_overview.html",
            context={
                "club_list":[
                    {
                        "club_model": self.club1,
                        "recent_approved_constitution": self.const1,
                        "recent_submitted_constitution": self.const2,
                    },
                    {
                        "club_model": self.club2,
                        "recent_approved_constitution": None,
                        "recent_submitted_constitution": None,
                    }
                ]
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


    def test_review_constitution_page(self):
        self.assertPageView(
            url="review_constitution",
            url_args={ "club_url": self.club1.url, "constitution_pk": self.const2.pk },
            template="board/review_constitution.html",
            context={
                "club": self.club1,
                "new_constitution": self.const2,
                "all_articles": [
                    {
                        "new": self.const2.articles.get(number=1),
                        "old": self.const1.articles.get(number=1),
                        "sections": [
                            {
                                "new": self.const2.articles.get(number=1).sections.get(number=1),
                                "old": self.const1.articles.get(number=1).sections.get(number=1)
                            },
                            {
                                "new": self.const2.articles.get(number=1).sections.get(number=2),
                                "old": self.const1.articles.get(number=1).sections.get(number=2)
                            }
                        ]
                    },
                    {
                        "new": self.const2.articles.get(number=2),
                        "old": self.const1.articles.get(number=2),
                        "sections": [
                            {
                                "new": self.const2.articles.get(number=2).sections.get(number=1),
                                "old": self.const1.articles.get(number=2).sections.get(number=1)
                            }
                        ]
                    }
                ]
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