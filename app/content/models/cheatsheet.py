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
    desc = models.TextField(blank=True, default='')
    creator = models.CharField(max_length = 200)
    grade = EnumChoiceField(UserClass, default=UserClass.FIRST)
    study = EnumChoiceField(UserStudy, default=UserStudy.DATAING)
    course = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Cheatsheets'

    def __str__(self):
        return f'Cheatsheet -{self.title} {self.desc} {self.creator} {self.sheet_course}'
    

    