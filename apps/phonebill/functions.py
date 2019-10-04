from babel.numbers import format_currency
from datetime import timedelta, time, date, datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from apps.registercall.choices import CallTypes
from apps.registercall.models import RegisterCall

from .rates import PriceRates


class CallBill:
    """Class responsible for calculating the telephone calls

    Attributes
        **source_call (str):** The telephone number of the subscribe

        **period (str, optional):** The reference period (mm/yyyy).
        If the reference period is not informed the system will consider the last month
    """

    def __init__(self, source_call, period=None):
        self.source_call = source_call
        self.period = period
        self.month, self.year, self.error, self.result = None, None, None, None

    def validate_params(self):
        """Validate the parameters

        Return
            **bool:** True if is valid, False otherwise.
        """
        if not self.source_call:
            return False

        if not self.period:
            self.period = (timezone.now() - relativedelta(months=1))
            self.month, self.year = self.period.month, self.period.year
        else:
            try:
                parts = self.period.split('/')
                self.month, self.year = int(parts[0]), int(parts[1])
            except Exception:
                return False
                raise

            try:
                date(self.year, self.month, 1)
            except Exception:
                return False
                raise

            now = datetime.now()
            if '{}/{}'.format(self.month, self.year) == '{}/{}'.format(now.month, now.year):
                return False
        return True

    @staticmethod
    def _get_price(start, end):
        """Calculate the call price according the start/end arguments

        The are two tarrif times:

        1. Standard time call - between 6h00 and 22h00 (excluding):

            Standing charge: R$ 0,36 (fixed charges used to pay for the cost of the call)

            Call charge/minute: R$ 0,09 (there is no fractioned charge. The charge applies
            to each completed 60 seconds cycle).

        2. Reduced tariff time call - between 22h00 and 6h00 (excluding):

            Standing charge: R$ 0,36 * Call charge/minute: R$ 0,00

        Args:
            **start (datetime):** Call start date/time

            **end (datetime):** Call end date/time

        Return:
            **float:** Call price
        """
        if not (isinstance(start, datetime) or isinstance(end, datetime)):
            return "R$ 0.00"
        minutes = 0
        while start < end:
            start = start + timedelta(minutes=1)
            if start < end and time(6, 0, 0) < start.time() < time(22, 0, 0):
                minutes += 1

        price = (minutes * PriceRates.MINUTE) + PriceRates.FLAT_RATE
        return format_currency(price, 'R$', '¤¤ ###,###,##0.00', locale='pt')

    @staticmethod
    def _get_duration(start, end):
        """Call duration (hour, minute and seconds): e.g. 0h31m00s

        Args:
            **start (datetime):** Call start date/time

            **end (datetime):** Call end date/time

        Return:
            **str:** Call duration (hour, minute, seconds)
        """
        if not (isinstance(start, datetime) or isinstance(end, datetime)):
            return "0h0m0s"
        diff = (end - start).total_seconds()
        minutes, seconds = divmod(diff, 60)
        hours, minutes = divmod(minutes, 60)
        return "{}h{}m{}s".format(int(hours), int(minutes), int(seconds))

    def calculate_bill(self):
        """Calculate the bill for each call in period according the price rules

        Return:
            list: List of call records in the period
            ::

                {
                    'destination_call': The phone number  that received the call
                    'start_date_call': The date of when the event occured
                    'start_time_call': The time of when the event occured
                    'durantion_call': Durantion of the call
                    'price_call': Price of the call
                }
        """
        self.validate_params()

        # First step: get all the phone calls from the subscriber
        subscriber_calls = RegisterCall.objects.filter(
            source_call=self.source_call
        ).values_list('id_call', flat=True)

        # Second step: get all the calls in the period, filtering by type=2 (end)
        calls_in_period = RegisterCall.objects.filter(
            timestamp_call__year=self.year,
            timestamp_call__month=self.month,
            type_call=CallTypes.END,
            id_call__in=subscriber_calls
        ).values_list('id_call', flat=True)

        if not calls_in_period:
            period_not_found = [{
                'error': 'The close of this call corresponds to the following month'
            }]

            return period_not_found

        # Finaly, get the calls that should be priced
        calls = RegisterCall.objects.filter(id_call__in=calls_in_period)\
            .order_by('id_call', 'timestamp_call')

        # Grouping the same call_ids in one registry
        group_call = {}
        for call in calls:
            group_call.setdefault(call.id_call, {})
            if call.destination_call:
                group_call[call.id_call]['destination_call'] = call.destination_call

            if call.type_call == CallTypes.START:
                group_call[call.id_call]['call_start'] = call.timestamp_call
            else:
                group_call[call.id_call]['call_end'] = call.timestamp_call

        # Formating the data, and calculating the price and duration of the calls
        bill_data = []
        for bill in group_call.values():
            start = bill.get('call_start')
            end = bill.get('call_end')
            if not (start or end):
                continue

            bill_data.append({
                'destination_call': bill.get('destination_call'),
                'duration_call': self._get_duration(start, end),
                'price_call': self._get_price(start, end),
                'start_date_call': start.date(),
                'start_time_call': start.time(),
            })

        self.result = bill_data

        return bill_data
