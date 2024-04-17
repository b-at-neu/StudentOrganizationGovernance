import uuid

from django.core.validators import MinValueValidator 
from django.db import models

from clubs.models.constitution import Constitution
from student_org_gov.models import duplicating_model


class Article(duplicating_model.DuplicatingModel):
    class Meta:
        unique_together = ["constitution", "did"]

    constitution = models.ForeignKey(Constitution, on_delete=models.CASCADE, editable=False, related_name="articles", default=None)

    # Duplicate ID field, identifies the same article even across multiple constitutions
    did = models.UUIDField(default=uuid.uuid4, editable=False)

    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=None)
    title = models.CharField(max_length=200, default=None)

    def __str__(self) -> str:
        return f'Article {self.number}: {self.title}'