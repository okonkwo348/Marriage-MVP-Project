# Eden Marriage

Eden Marriage is a web-based platform built with Django to provide interactive lessons and AI-generated quizzes for couples to manage conflict and strengthen their marriage.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/eden-marriage.git
   cd eden_marriage
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     SECRET_KEY=your-secret-key
     DATABASE_URL=sqlite:///db.sqlite3  # Use PostgreSQL URL for production
     ```
   - Get your `GEMINI_API_KEY` from https://ai.google.dev/.

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` to see the app.

7. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

## Key Features
- **Lesson Management**: Create and view lessons on marital topics like conflict management.
- **AI-Generated Quizzes**: Uses Gemini AI to dynamically generate quizzes based on lesson content (requires billing to resolve free tier quota limits).
- **Interactive Interface**: Displays lessons and quizzes in a user-friendly HTML template.
- **Scalable Design**: Easily expandable to include more topics or features.

## Usage Examples
1. **Add a Lesson**:
   - Access the Django admin at `http://127.0.0.1:8000/admin/` (create a superuser with `python manage.py createsuperuser`).
   - Add a new `Lesson` with title "Managing Conflict" and content "Learning self control Learning triggers of conflict".

2. **Generate Quizzes**:
   - Visit `http://127.0.0.1:8000/lesson/1/` (replace `1` with your lesson ID).
   - Click "Generate Quizzes" to create sample quizzes (dynamic quizzes require Gemini API billing).

3. **View Quizzes**:
   - The page will display questions like "What is a key skill for managing marital conflict?" with options ["Self control", "Yelling", "Avoiding", "Blaming"].

## Additional AI-Generated Documentation

### API Documentation
**Endpoint: `/lesson/<int:lesson_id>/generate_quiz_ai/`**
- **Method**: GET
- **Authentication**: Requires login (Django auth)
- **Description**: Generates quizzes for a specific lesson using Gemini AI.
- **Parameters**:
  - `lesson_id` (int): The ID of the lesson to generate quizzes for.
- **Response**:
  - Success: Redirects to `lesson_detail` with newly generated quizzes.
  - Failure: Displays an error message and creates a sample quiz.
- **Example**:
  - Request: `GET /lesson/1/generate_quiz_ai/`
  - Response: Redirect to `/lesson/1/` with quizzes or a fallback message.

### Onboarding Guide
- **Step 1**: Clone the repo and set up the environment as per setup instructions.
- **Step 2**: Configure your Gemini API key to enable dynamic quiz generation.
- **Step 3**: Use the Django admin to add lessons and test the quiz generation feature.
- **Step 4**: Deploy to Vercel (see deployment guide below) for public access.

### Deployment Guide
- **Platform**: Vercel
- **Steps**:
  1. Install Vercel CLI: `npm install -g vercel`.
  2. Log in: `vercel login`.
  3. Deploy: `cd eden_marriage && vercel`, add `GEMINI_API_KEY` and `SECRET_KEY` as environment variables.
  4. Test at the provided Vercel URL.
- **Note**: Enable billing at https://console.cloud.google.com/billing for dynamic quizzes.