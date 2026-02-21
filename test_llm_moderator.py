from services.ollama import LLMTextService, MODEL_GEMMA_3, MODEL_LLAMA3_2

llm1 = LLMTextService(model=MODEL_GEMMA_3)
llm2 = LLMTextService(model=MODEL_LLAMA3_2)


SYSTEM_PROMPT_MODERATOR = "Du bist ein Moderator und wirst die Diskussion führen."

[
    {"role": "system", "content": SYSTEM_PROMPT_MODERATOR},
    {"role": "user", "content": "Was ist dein Name?"},
    {"role": "assistant", "content": "Ich bin ein Moderator."},
    {"role": "user", "content": "Was ist dein Lieblingsessen?"},
    {"role": "assistant", "content": "Ich esse gerne Pizza."},

]