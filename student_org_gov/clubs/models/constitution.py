from django.db import models

import clubs.models as club_models
from student_org_gov.models import duplicating_model


class Constitution(duplicating_model.DuplicatingModel):
    class Status(models.IntegerChoices):
        APPROVED = 1, "Approved"
        DENIED = 2, "Denied"
        CONDITIONALLY_APPROVED = 3, "Conditionally Approved"
        EDITED = 4, "Edited"
        SUBMITTED = 5, "Submitted"

    club = models.ForeignKey(club_models.club.Club, on_delete=models.CASCADE, editable=False, related_name="constitutions", default=None)

    timestamp = models.DateTimeField(auto_now_add=True)
    submitted_timestamp = models.DateTimeField(null=True, default=None)
    reviewed_timestamp = models.DateTimeField(null=True, default=None)

    status = models.IntegerField(choices=Status, default=None)

    def __str__(self) -> str:
        return f'{self.club} ({self.timestamp.strftime("%m/%d/%Y, %H:%M")} ID{self.pk})'
    
    def url(self) -> str:
        return str(self.pk).zfill(8)
    
    def get_json(self):
        """
        Returns a JSON version of the model. Structure:
        {
            "pk": 0,
            "articles": [{
                "number": 0,
                "title": "x",
                "pk": 0
                "sections": [{
                    "number": 0,
                    "content": "x",
                    "pk": 0
                }]
            }]
        }
        """
        data = {}
        data["pk"] = self.pk
        data["articles"] = []

        # Add articles
        for article in club_models.Article.objects.filter(constitution_id=self.pk).order_by("number"):
            # Add sections
            sections = []
            for section in club_models.Section.objects.filter(article_id=article.pk).order_by("number"):
                sections.append({
                    "number": section.number,
                    "content": section.content,
                    "pk": section.pk
                })
            
            data["articles"].append({
                "number": article.number,
                "title": article.title,
                "pk": article.pk,
                "sections": sections
            })

        return data