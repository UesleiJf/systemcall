from rest_framework.serializers import ModelSerializer
from .models import RegisterCall


class RegisterCallSerializer(ModelSerializer):
    class Meta:
        model = RegisterCall
        fields = ('id', 'type_call', 'timestamp_call', 'id_call', 'source_call',
                  'destination_call')
