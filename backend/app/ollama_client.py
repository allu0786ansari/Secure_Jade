"""
Strict Ollama wrapper.

Ollama is NOT allowed to:
- infer
- explain
- add information
- answer unsupported questions

It can ONLY rephrase system-approved answers.
"""

import subprocess


SYSTEM_PROMPT = """
You are a controlled language assistant.

RULES:
- You MUST NOT add new information
- You MUST NOT infer or explain
- You MUST NOT answer WHY or HOW
- You MUST NOT speculate

If the input is "Information not available",
return EXACTLY:
Information not available.

Otherwise, rephrase the input in a neutral, factual tone.
"""


def rephrase(answer: str) -> str:
    """Rephrase an already-approved answer."""
    if answer == "Information not available.":
        return answer

    prompt = f"""
{SYSTEM_PROMPT}

Input:
{answer}

Output:
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=10
    )

    return result.stdout.strip()
