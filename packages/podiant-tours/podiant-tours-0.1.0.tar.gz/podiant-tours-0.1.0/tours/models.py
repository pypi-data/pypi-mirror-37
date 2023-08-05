from django.db import models
import json


class TourData(models.Model):
    user = models.OneToOneField(
        'auth.User',
        related_name='viewed_tours',
        unique=True,
        on_delete=models.CASCADE
    )

    data = models.TextField(default='{}')

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_data(self):
        return json.loads(self.data)

    def set_data(self, data, commit=False):
        self.data = json.dumps(data)

        if commit:
            self.save()

    class Meta:
        db_table = 'tour_userdata'
