import uuid

from django.db import models

from enumchoicefield import EnumChoiceField
from polymorphic.models import PolymorphicModel

from app.content.models.event import Event
from app.content.models.user import User
from app.forms.enums import EventFormType, FormFieldType
from app.util.models import BaseModel


class Form(PolymorphicModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Form"
        verbose_name_plural = "Forms"

    def __str__(self):
        return self.title


class EventForm(Form):

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="forms")
    type = EnumChoiceField(EventFormType, default=EventFormType.SURVEY)

    class Meta:
        unique_together = ("event", "type")
        verbose_name = "Event form"
        verbose_name_plural = "Event forms"


class Field(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    type = EnumChoiceField(FormFieldType, default=FormFieldType.TEXT_ANSWER)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class Option(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, default="")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="options")

    def __str__(self):
        return self.title


class Submission(BaseModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")

    class Meta:
        unique_together = ("form", "user")

    def __str__(self):
        return f"{self.user.user_id}'s submission to {self.form}"


class Answer(BaseModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="answers"
    )
    selected_options = models.ManyToManyField(
        Option, related_name="selected_in_answers", blank=True
    )
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name="answers", null=True, blank=True
    )
    answer_text = models.CharField(max_length=255, default="", blank=True, null=True)

    def get_field(self):
        return self.field if self.field else self.selected_options.first().field

    def saved(self, *args, **kwargs):
        """
        Aggregate the ids of the selected options and
        add them all at once to minimize database queries
        because of the many to many relation.
        """
        selected_options = kwargs.pop("selected_options")
        ids_of_options_to_add = []

        for selected_option in selected_options:
            ids_of_options_to_add.append(selected_option.id)

        self.selected_options.add(*ids_of_options_to_add)
        super().save()

    def __str__(self):
        return f"Answer to {self.submission}"