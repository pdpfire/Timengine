from django.db import models

# class DiaryEntry(models.Model):
#     strtime = models.DateTimeField()
#     title = models.CharField(max_length=200)
#     tasktime = models.CharField(max_length=100)
#     taskdetails = models.TextField()
#     detailtime = models.CharField(max_length=100)
#     endtime = models.DateTimeField()

#     class Meta:
#         db_table = 'diaryapp'  # Corrected from table_name to db_table
        
#     def __str__(self):
#         return self.title

class DiaryEntry(models.Model):
    strtime = models.DateTimeField()
    title = models.TextField()
    tasktime = models.TextField()
    taskdetails = models.TextField()
    detailtime = models.TextField()
    endtime = models.DateTimeField()
    goal = models.TextField()

    FEELING_CHOICES = [
        ('fulfilled', 'Fulfilled'),
        ('energized', 'Energized'),
        ('focused', 'Focused'),
        ('neutral', 'Neutral'),
        ('tired', 'Tired'),
        ('stressed', 'Stressed'),
        ('frustrated', 'Frustrated'),
        # Add more feelings as desired
    ]
    feeling = models.CharField(
        max_length=50,
        choices=FEELING_CHOICES,
        default='neutral', # Or can be blank=True, null=True if optional
        help_text="How did you feel during/after this activity?"
    )
    class Meta:
        db_table = 'final_diary'
        app_label = 'diaryapp'

    def __str__(self):
        return f"{self.strtime.strftime('%Y-%m-%d %H:%M')} - {self.title}"

