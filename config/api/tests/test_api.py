from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from ..models import Wallet, Transaction
from ..serializers import WalletSerializer, TransactionSerializer


class WalletTransactionAPITestCase(APITestCase):
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

    def test_api_get_all_wallets(self):
        url_list = reverse('wallet-list')
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.get(url_list)
        force_authenticate(request=response, user=self.owner_1)
        serializer_data = WalletSerializer([self.wallet_1, self.wallet_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data['results'])

    def test_api_get_all_transactions(self):
        url_list = reverse('transaction-list')
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.get(url_list)
        serializer_data = TransactionSerializer([self.transaction_1, self.transaction_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data['results'])

