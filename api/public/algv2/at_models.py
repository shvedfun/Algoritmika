from pyairtable.orm import Model, fields as F

from api.db_airtable import db_airtable

class Booking(Model):
    id = F.AutoNumberField('id')
    student = F.TextField("Имя", )
    student_age = F.TextField("Возраст")
    school = F.TextField("Школа")
    group = F.TextField("Группа")
    accept_navigator = F.CheckboxField("Согласовано Навигатором")

    class Meta:
        base_id = "appgTUeSCrX1UELjs"
        table_name = "Booking"
        table_id = "tblQfKMFIDCBI6pKQ"
        api_key = db_airtable.api_key

