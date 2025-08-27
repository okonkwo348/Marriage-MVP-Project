from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Lesson, Quiz, Progress, ForumPost, MentorshipBooking, HomePageContent
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings
import json
from openai import OpenAI

#Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@login_required
def generate_quiz_ai(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    try:
        prompt = f"""
        Generate exactly 3 multiple-choice questions based on this lesson content: "{lesson.content}".

        Return ONLY a JSON array with this exact structure:
        [
          {{"question": "question text", "options": ["option1", "option2", "option3", "option4"], "correct_answer": "option1"}},
          {{"question": "question text", "options": ["option1", "option2", "option3", "option4"], "correct_answer": "option2"}},
          {{"question": "question text", "options": ["option1", "option2", "option3", "option4"], "correct_answer": "option3"}}
        ]
        No additional text, explanations, or labels. Ensure questions and options are relevant to the lesson content.
        """
        print("Prompt Sent:", prompt)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use a suitable model (e.g., gpt-4 for better results, if available)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        print("Response:", response)
        raw_text = response.choices[0].message.content.strip()
        print("AI Raw Response:", raw_text)

        if not raw_text:
            raise ValueError("Empty response from OpenAI API")

        try:
            quiz_list = json.loads(raw_text)
            print("Parsed Quiz List:", quiz_list)
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", str(e), "Raw Text:", raw_text)
            lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
            if len(lines) >= 5:
                quiz_list = [{
                    "question": lines[0] if lines else f"Sample question for {lesson.title}",
                    "options": lines[1:5],
                    "correct_answer": lines[1] if len(lines) > 1 else "Option A"
                }]
            else:
                quiz_list = []

        created_count = 0
        for q in quiz_list:
            if (
                isinstance(q, dict)
                and "question" in q
                and "options" in q
                and isinstance(q["options"], list)
                and len(q["options"]) == 4
                and "correct_answer" in q
                and q["correct_answer"] in q["options"]
            ):
                Quiz.objects.create(
                    lesson=lesson,
                    question=q["question"],
                    option1=q["options"][0],
                    option2=q["options"][1],
                    option3=q["options"][2],
                    option4=q["options"][3],
                    correct_option=q["correct_answer"]
                )
                created_count += 1
            else:
                print("Invalid quiz data:", q)

        if created_count > 0:
            messages.success(request, f"{created_count} quizzes generated for {lesson.title}!")
        else:
            raise ValueError("No valid quizzes generated from the response.")

    except Exception as e:
        messages.error(request, f"OpenAI API request failed: {str(e)} — added a sample quiz instead.")
        print("API Error Details:", str(e))
        Quiz.objects.create(
            lesson=lesson,
            question=f"Sample question for {lesson.title} (Fallback due to error: {str(e)[:50]})",
            option1="Option A",
            option2="Option B",
            option3="Option C",
            option4="Option D",
            correct_option="Option A"
        )

    return redirect("lesson_detail", id=lesson_id)

# HOME
# ---------------------------
def home(request):
    lessons = Lesson.objects.all()
    homepage_content = HomePageContent.objects.first()
    return render(request, 'home.html', {
        'lessons': lessons,
        'homepage_content': homepage_content
    })


# ---------------------------
# DASHBOARD
# ---------------------------
@login_required
def dashboard(request):
    lessons = Lesson.objects.all()
    progress_qs = Progress.objects.filter(user=request.user)

    total_lessons = lessons.count()
    total_completed = progress_qs.filter(completed=True).count()
    overall_progress = int((total_completed / total_lessons) * 100) if total_lessons > 0 else 0

    progress_dict = {
        p.lesson.id: {'completed': p.completed, 'score': p.score, 'percentage': p.score}
        for p in progress_qs
    }

    bookings = MentorshipBooking.objects.filter(user=request.user).order_by('-date')

    recommended_lesson = None
    if progress_qs.exists():
        lowest_score = min((p.score for p in progress_qs if p.score is not None), default=100)
        if lowest_score < 70:
            recommended_lesson = Lesson.objects.exclude(
                id__in=progress_qs.filter(completed=True).values_list('lesson_id', flat=True)
            ).first()

    return render(request, 'dashboard.html', {
        'lessons': lessons,
        'progress': progress_dict,
        'recommended_lesson': recommended_lesson,
        'total_lessons': total_lessons,
        'total_completed': total_completed,
        'overall_progress': overall_progress,
        'bookings': bookings,
    })


# ---------------------------
# LESSON DETAIL
# ---------------------------
@login_required
def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    quizzes = lesson.quiz_set.all()
    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'quizzes': quizzes
    })


# ---------------------------
# QUIZ PAGE (multi-question per lesson)
# ---------------------------
@login_required
def quiz_page(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = lesson.quiz_set.all()

    if request.method == 'POST':
        score = 0
        total = quizzes.count()

        for quiz in quizzes:
            user_answer = request.POST.get(f'option_{quiz.id}')
            if user_answer and user_answer == quiz.correct_option:
                score += 1

        percentage = int((score / total) * 100) if total > 0 else 0

        progress, _ = Progress.objects.get_or_create(user=request.user, lesson=lesson)
        progress.score = percentage
        progress.completed = percentage >= 70
        progress.save()

        messages.success(request, f"You scored {percentage}% on {lesson.title}")
        return redirect('dashboard')

    return render(request, 'quiz_page.html', {
        'lesson': lesson,
        'quizzes': quizzes
    })


# ---------------------------
# REGISTER
# ---------------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# ---------------------------
# MENTORSHIP BOOKING
# ---------------------------
@login_required
def mentorship_booking(request):
    mentors = ['Pastor James', 'Mrs. Adaobi', 'Dr. Olakunle']
    if request.method == 'POST':
        mentor = request.POST.get('mentor')
        date_str = request.POST.get('date')
        if mentor and date_str:
            date_obj = timezone.datetime.fromisoformat(date_str)
            MentorshipBooking.objects.create(user=request.user, mentor=mentor, date=date_obj)
        return redirect('dashboard')
    return render(request, 'mentorship_booking.html', {'mentors': mentors})


# ---------------------------
# FORUM
# ---------------------------
@login_required
def forum(request):
    posts = ForumPost.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        ForumPost.objects.create(user=request.user, title=title, content=content)
        return redirect('forum')
    return render(request, 'forum.html', {'posts': posts})


# ---------------------------
# COURSE LIST
# ---------------------------
@login_required
def course(request):
    lessons = Lesson.objects.all()
    return render(request, 'course.html', {'lessons': lessons})


# ---------------------------
# CONTACT & SUPPORT
# ---------------------------
def contact(request):
    return render(request, 'contact.html', {})

def support(request):
    return render(request, 'support.html', {})


# ---------------------------
# ASSESSMENT (shortcut to first lesson quiz)
# ---------------------------
@login_required
def assessment(request):
    first_lesson = Lesson.objects.first()
    if first_lesson:
        return redirect('quiz_page', lesson_id=first_lesson.id)
    return render(request, 'dashboard.html', {
        'error': 'No lessons available for assessment'
    })


# ---------------------------
# PROFILE
# ---------------------------
@login_required
def profile(request):
    return render(request, 'profile.html', {})
