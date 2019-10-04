from rest_framework import serializers
from .models import PhoneBill, Registers


class RegistersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registers
        fields = ('destination_call', 'duration_call', 'price_call',
                  'start_date_call', 'start_time_call', 'phone_bill')


class PhoneBillSerializer(serializers.ModelSerializer):

    bill = serializers.StringRelatedField(many=True)

    class Meta:
        model = PhoneBill
        fields = ('id', 'period', 'source_call', 'bill')
