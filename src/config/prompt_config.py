from src.utils.providers.alibaba import prompt_alibaba
from src.utils.providers.anthropic import prompt_anthropic
from src.utils.providers.deepseek import prompt_deepseek
from src.utils.providers.google import prompt_google
from src.utils.providers.openai import prompt_openai

PROMPT_FUNCTION_MAP = {
    "alibaba": prompt_alibaba,
    "anthropic": prompt_anthropic,
    "deepseek": prompt_deepseek,
    "google": prompt_google,
    "openai": prompt_openai,
}
