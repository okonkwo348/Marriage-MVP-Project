from django.contrib import admin
from .models import Lesson, Quiz, Progress, MentorshipBooking, ForumPost, HomePageContent

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title',)
    list_editable = ('image',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question')
    search_fields = ('question',)
    list_filter = ('lesson',)

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score')
    list_filter = ('completed',)

@admin.register(MentorshipBooking)
class MentorshipBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'mentor', 'date', 'status')
    list_filter = ('status',)

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at',)

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('welcome_title', 'hero_image')