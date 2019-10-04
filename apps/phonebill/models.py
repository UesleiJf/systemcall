from django.db import models


class PhoneBill(models.Model):
    """PhoneBill Model

    The Phone Account is generated through two fields: ``source_call`` which is
    the number chosen for the account and ``period`` (optional), if the period
    is not informed, the account comes with the last month closed

    Attributes:
        **period (str):** The period to generate the account (mm / YYYY)

        **source_call (str):** The number you chose to generate the account
    """

    period = models.CharField(max_length=7, blank=True, null=True)
    source_call = models.CharField(max_length=11)

    def __str__(self):
        return "Source Call: {} | Period: {}".format(self.source_call, self.period)


class Registers(models.Model):
    """Registers Model

    Through the account number a list is created with all the call records of the chosen period.

    Attributes:
        **phone_bill (fk):** Foreign key of phone bill

        **destination_call (str):** Call destination number

        **duration_call (str):** Duration of the call

        **price_call (str):** Price of the call
        (Calculated by a fixed rate and the duration of the call in minutes)

        **start_date_call (date):** Call record date

        **start_date_call (dateTime):** Call record start time
    """

    phone_bill = models.ForeignKey(PhoneBill, related_name='bill', on_delete=models.PROTECT)
    destination_call = models.CharField(max_length=11)
    duration_call = models.CharField(max_length=11)
    price_call = models.CharField(max_length=11)
    start_date_call = models.DateField(max_length=11)
    start_time_call = models.TimeField()

    class Meta:
        ordering = ['phone_bill']

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields():
            field_values.append(str(field.name) + ": " + str(getattr(self, field.name, '')))
        return ' | '.join(field_values)

    def phone_origin(self):
        return self.phone_bill.source_call

    def period_call(self):
        return self.phone_bill.period
