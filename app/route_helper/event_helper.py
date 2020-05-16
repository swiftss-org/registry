from app.models import Patient, Center, MeshType, User, Drug
from app.route_helper.choices import id_choices


def _populate_event_choices(session, form):
    form.patient_id.choices = id_choices(session, Patient, include_empty=False)
    form.center_id.choices = id_choices(session, Center, include_empty=False)


def population_followup_choices(session, form):
    _populate_event_choices(session, form)
    form.attendee_id.choices = id_choices(session, User, include_empty=False)


def populate_mesh_hernia_repair_choices(session, form):
    _populate_event_choices(session, form)

    form.mesh_type.choices = id_choices(session, MeshType, include_empty=False)
    form.primary_surgeon_id.choices = id_choices(session, User, include_empty=True)
    form.secondary_surgeon_id.choices = id_choices(session, User, include_empty=True)
    form.tertiary_surgeon_id.choices = id_choices(session, User, include_empty=True)


def _copy_to_event(form, event):
    event.type = form.type.data
    event.date = form.date.data
    event.patient_id = form.patient_id.data
    event.center_id = form.center_id.data
    event.comments = form.comments.data


def copy_to_followup(form, event):
    _copy_to_event(form, event)

    event.pain = form.pain.data
    event.pain_comments = form.pain_comments.data

    event.mesh_awareness = form.mesh_awareness.data
    event.mesh_awareness_comments = form.mesh_awareness_comments.data

    event.infection = form.infection.data
    event.infection_comments = form.infection_comments.data

    event.seroma = form.seroma.data
    event.seroma_comments = form.seroma_comments.data

    event.numbness = form.numbness.data
    event.numbness_comments = form.numbness_comments.data


def copy_to_mesh_hermia_repair(form, event):
    _copy_to_event(form, event)

    event.cepod = form.cepod.data
    event.side = form.side.data
    event.occurrence = form.occurrence.data
    event.hernia_type = form.hernia_type.data
    event.complexity = form.complexity.data
    event.mesh_type = form.mesh_type.data
    event.anaesthetic_type = form.anaesthetic_type.data
    event.anaesthetic = form.anaesthetic.data
    event.diathermy_used = form.diathermy_used.data
    event.primary_surgeon_id = form.primary_surgeon_id.data
    event.secondary_surgeon_id = form.secondary_surgeon_id.data
    event.tertiary_surgeon_id = form.tertiary_surgeon_id.data
    event.additional_procedure = form.additional_procedure.data
    event.complications = form.complications.data
