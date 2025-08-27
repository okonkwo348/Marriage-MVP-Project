from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.lesson.title} - {self.question}"

    @property
    def options_list(self):
        return [self.option1, self.option2, self.option3, self.option4]

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.completed else 'Pending'}"

class MentorshipBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.mentor} on {self.date}"

class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class HomePageContent(models.Model):
    hero_image = models.ImageField(upload_to='home_images/', blank=True, null=True)
    welcome_title = models.CharField(max_length=200, default='Welcome to Eden Marriage')
    welcome_subtitle = models.TextField(default='Discover the biblical blueprint for a fulfilling marriage.')

    def __str__(self):
        return "Homepage Content"