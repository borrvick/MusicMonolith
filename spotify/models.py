from django.db import models
from users.models import Profile


# model to store last 5 searches in user account
class CSVFile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(default="Default", max_length=50)
    csv = models.FileField(default="default.csv", upload_to="spotify_csv")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username}{self.csv.name}"

    # deletes the file in media folder
    def delete(self, *args, **kwargs):
        self.csv.delete()
        super().delete(*args, **kwargs)
