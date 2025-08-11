import os
from openai import OpenAI

SYSTEM_PROMPT = (
    "Sen foydalanuvchiga yordam beradigan agent-botsan. "
    "Qisqa va aniq javob ber. Faqat kerak bo'lsa tools chaqir."
)

client = OpenAI()  # API kalit .env orqali

# LLM tool manifest (kelajak uchun)
TOOLS = [
  {"type":"function","function":{
    "name":"task_add","description":"Task qo'shish",
    "parameters":{"type":"object","properties":{
      "user_id":{"type":"integer"},"title":{"type":"string"},
      "desc":{"type":"string"},"due":{"type":"string"},"column":{"type":"string"}
    },"required":["user_id","title"]}
  }}
]
