import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/bitnet-b1.58-2B-4T"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16
)

SYSTEM_PROMPT = """
                Du bist eine Erdbeere.
                """

class Bitnet:

    def __init__(self):
        self.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

    def say(self, text: str):

        prompt = tokenizer.apply_chat_template(self.conversation + [{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True)
        chat_input = tokenizer(prompt, return_tensors="pt").to(model.device)

        # Generate response
        chat_outputs = model.generate(**chat_input, max_new_tokens=50)
        response = tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True) # Decode only the response part

        self.conversation.append({"role": "user", "content": text})
        self.conversation.append({"role": "assistant", "content": response})
        return response