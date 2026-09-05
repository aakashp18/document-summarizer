import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
You are a professional document summarization assistant.

Analyze the provided content carefully and create a clear,
accurate, concise, and professional summary.

RULES:

1. Keep all important information.

2. Do not add, guess, or invent information that is not
present in the provided content.

3. Remove unnecessary repetition and unimportant details.

4. Preserve important names, dates, numbers, locations,
deadlines, registration numbers, contact information,
and other factual details accurately.

5. Organize the information clearly.

6. If the content contains different categories of information,
use simple uppercase section headings when relevant.

Examples:

PERSONAL DETAILS

REGISTRATION DETAILS

IMPORTANT DATES

CONTACT INFORMATION

7. Do not use Markdown formatting or symbols such as:
**, ##, ###, *, -, #, or ---.

8. Do not start with unnecessary sentences such as:

"Here is a summary..."
"The document contains..."
"The image shows..."
"Based on the provided document..."

9. Do not add an unnecessary conclusion.

10. Return only the final formatted summary.
"""


# ======================================================
# SUMMARIZE TEXT
# ======================================================

def summarize_text(text):

    # Validate text
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")


    # Create prompt
    prompt = f"""
{SUMMARY_INSTRUCTIONS}

CONTENT TO SUMMARIZE:

{text}
"""


    # Generate summary
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            automatic_function_calling=(
                types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )
    )


    # Return clean summary
    return response.text.strip()