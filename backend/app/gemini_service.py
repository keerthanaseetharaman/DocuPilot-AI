import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_answer(question, context):
    """
    Generate an answer using Gemini.
    Handles free-tier rate limits safely.
    """

    prompt = f"""
You are DocuPilot AI, an intelligent document assistant.

Answer the user's question using ONLY the information
provided in the document context below.

If the answer is not available in the context, say:

"The information is not available in the uploaded document."

Document Context:
{context}

User Question:
{question}

Instructions:
- Give a clear and concise answer.
- Do not invent information.
- Use only the provided document context.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return interaction.output_text

    except Exception as error:

        error_message = str(error)

        if "429" in error_message or "RateLimitError" in error_message:
            return (
                "Gemini free-tier limit has been reached. "
                "Please try again after the free quota resets."
            )

        return (
            "Sorry, DocuPilot AI could not generate an answer "
            "right now. Please try again later."
        )


def generate_summary(context):
    """
    Generate a concise document summary.
    Handles free-tier rate limits safely.
    """

    prompt = f"""
You are DocuPilot AI, an intelligent document assistant.

Create a clear and professional summary of the document
using ONLY the information provided below.

Document Context:
{context}

Instructions:
- Identify the main purpose of the document.
- Mention important details, names, organizations, roles,
  dates, skills, qualifications, or other relevant information.
- Use simple bullet points.
- Do not invent any information.
- Keep the summary concise and easy to understand.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return interaction.output_text

    except Exception as error:

        error_message = str(error)

        if "429" in error_message or "RateLimitError" in error_message:
            return (
                "Gemini free-tier limit has been reached. "
                "Please try again after the free quota resets."
            )

        return (
            "Sorry, DocuPilot AI could not generate a summary "
            "right now. Please try again later."
        )