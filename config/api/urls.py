from rest_framework.routers import SimpleRouter

from .views import TransactionViewSet, WalletViewSet


router = SimpleRouter()

router.register(r'wallets', WalletViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = router.urls
