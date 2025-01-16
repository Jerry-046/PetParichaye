from django.db import models
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from io import BytesIO
from accounts.models import CustomUser

class Pet(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to="profile_pics/pets/", blank=True, null=True)
    medical_reports = models.ManyToManyField('MedicalReport', blank=True, related_name='pets')
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def __str__(self):
        return self.name

# Post-save signal to generate QR code after a pet is saved
@receiver(post_save, sender=Pet)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        # Generate QR code when pet is created
        qr_url = f"http://192.168.1.100:8000/api/pets/{instance.id}/profile/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)  # Add the profile URL to the QR code
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a BytesIO object
        qr_code_io = BytesIO()
        img.save(qr_code_io, format='PNG')
        qr_code_io.seek(0)

        # Save the QR code image to the model
        instance.qr_code.save(f"qr_code_{instance.id}.png", File(qr_code_io), save=True)


class MedicalReport(models.Model):
    pet = models.ForeignKey(Pet, related_name="reports", on_delete=models.CASCADE)
    report_image = models.ImageField(upload_to="medical_reports/")
    description = models.TextField()

    def __str__(self):
        return f"Medical Report for {self.pet.name}"
