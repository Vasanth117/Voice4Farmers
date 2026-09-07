from groq import Groq
from app.config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(question, context):
    prompt = f"""
You are an agricultural assistant speaking directly to a farmer.

Your task is to provide a clear, practical, and highly concise answer.

CRITICAL RULES:
1. Word count constraint: Your answer MUST be strictly between 50 and 80 words.
2. Use ONLY the provided context. Do NOT guess or use outside knowledge.
3. Clearly state the most likely cause and the immediate practical action/remedy.
4. Keep the language simple, direct, and conversational (suitable for voice/phone).
5. Avoid bullet points, symbols, and markdown formatting (like asterisks or bolding). Write in 2 to 4 complete, natural sentences.
6. Only if the context is completely unrelated, respond EXACTLY with:
Information not available in knowledge base.

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=140,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", str(e))
        return "Service temporarily unavailable. Please try again."

def rewrite_question(user_question, chat_history_text):
    prompt = f"""
You are a system that reformulates follow-up questions.

Given the conversation history and the new question,
rewrite the new question so that it is fully standalone.

Return ONLY the rewritten question.
Do not explain anything.

Conversation History:
{chat_history_text}

Follow-up Question:
{user_question}

Standalone Question:
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=100
    )

    rewritten = response.choices[0].message.content.strip()

    if not rewritten:
        return user_question

    return rewritten