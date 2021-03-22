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
        self.wallet_4 = Wallet.objects.create(name='Fourth wallet',
                                              owner=self.owner_2,
                                              balance=40.50)
        self.transaction_1 = Transaction.objects.create(wallet=self.wallet_1,
                                                        operation='+',
                                                        value=100,
                                                        comment='This is Transaction')
        self.transaction_2 = Transaction.objects.create(wallet=self.wallet_1,
                                                        operation='-',
                                                        value=50,
                                                        comment='Minus 50')
        self.transaction_4 = Transaction.objects.create(wallet=self.wallet_4,
                                                        operation='+',
                                                        value=10,
                                                        comment='Plus 10')
        self.transaction_5 = Transaction.objects.create(wallet=self.wallet_4,
                                                        operation='+',
                                                        value=10,
                                                        comment='Plus 10')

    def test_api_get_wallets(self):
        url_list = reverse('wallet-list')
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = WalletSerializer([self.wallet_1, self.wallet_2, self.wallet_4], many=True).data
        self.assertEqual(serializer_data, response.data['results'])

    def test_api_get_transactions(self):
        url_list = reverse('transaction-list')
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = TransactionSerializer([self.transaction_1,
                                                 self.transaction_2,
                                                 self.transaction_4,
                                                 self.transaction_5], many=True).data
        self.assertEqual(serializer_data, response.data['results'])

    def test_api_get_transactions_filter_by_wallet(self):
        url_list = reverse('transaction-list')
        self.client.force_authenticate(user=self.owner_2)
        response = self.client.get(url_list, data={'wallet': self.wallet_4.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = TransactionSerializer([self.transaction_4, self.transaction_5], many=True).data
        self.assertEqual(response.data['results'], serializer_data)

    def test_api_get_wallet(self):
        url_detail = reverse('wallet-detail', kwargs={'pk': self.wallet_1.pk})
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = WalletSerializer(self.wallet_1).data
        self.assertEqual(serializer_data, response.data)

    def test_api_get_transaction(self):
        url_detail = reverse('transaction-detail', kwargs={'pk': self.transaction_1.pk})
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = TransactionSerializer(self.transaction_1).data
        self.assertEqual(serializer_data, response.data)

    def test_api_create_wallet(self):
        new_wallet = {'name': 'New test wallet',
                      'owner': self.owner_1.pk,
                      'balance': '999.00'}
        url_list = reverse('wallet-list')
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.post(url_list, new_wallet)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.wallet_3 = Wallet.objects.get(pk=response.data['id'])
        serializer_data = WalletSerializer(self.wallet_3).data
        self.assertEqual(serializer_data, response.data)

    def test_api_create_transaction(self):
        new_transaction = {'wallet': self.wallet_1.pk,
                           'operation': '+',
                           'value': '1',
                           'comment': 'test test'}
        url_list = reverse('transaction-list')
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.post(url_list, new_transaction)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.transaction_3 = Transaction.objects.get(pk=response.data['id'])
        serializer_data = TransactionSerializer(self.transaction_3).data
        self.assertEqual(serializer_data, response.data)
        url_detail = reverse('wallet-detail', kwargs={'pk': self.wallet_1.pk})
        response = self.client.get(url_detail)
        self.assertEqual(response.data['balance'], '1051.00')

    def test_api_update_wallet(self):
        url_detail = reverse('wallet-detail', kwargs={'pk': self.wallet_1.pk})
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.put(url_detail, {'name': 'Changed wallet',
                                                'owner': self.owner_1.pk,
                                                'balance': '777.00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url_detail, kwargs={'pk': self.wallet_1.pk})
        self.assertNotEqual(response.data['balance'], '777.00')

    def test_api_update_transaction(self):
        url_detail = reverse('transaction-detail', kwargs={'pk': self.transaction_1.pk})
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.put(url_detail)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_delete_wallet(self):
        self.test_api_create_wallet()
        url_detail = reverse('wallet-detail', kwargs={'pk': self.wallet_3.pk})
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_delete_transaction(self):
        self.test_api_create_transaction()
        url_detail = reverse('transaction-detail', kwargs={'pk': self.transaction_3.pk})
        self.client.force_authenticate(user=self.owner_1)
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url_detail = reverse('wallet-detail', kwargs={'pk': self.wallet_1.pk})
        response = self.client.get(url_detail)
        self.assertEqual(response.data['balance'], '1050.00')

