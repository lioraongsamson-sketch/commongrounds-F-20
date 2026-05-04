from django.urls import reverse
from django.contrib.auth.models import User

USER_ROLES ={
    "Market Seller": "Market Seller",
    "Event Organizer": "Event Organizer",
    "Book Contributor": "Book Contributor",
    "Project Creator": "Project Creator",
    "Commission Maker": "Commission Maker",
}

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email = models.EmailField()
    role = models.CharField(max_length=50, choices=USER_ROLES, blank=True, null=True)

    def __str__(self):
        return self.display_name