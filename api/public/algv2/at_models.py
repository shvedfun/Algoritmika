from pyairtable.orm import Model, fields as F

from api.db_airtable import db_airtable

class Booking(Model):
    # id = F.AutoNumberField('id')
    student = F.TextField("student", )
    student_age = F.TextField("student_age")
    school = F.TextField("school")
    group = F.TextField("group")
    accept_navigator = F.CheckboxField("accept_navigator")

    class Meta:
        base_id = "appgTUeSCrX1UELjs"
        table_name = "Booking"
        table_id = "tblQfKMFIDCBI6pKQ"
        api_key = db_airtable.api_key

