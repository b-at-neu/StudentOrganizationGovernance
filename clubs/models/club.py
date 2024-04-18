import json

from django.db import models
from django.db.models import Q
from django.contrib.staticfiles import finders

import clubs.models as club_models


class ClubManager(models.Manager):
    def create(self, *args, **kwargs):
        """
        Runs when an object is created
        """
        kwargs["url"] = kwargs.get("full_name", "").replace(" ", "").lower()[:50]

        o = super(ClubManager, self).create(*args, **kwargs)

        # Create constitution
        if len(o.constitutions.all()) == 0:
            o.create_constitution(
                structure=json.load(open(finders.find("clubs/TEMPLATE_CONSTITUTION.json")))
            )

        return o


class Club(models.Model):
    objects = ClubManager()

    full_name = models.CharField(max_length=200, unique=True, default=None)
    url = models.CharField(max_length=50, unique=True, default=None)
    abbreviation = models.CharField(max_length=50, default=None)


    def create_constitution(self, structure, purpose="", affiliation="", dues_amount=""):
        """
        Structure example:
        {
            "article text": [
                "section text",
                "section text"
            ],
            "article text": [
                "section text"
            ]
        }
        """
        replacement_text = {
            "ORG_NAME": self.full_name,
            "ORG_ABBR": self.abbreviation,
            "PURPOSE": purpose,
            "AFFILIATION": affiliation,
            "DUES_AMOUNT": str(dues_amount),
        }

        from .article import Article
        from .section import Section
        
        # Replace text in json
        json_string = json.dumps(structure)
        
        for old, new in replacement_text.items():
            json_string = json_string.replace(old, new)

        new_structure = json.loads(json_string)

        # Create constitution
        constitution = club_models.constitution.Constitution.objects.create(club=self, status=club_models.constitution.Constitution.Status.EDITED)

        # Create articles
        for i, (article_text, sections) in enumerate(new_structure.items()):
            article = Article.objects.create(constitution=constitution, number=(i+1), title=article_text)

            # Create sections
            for j, section_text in enumerate(sections):
                Section.objects.create(article=article, number=(j+1), content=section_text)

        return constitution
    

    # Creates an edit version of the constitution if it doesn't exist yet
    def create_edit_constitution(self):
        constitution = club_models.constitution.Constitution.objects.filter(club=self).order_by('-timestamp').first()

        # Check if there is already an edit version
        if constitution.status != club_models.constitution.Constitution.Status.EDITED:
            # Copy old constitution
            constitution.deep_copy()

            # Change status
            constitution.status = club_models.constitution.Constitution.Status.EDITED
            constitution.save()

        return constitution
    

    def get_recently_submitted_constitutions(self):
        """
        Returns a queryset of submitted constitutions from the current club ordered by recent  
        """
        return self.constitutions.order_by("-timestamp").filter(~Q(status=club_models.Constitution.Status.EDITED))


    def get_recently_approved_constitutions(self):
        """
        Returns a queryset of approved constitutions from the current club ordered by recent  
        """
        return self.constitutions.order_by("-timestamp").filter(status=club_models.Constitution.Status.APPROVED)


    def __str__(self) -> str:
        return self.full_name