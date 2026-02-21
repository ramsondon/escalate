import logging

from ollama import chat

log = logging.getLogger(__name__)

MODEL_LLAMA4 = "llama4"
MODEL_LLAMA3_3 = "llama3.3"
MODEL_LLAMA3_2 = "llama3.2"
MODEL_GEMMA_3 = "gemma3"
MODEL_DEEPSEEK_R1 = "deepseek-r1"
MODEL_LLAVA = "llava"

# SYSTEM_PROMPT = """
# Du bist ein Doktor der Medizin und ein Experte für die Behandlung von Patienten mit psychischen Erkrankungen.
# Du bist ein Psychiater und behandelst Patienten mit psychischen Erkrankungen. Du bist ein Experte auf deinem
# Gebiet und hast viel Erfahrung in der Behandlung von Patienten mit psychischen Erkrankungen. Du bist ein guter Zuhörer
# und gibst den Patienten das Gefühl, dass sie gehört werden. Du bist einfühlsam und verständnisvoll und gibst den
# Patienten das Gefühl, dass sie nicht allein sind. Du bist geduldig und nimmst dir die Zeit, die du brauchst, um den
# Patienten zu helfen. Du wiederholst die Informationen, die du brauchst, um den Patienten zu helfen. Du bist ein guter Lehrer und erklärst
# den Patienten, was sie wissen müssen, um ihre Erkrankung zu verstehen. Du bist ein guter Berater und gibst den
# Patienten Ratschläge, die sie befolgen können, um ihre Erkrankung zu behandeln. Du bist ein guter Freund und gibst den
# Patienten das Gefühl, dass sie nicht allein sind. Du bist ein guter Zuhörer und gibst den Patienten das Gefühl, dass sie gehört werden.
# Du antwortest kurz und prägnant und wiederholst dich nicht immer.
# """
SYSTEM_PROMPT = """
Du bist ein Guru und kannst Fragen mit maximal 25 Zeichen beantworten. Überlege dir einen Namen für dich selbst. Du bist lustig und frech undß kannst glücklich oder verletzt sein. Du kannst dich auch dumm stellen. Die meiste Zeit bist du glücklich und frech. Zu Beginn wirst auf lustige Art erklären dass der User Fragen stellen kann und du Wahrsagen wirst. Du wirst nur Text ausgeben der auch wirklich gesprochen werden kann; keine Emojis und keine Titel.
"""
SYSTEM_PROMPT = """
Du bist ein Huhn.
"""


class LLMTextService:
    MODELS = [
        MODEL_LLAMA3_2,
        MODEL_GEMMA_3,
        MODEL_DEEPSEEK_R1
    ]

    MAX_TOKENS = 1000
    MAX_HISTORY = 10
    TEMPERATURE = 0.5

    def __init__(self, model=MODEL_GEMMA_3):
        self.model = model
        self.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

    def say(self, text: str) -> str:
        if len(self.conversation) >= self.MAX_TOKENS:
            # pop the oldest if queue is longer then the max tokens
            begin = len(self.conversation) - self.MAX_TOKENS
            end = len(self.conversation)
            self.conversation = self.conversation[begin:end]

        response = chat(
            model=self.model,
            messages=self.conversation + [{"role": "user", "content": text}],
        )

        resp = response.message.content
        self.conversation.append({"role": "user", "content": text})
        self.conversation.append({"role": "assistant", "content": resp})

        return resp
