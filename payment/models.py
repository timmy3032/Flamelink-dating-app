from django.db import models
from django.conf import settings

class Coupon(models.Model):

    code = models.CharField(max_length=20, unique=True)
    value = models.IntegerField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class UserCoupon(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)