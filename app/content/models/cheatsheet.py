from django.db import models
from enumchoicefield import EnumChoiceField

from app.util.models import BaseModel
from app.content.enums import UserClass, UserStudy
import uuid

class Cheatsheet(BaseModel):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
    title = models.CharField(max_length=200)
    creator = models.CharField(max_length = 200)
    grade = EnumChoiceField(UserClass, default=UserClass.FIRST)
    study = EnumChoiceField(UserStudy, default=UserStudy.DATAING)
    course = models.CharField(max_length=200)
    url = models.URLField(max_length=600)

    class Meta:
        verbose_name = 'Cheatsheet'
        verbose_name_plural = 'Cheatsheets'

    def __str__(self):
        return f'Cheatsheet -{self.title} {self.creator} {self.grade} {self.study} {self.course}'