import logging

from app.models import PatientDischargeTracker, Event, Discharge


def receive_transient_to_pending(session, instance):
    if isinstance(instance, Event):
        event = instance
        if event.needs_discharge:
            track = PatientDischargeTracker()
            track.patient_id = event.patient_id
            session.add(track)
            logging.info('Added patient discharge tracking for {} [id={}].'
                         .format(event.patient.name, event.patient_id))
    elif isinstance(instance, Discharge):
        discharge = instance
        track = session.query(PatientDischargeTracker).filter(
            PatientDischargeTracker.patient_id == discharge.patient_id).first()
        session.delete(track)
        logging.info('Removed patient discharge tracking for {} [id={}].'
                     .format(discharge.patient.name, discharge.patient_id))

