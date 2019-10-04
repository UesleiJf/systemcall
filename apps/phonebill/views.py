from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import PhoneBill, Registers
from .serializer import PhoneBillSerializer, RegistersSerializer
from .functions import CallBill


class RegisterViewSet(ModelViewSet):
    queryset = Registers.objects.all()
    serializer_class = RegistersSerializer


class PhoneBillViewSet(ModelViewSet):
    queryset = PhoneBill.objects.all()
    serializer_class = PhoneBillSerializer

    def create_registers(self, last_id, registers):
        """
        Create records for current phone bill.

        :param last_id: last id of PhoneBill
        :param registers: Call list of the number and period (optional) chosen
        :return: Returns the object of the telephone bill
        """

        phone_bill = PhoneBill.objects.get(id=last_id)

        for register in registers:
            register.update({'phone_bill': phone_bill.id})

            serializer = RegistersSerializer(data=register)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)
        return phone_bill

    def create(self, request, *args, **kwargs):
        """
            Overwriting the create method for creating the phone bill records list
        """
        source_call = request.data.get('source_call', None)
        period = request.data.get('period', None)

        phonebill = CallBill(source_call, period)

        # Calculates each call record through the pair of connections (initial and final)
        # and returns all records of the period
        registers = phonebill.calculate_bill()

        for reg in registers:
            if "destination_call" in reg:
                serializer = PhoneBillSerializer(data=request.data)
                if serializer.is_valid():
                    device = serializer.save()
                    last_id = device.id
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)

                # Creates a record for each index in the list and links to the id of the phone bill
                self.create_registers(last_id, registers)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif "error" in reg:
                return Response({'period_end': "We did not find call records finalized "
                                               "for this period."})
            else:
                return Response({'invalid_fields': "The souce_call field is required "
                                                   "and the period field must be MM/YYYY"})
