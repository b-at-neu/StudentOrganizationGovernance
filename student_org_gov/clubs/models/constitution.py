import json

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
    