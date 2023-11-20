from django.db import models

# Create your models here.
class qrcode(models.Model):
    S_No = models.IntegerField(primary_key=True)
    QR_Id = models.CharField(max_length=50)
    Registration_Status = models.IntegerField(default=0)
    class Meta:
        db_table = 'qrcode'