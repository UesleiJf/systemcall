from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet
from .models import RegisterCall
from .serializer import RegisterCallSerializer


class RegisterCallViewSet(ModelViewSet):

    serializer_class = RegisterCallSerializer

    # choose querystring altomatic
    # pip install django-filter, add in settings too
    filter_backends = (SearchFilter,)
    # for fk pass "nameClassForegn.field"
    search_fields = ('type_call', 'source_call', 'destination_call')

    # login required to authenticate
    # USER THIS PERMISSION
    # permission_classes = (IsAuthenticated,)
    # OR THE NEXT
    permission_classes = (DjangoModelPermissions,)
    authentication_classes = (TokenAuthentication,)

    # look for registers for source_call - MUST BE UNIQUE!!!!
    # lookup_field = 'source_call'

    # choose querystring manualy
    def get_queryset(self):
        queryset = RegisterCall.objects.all()
        # in Debug = data into queryparams
        id = self.request.query_params.get('id', None)
        type_call = self.request.query_params.get('type_call', None)
        source_call = self.request.query_params.get('source_call', None)

        if id:
            queryset = RegisterCall.objects.filter(pk=id)
        if type_call:
            queryset = queryset.filter(type_call=type_call)
        if source_call:
            queryset = queryset.filter(source_call=source_call)

        return queryset
