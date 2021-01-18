from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import pytest

from app.common.enums import AdminGroup
from app.content.factories.event_factory import EventFactory
from app.content.factories.user_factory import UserFactory
from app.forms.models.forms import Form


def _create_user_client(user_group):
    test_user = UserFactory(
        user_id="dev", password="123", first_name="member", last_name="user"
    )
    test_user.groups.add(Group.objects.create(name=user_group))
    token = Token.objects.get(user_id=test_user.user_id)
    client = APIClient()
    client.credentials(HTTP_X_CSRF_TOKEN=token)
    return client


def _event_url(event):
    return f"/api/v1/events/{event.id}/"


def _forms_url():
    return "/api/v1/forms/"


def _form_detail_url(form):
    return f"{_forms_url()}{form.id}/"


def _get_form_post_data(form):
    return {
        # "event": event.pk,
        "allow_photo": False,
    }


# def _get_registration_put_data(user, event):
#    return {
#        **_get_registration_post_data(user, event),
#        "is_on_wait": False,
#        "has_attended": False,
#    }


# GET /events
# Send med formet (read_only)
@pytest.mark.django_db
def test_retrieve_events():
    raise NotImplementedError()


# GET /events/<id>/
# Send med formet (read_only)
# Er brukeren admin?
# Send med all info fra den over (retrieve) pluss brukerens ubesvarte forms
# Dette feltet ligger på brukeren som "request.user.unanswered_forms()"
@pytest.mark.django_db
def test_retrieve_event():
    event = EventFactory()
    client = _create_user_client(AdminGroup.INDEX)
    response = client.get(_event_url(event))
    event = response.json()
    form = event.get("forms")[0]
    print(form)
    assert {"id": form.id, "type": form.type, "hidden": form.hidden} == {
        "id": event.id,
        "type": event.type,
        "hidden": event.hidden,
    }


# PUT /events/<id>/
# Oppdaterer ikke formet (sendes ikke med fra frontend)
@pytest.mark.django_db
def test_update_event():
    raise NotImplementedError()


# POST /events/
# Oppdaterer/lager ikke formet (sendes ikke med fra frontend)
@pytest.mark.django_db
def test_create_event():
    raise NotImplementedError()


@pytest.mark.django_db
def test_get_forms():
    raise NotImplementedError()
    form1 = None  # _create_form("foo")
    form2 = None  # _create_form("bar")
    client = _create_user_client(AdminGroup.INDEX)
    response = client.get(_forms_url())
    forms = response.json()
    print(forms)
    assert forms == [
        {
            "id": form1.id,
            "title": form1.title,
            "event": form1.event,
            "type": form1.type,
            "hidden": form1.hidden,
            "fields": form1.fields,
        },
        {
            "id": form2.id,
            "title": form2.title,
            "event": form2.event,
            "type": form2.type,
            "hidden": form2.hidden,
            "fields": form2.fields,
        },
    ]
    raise NotImplementedError()


@pytest.mark.django_db
def test_get_forms_permissions(user_group):
    raise NotImplementedError()


@pytest.mark.django_db
def test_get_form():
    raise NotImplementedError()


@pytest.mark.django_db
def test_create_forms():
    raise NotImplementedError()


@pytest.mark.django_db
@pytest.mark.django_db
def test_get_forms_permissions(user_group):
    raise NotImplementedError()


@pytest.mark.django_db
def test_get_form():
    raise NotImplementedError()


@pytest.mark.django_db
def test_create_forms():
    raise NotImplementedError()


@pytest.mark.django_db
def test_update_form():
    raise NotImplementedError()