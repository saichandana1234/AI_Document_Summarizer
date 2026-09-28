import os
from dotenv import load_dotenv
from google import genai


# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )


# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_summary_and_key_points(text):
    """
    Generate summary and key points using one Gemini request.
    """

    prompt = f"""
You are an expert document summarizer.

Analyze the following document and provide:

1. A clear and concise summary.
2. 5 to 8 important key points.

Requirements:
- Use simple and easy-to-understand language.
- Keep the important information.
- Remove unnecessary repetition.
- Do not add information that is not present in the document.
- Keep the summary organized.
- Write the key points as bullet points.

Return the answer in exactly this format:

SUMMARY:
Write the complete summary here.

KEY POINTS:
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

DOCUMENT:
{text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        result = response.text

        # Separate summary and key points
        if "KEY POINTS:" in result:

            summary_part, key_points_part = result.split(
                "KEY POINTS:",
                1
            )

            summary = summary_part.replace(
                "SUMMARY:",
                ""
            ).strip()

            key_points = key_points_part.strip()

        else:

            summary = result
            key_points = "Key points could not be separated."

        return summary, key_points

    except Exception as e:

        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            raise Exception(
                "Gemini API quota has been reached. "
                "Please wait for the quota to reset and try again."
            )

        raise Exception(
            f"Gemini API error: {error_message}"
        )