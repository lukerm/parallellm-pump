from src.utils.providers.anthropic import prompt_anthropic
from src.utils.providers.google import prompt_google
from src.utils.providers.openai import prompt_openai

PROMPT_FUNCTION_MAP = {
    "openai": prompt_openai,
    "anthropic": prompt_anthropic,
    "google": prompt_google,
}
