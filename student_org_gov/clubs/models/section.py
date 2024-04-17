import uuid

from django.core.validators import MinValueValidator 
from django.db import models

from clubs.models.article import Article
from student_org_gov.models import duplicating_model


class Section(duplicating_model.DuplicatingModel):
    class Meta:
        unique_together = ["article", "did"]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, editable=False, related_name="sections", default=None)

    # Duplicate ID field, identifies the same section even across multiple constitutions
    did = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)

    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=None)
    content = models.CharField(max_length=10000, default=None)

    def __str__(self) -> str:
        return f'Section {self.number}: {self.content}'