from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.db import models

from .choices import CallTypes


class RegisterCall(models.Model):
    """RegisterCall Model

    There are two call detailed record types: Call Start Record and Call End Record.
    To get all information of a telephone call you should use the records pair.

    If is a Start Call, ``source_call`` and ``destination_call`` fields are ``required``,
    otherwise, can be ``null``

    A pair off c

    Attributes:
        **type_call (int):** Indicate if it's a call start or end record (1: start, 2: end)

        **timestamp_call (datetime):** The timestamp of when the event occured;

        **id_call (str):** Unique for each call record pair

        **source_call (str):** The subscriber phone number that originated the call

        **destination_call (str):** The phone number receiving the call
    """

    type_call = models.PositiveSmallIntegerField(choices=CallTypes.CHOICES)
    timestamp_call = models.DateTimeField()
    id_call = models.PositiveIntegerField()
    source_call = models.CharField(max_length=11, null=True, blank=True)
    destination_call = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        verbose_name = 'Register Call'
        verbose_name_plural = 'Register Calls'
        unique_together = (('type_call', 'timestamp_call', 'id_call', 'source_call',
                            'destination_call'),
                           ('type_call', 'id_call'),
                           ('type_call', 'timestamp_call'))

    def __str__(self):
        return str(self.source_call)

    def clean(self, *args, **kwargs):
        """Hook for doing any extra model-wide validation after clean() has been
        called on every field by self.clean_fields. Any ValidationError raised
        by this method will not be associated with a particular field; it will
        have a special-case association with the field defined by NON_FIELD_ERRORS.
        """
        super(RegisterCall, self).clean(*args, **kwargs)
        error = {}

        if self.type_call == CallTypes.START and not (self.source_call or self.destination_call):
            error.update({
                "source_call": ["This field is required."],
                "destination_call": ["This field is required."],
            })

        if not self.id_call:
            error.update({
                "id_call": ["This field is required."]
            })
        elif self.type_call == CallTypes.END:
            self.source_call = self.destination_call = None
            try:
                start_call = RegisterCall.objects.get(id_call=self.id_call)
                if self.timestamp_call < start_call.timestamp_call:
                    error.update({
                        "timestamp_call": ["Invalid timestamp_call. Must be grater then {}"
                                           .format(start_call.timestamp_call)]
                    })
            except RegisterCall.DoesNotExist:
                error.update({
                    "id_call": ["Does not exist a call start entry with this call id: {}"
                                .format(self.id_call)]
                })
            except MultipleObjectsReturned:
                error.update({
                    "id_call": ["Already exists a type END for this id_call: {}"
                                .format(self.id_call)]
                })

        if error:
            raise ValidationError(error)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(RegisterCall, self).save(*args, **kwargs)
