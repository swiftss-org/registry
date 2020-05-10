def copy_to_patient(form, patient):
    patient.name = form.name.data
    patient.national_id = form.national_id.data
    patient.birth_year = form.birth_year.data
    patient.center_id = form.center_id.data
    patient.gender = form.gender.data
    patient.phone1 = form.phone.data
    patient.address = form.address.data
