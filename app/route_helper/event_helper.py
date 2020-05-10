import importlib

from app.forms import FollowupForm, InguinalMeshHerniaRepairForm
from app.models import Patient, Center, MeshType, User, Event, InguinalMeshHerniaRepair, Followup
from app.route_helper.choices import id_choices


def find_helper(event):
    if isinstance(event, str):
        name = event
    else:
        name = type(event).__name__

    if name == 'Followup':
        return FollowupEventHelper()
    elif name == 'InguinalMeshHerniaRepair':
        return InguinalMeshHerniaRepairEventHelper()
    else:
        return ValueError('Unable to find an event helper for {}.'.format(name))


class EventHelper:
    def populate_choices(self, session, form):
        form.patient_id.choices = id_choices(session, Patient, include_empty=False)
        form.center_id.choices = id_choices(session, Center, include_empty=False)

    def copy_to_event(self, form, event):
        event.type = form.type.data
        event.date = form.date.data
        event.patient_id = form.patient_id.data
        event.center_id = form.center_id.data
        event.comments = form.comments.data

    def template(self):
        return _format_name(self.name(), '_').lower() + '.html'

    def template_inline(self):
        return _format_name(self.name(), '_').lower() + '_inline.html'

    def title(self):
        return _format_name(self.name(), ' ')

    def name(self):
        return self.clazz().__name__

    def event(self):
        return self.clazz()()

    def clazz(self):
        raise NotImplementedError()

    def form(self, event):
        raise NotImplementedError()


class FollowupEventHelper(EventHelper):
    def clazz(self):
        return Followup

    def form(self, event):
        return FollowupForm(obj=event)

    def populate_choices(self, session, form):
        super().populate_choices(session, form)
        form.attendee_id.choices = id_choices(session, User, include_empty=False)

    def copy_to_event(self, form, event):
        super().copy_to_event(form, event)
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


class InguinalMeshHerniaRepairEventHelper(EventHelper):
    def clazz(self):
        return InguinalMeshHerniaRepair

    def form(self, event):
        return InguinalMeshHerniaRepairForm(obj=event)

    def populate_choices(self, session, form):
        super().populate_choices(session, form)
        form.mesh_type.choices = id_choices(session, MeshType, include_empty=False)
        form.primary_surgeon_id.choices = id_choices(session, User, include_empty=True)
        form.secondary_surgeon_id.choices = id_choices(session, User, include_empty=True)
        form.tertiary_surgeon_id.choices = id_choices(session, User, include_empty=True)

    def copy_to_event(self, form, event):
        super().copy_to_event(form, event)
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


def _format_name(name, space_char):
    nice_name = ''
    for (i, c) in enumerate(name):
        if i > 0 and c.isupper():
            nice_name += space_char

        nice_name += c

    return nice_name
