from django.core.validators import MinValueValidator 
from django.db import models

from clubs.models.article import Article
from student_org_gov.models import duplicating_model


class Section(duplicating_model.DuplicatingModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, editable=False, related_name="sections", default=None)

    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=None)
    content = models.CharField(max_length=10000, default=None)

    def __str__(self) -> str:
        return f'Section {self.number}: {self.content}'