import os
import time

from google import genai
from google.genai import types
from dotenv import load_dotenv


# ======================================================
# LOAD ENVIRONMENT VARIABLES
# ======================================================

load_dotenv()


# ======================================================
# GEMINI API
# ======================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")


client = genai.Client(
    api_key=api_key
)


# ======================================================
# COMMON SUMMARY INSTRUCTIONS
# ======================================================

SUMMARY_INSTRUCTIONS = """
You are a professional document and content summarization assistant.

Analyze the provided content carefully and create a clear,
accurate, concise, and professional summary.

RULES:

1. Keep all important information.

2. Do not add, guess, or invent information.

3. Remove unnecessary repetition.

4. Preserve important names, dates, numbers, locations,
deadlines, registration numbers, contact details, and other
important factual information accurately.

5. Organize information clearly.

6. When the content contains different categories of information,
use simple uppercase section headings when relevant.

Examples:

PERSONAL DETAILS

REGISTRATION DETAILS

IMPORTANT DATES

CONTACT INFORMATION

7. Do not use Markdown formatting or symbols such as:
**, ##, ###, *, -, #, or ---.

8. Do not start with phrases such as:

"Here is a summary"
"Here is the summary"
"The image shows"
"This image shows"
"The image contains"
"This image contains"
"Based on the provided image"

9. Do not describe the visual layout, colors, logos, stamps,
QR codes, or appearance unless that information is important
to understanding the content.

10. If the image contains a document, certificate, form,
receipt, letter, notice, ID, or other written content,
summarize the INFORMATION in that document instead of
describing the image.

11. Return only the final formatted summary.
"""


# ======================================================
# SUMMARIZE IMAGE
# ======================================================

def summarize_image(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Image file not found"
        )


    # Upload image to Gemini
    image = client.files.upload(
        file=file_path
    )


    # Create professional summarization prompt
    prompt = f"""
{SUMMARY_INSTRUCTIONS}

Analyze the uploaded image carefully.

If it contains readable text or a document, first understand
the actual information in the content.

For example:

If it is a birth certificate, extract and organize the
important personal and registration details.

If it is an invoice, organize important billing, company,
amount, and date information.

If it is a notice, organize the important announcement,
dates, deadlines, and instructions.

If it is a general image without a document, summarize only
the important information or subject shown.

Return only the final formatted summary.
"""


    # Retry if Gemini temporarily returns 503
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",

                contents=[
                    prompt,
                    image
                ],

                config=types.GenerateContentConfig(
                    automatic_function_calling=(
                        types.AutomaticFunctionCallingConfig(
                            disable=True
                        )
                    )
                )
            )


            return response.text.strip()


        except Exception as e:

            if "503" not in str(e):
                raise e


            if attempt < 2:

                print(
                    "Gemini temporarily unavailable. "
                    f"Retrying ({attempt + 1}/2)..."
                )

                time.sleep(3)

            else:
                raise e