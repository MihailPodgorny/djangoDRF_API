from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    """
    Описание модели Кошелек.
    """
    name = models.CharField(max_length=255, verbose_name="Наименование")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets',
                              default=User.username,
                              verbose_name="Владелец кошелька")
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                  verbose_name="Баланс кошелька, ₽")

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'

    def __str__(self):
        return f"Кошелек: {self.name}"


class Transaction(models.Model):
    """
    Описание модели Транзакция.
    """
    OPERATION = (
        ('+', 'Income'),
        ('-', 'Outcome'),
    )

    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='transactions',
                               verbose_name="Кошелек")
    operation = models.CharField(max_length=1, choices=OPERATION, blank=False, null=False,
                                 verbose_name="Тип операции")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Время транзакции")
    value = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Сумма транзакции, ₽")
    comment = models.CharField(max_length=255, verbose_name="Комментарий пользователя")

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f"Транзакция №{self.pk}"

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        self._update_wallet(created)

    def delete(self, *args, **kwargs):
        self._update_wallet(deleted=True)
        super().save(*args, **kwargs)

    def _update_wallet(self, created=False, deleted=False):
        if created:
            if self.operation == '+':
                self._increase_balance()
            elif self.operation == '-':
                self._decrease_balance()
        if deleted:
            if self.operation == '+':
                self._decrease_balance()
            elif self.operation == '-':
                self._increase_balance()

    def _increase_balance(self):
        self.wallet.balance += self.value
        self.wallet.save()

    def _decrease_balance(self):
        self.wallet.balance -= self.value
        self.wallet.save()
