from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default="example@example.com")  # Added default
    phone = models.CharField(max_length=15,default="11111111111")
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Queue(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="queues")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # Allow null

    def generate_qr_code(self):
        """Generates a QR code with the correct Queue ID after saving."""
        if not self.id:  # Prevent generating QR before saving
            return  
        qr_url = f"http://192.168.42.245:8000/join-queue/{self.id}/"

        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        
        self.qr_code.save(f'queue_{self.id}.png', ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        """Ensure Queue ID exists before generating QR."""
        super().save(*args, **kwargs)  # Save first to get an ID
        if not self.qr_code:  # Generate QR after ID is assigned
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])  # Save again with QR


class Ticket(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class QueueParticipant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default="noreply@example.com")
    position = models.PositiveIntegerField()
    queue = models.ForeignKey("Queue", on_delete=models.CASCADE)
    served = models.BooleanField(default=False)  # New field to track served users

    def notify_user_if_needed(self):
        """Send an email if the user's position is less than 5."""
        if self.position < 5 and not self.served:
            send_mail(
                "Your Turn is Near!",
                f"Hello {self.name}, your queue position is now {self.position}. Please be ready!",
                "noreply@queueapp.com",
                [self.email],
                fail_silently=False,
            )

    def mark_as_served(self):
        """Mark participant as served and update queue."""
        self.served = True
        self.save()
        self.update_queue_positions()

    @classmethod
    def update_queue_positions(cls):
        """Recalculate positions after a participant is served."""
        active_participants = cls.objects.filter(served=False).order_by("position")
        for i, participant in enumerate(active_participants):
            participant.position = i + 1
            participant.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.notify_user_if_needed()

@receiver(post_delete, sender=QueueParticipant)
def update_positions_after_delete(sender, instance, **kwargs):
    """ Update queue positions after a user is removed """
    remaining_participants = QueueParticipant.objects.filter(queue=instance.queue).order_by('position')

    for index, participant in enumerate(remaining_participants, start=1):
        participant.position = index
        participant.save(update_fields=['position'])