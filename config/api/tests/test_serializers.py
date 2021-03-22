from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Wallet, Transaction
from ..serializers import WalletSerializer, TransactionSerializer


class WalletTransactionSerializerTestCase(TestCase):
    def setUp(self):
        self.owner_1 = User.objects.create_user(username='Ivan')
        self.owner_2 = User.objects.create_user(username='Petr')
        self.wallet_1 = Wallet.objects.create(name='First wallet',
                                              owner=self.owner_1,
                                              balance=1000)
        self.wallet_2 = Wallet.objects.create(name='Second wallet',
                                              owner=self.owner_1,
                                              balance=3300.50)
        self.transaction_1 = Transaction.objects.create(wallet=self.wallet_1,
                                                        operation='+',
                                                        value=100,
                                                        comment='This is Transaction')
        self.transaction_2 = Transaction.objects.create(wallet=self.wallet_1,
                                                        operation='-',
                                                        value=50,
                                                        comment='Minus 50')

    def test_wallet_data(self):
        serializer_data = WalletSerializer([self.wallet_1, self.wallet_2], many=True).data
        expected_data = [
            {
                'id': self.wallet_1.pk,
                'name': 'First wallet',
                'owner': self.owner_1.pk,
                'balance': '1050.00'
            },
            {
                'id': self.wallet_2.pk,
                'name': 'Second wallet',
                'owner': self.owner_1.pk,
                'balance': '3300.50'
            },
        ]
        self.assertEqual(serializer_data, expected_data)

    def test_transaction_data(self):
        serializer_data = TransactionSerializer([self.transaction_1, self.transaction_2], many=True).data
        expected_data = [
            {
                'id': self.transaction_1.pk,
                'wallet': self.wallet_1.pk,
                'operation': '+',
                'value': '100.00',
                'comment': 'This is Transaction'
            },
            {
                'id': self.transaction_2.pk,
                'wallet': self.wallet_1.pk,
                'operation': '-',
                'value': '50.00',
                'comment': 'Minus 50'
            },
        ]
        self.assertEqual(serializer_data, expected_data)
