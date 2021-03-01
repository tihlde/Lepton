from django.contrib import admin

from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from app.forms import models

admin.site.register(models.Field)
admin.site.register(models.Option)
admin.site.register(models.Submission)
admin.site.register(models.Answer)


class OptionInline(admin.TabularInline):
    model = models.Option


class FieldInline(admin.TabularInline):
    model = models.Field
    inlines = (OptionInline,)


class FormChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """

    base_model = models.Form  # Optional, explicitly set here.


@admin.register(models.EventForm)
class EventFormAdmin(FormChildAdmin):
    base_model = models.EventForm
    show_in_index = True  # makes child model admin visible in main admin site
    inlines = (FieldInline,)


@admin.register(models.Form)
class FormAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """

    base_model = models.Form
    child_models = (models.EventForm, models.Form)
    pk_regex = "([\\w-]+)"
    list_filter = (PolymorphicChildModelFilter,)
    inlines = (FieldInline,)
