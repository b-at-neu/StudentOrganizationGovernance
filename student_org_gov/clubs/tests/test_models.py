from clubs.models import Club, Constitution, Article, Section
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
        cls.constitution1 = Constitution.objects.create(
            club=cls.club1,
            status=Constitution.Status.APPROVED,
        )
        cls.constitution2 = Constitution.objects.create(
            club=cls.club2,
            status=Constitution.Status.DENIED,
        )
        cls.constitution3 = Constitution.objects.create(
            club=cls.club3,
            status=Constitution.Status.EDITED,
        )
        cls.article1 = Article.objects.create(
            constitution=cls.constitution1,
            number=1,
            title="first title"
        )
        cls.article2 = Article.objects.create(
            constitution=cls.constitution1,
            number=2,
            title="second title"
        )
        cls.article3 = Article.objects.create(
            constitution=cls.constitution2,
            number=1,
            title="another title"
        )
        cls.section1 = Section.objects.create(
            article=cls.article1,
            number=1,
            content="here's a bit of content"
        )
        cls.section2 = Section.objects.create(
            article=cls.article1,
            number=2,
            content="some OTHER content"
        )
        cls.section3 = Section.objects.create(
            article=cls.article3,
            number=1,
            content="and the final one"
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
        # Some complex funcs remain untested so far
        self.assertModelFunction(
            function="__str__",
            data={
                self.club1: "FIRST",
                self.club2: "club with a long name here and spaces",
                self.club3: "jacko"
            }
        )
        self.assertModelFunction(
            function="get_recently_submitted_constitutions",
            data={
                self.club1: [self.constitution1],
                self.club2: [self.constitution2],
                self.club3: []
            }
        )
        self.assertModelFunction(
            function="get_recently_approved_constitutions",
            data={
                self.club1: [self.constitution1],
                self.club2: [],
                self.club3: []
            }
        )


    def test_constitution(self):
        self.assertModelCreation(
            {
                self.constitution1: {
                    "club": self.club1,
                    "status": Constitution.Status.APPROVED,
                    "submitted_timestamp": None,
                    "reviewed_timestamp": None,
                },
                self.constitution2: {
                    "club": self.club2,
                    "status": Constitution.Status.DENIED,
                    "submitted_timestamp": None,
                    "reviewed_timestamp": None,
                },
                self.constitution3: {
                    "club": self.club3,
                    "status": Constitution.Status.EDITED,
                    "submitted_timestamp": None,
                    "reviewed_timestamp": None,
                }
            }
        )
        # __str__ func not testable because of timestamp dependancy
        self.assertModelFunction(
            function="url",
            data={
                self.constitution1: "00000004",
                self.constitution2: "00000005",
                self.constitution3: "00000006"
            }
        )

    
    def test_article(self):
        self.assertModelCreation(
            {
                self.article1: {
                    "constitution": self.constitution1,
                    "number": 1,
                    "title": "first title"
                },
                self.article2: {
                    "constitution": self.constitution1,
                    "number": 2,
                    "title": "second title"
                },
                self.article3: {
                    "constitution": self.constitution2,
                    "number": 1,
                    "title": "another title"
                }
            }
        )
        self.assertModelFunction(
            function="__str__",
            data={
                self.article1: "Article 1: first title",
                self.article2: "Article 2: second title",
                self.article3: "Article 1: another title"
            }
        )

    
    def test_section(self):
        self.assertModelCreation(
            {
                self.section1: {
                    "article": self.article1,
                    "number": 1,
                    "content": "here's a bit of content"
                },
                self.section2: {
                    "article": self.article1,
                    "number": 2,
                    "content": "some OTHER content"
                },
                self.section3: {
                    "article": self.article3,
                    "number": 1,
                    "content": "and the final one"
                }
            }
        )
        self.assertModelFunction(
            function="__str__",
            data={
                self.section1: "Section 1: here's a bit of content",
                self.section2: "Section 2: some OTHER content",
                self.section3: "Section 1: and the final one"
            }
        )