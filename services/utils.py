import base64
import io
import os
from collections import Counter

import gspread
import matplotlib
from django.conf import settings
from django.core.exceptions import ValidationError

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.utils.html import format_html
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from google.oauth2.service_account import Credentials


def validate_file_type_and_size(value):
    """
    Validates the file type and size of uploaded files.

    Allowed types: PDF, Word, Excel
    Maximum size: 5MB
    """
    allowed_extensions = ['.pdf', '.mp4', '.mov', '.avi', '.mkv', '.flv', '.ppt', '.pptx']
    max_file_size = 50 * 1024 * 1024  # 50 MB

    # Get file extension
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed types are: {', '.join(allowed_extensions)}")

    # Check file size
    if value.size > max_file_size:
        raise ValidationError(f"The file size exceeds the 50MB limit.")


def calculate_percent(customer, category_id: int):
    from .models import HonestyTest, HonestyTestResult

    all_tests = HonestyTest.objects.filter(category_id=category_id).count()
    true_tests = HonestyTestResult.objects.filter(test__category_id=category_id, customer_id=customer.id,
                                                  result=True).count()
    return (true_tests / all_tests) * 100 or 0


def get_google_sheet_statistics(sheets_id):
    base_dir = os.path.dirname(__file__)
    os.makedirs(os.path.join(base_dir, 'google_access_json'), exist_ok=True)
    if not os.listdir(f'{base_dir}/google_access_json'):
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Google Sheet access json folder not found.')

    SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(
        filename=f"{base_dir}/google_access_json/{settings.GOOGLE_ACCESS_JSON_NAME}", scopes=SCOPE)
    client = gspread.authorize(creds)
    rows = client.open_by_key(sheets_id).sheet1.get_all_values()

    if not rows:
        raise CustomApiException(error_code=ErrorCodes.NOT_FOUND, message='Data not found')

    header, *data = rows
    total_entries = len(data)

    def process_question(i):
        answers_count = Counter(
            map(lambda row: row[i].strip(), filter(lambda r: len(r) > i and r[i].strip(), data))
        )
        return header[i], answers_count

    question_stats = dict(map(process_question, range(1, len(header))))

    def format_answer(count_list, ingredients):
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        wedges, texts, autotexts = ax.pie(
            count_list, autopct=lambda pct: f"{pct:.1f}%",
            textprops=dict(color="w"), startangle=90)

        ax.legend(wedges, ingredients,
                  title="",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        plt.subplots_adjust(left=0.05, right=0.85)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()

        return f'<img src="data:image/png;base64,{image_base64}" />'

    def format_question(question_data):
        question, answers = question_data
        answers_count = []
        answers_text = []
        for answer, count in answers.items():
            answers_text.append(f'{answer} ({count} ta)')
            answers_count.append(count)
        answers_html = format_answer(answers_count, answers_text)
        return f"<li><strong>{question}:</strong><br><br><ul>{answers_html}</ul></li>"

    question_html = "".join(map(format_question, question_stats.items()))

    content = format_html(
        """
        <h2>Results / Результаты / Natijalar </h2>
        <p><strong>Total Entries / Общее количество участников / Umumiy qatnashganlar soni:</strong> {}</p>
        <h3>Question-wise Answer Results / Результаты ответов по вопросам / Savollar bo'yicha javoblar natijalari</h3>
        <ul>{}</ul>
        """,
        total_entries,
        format_html(question_html),
    )

    return content
