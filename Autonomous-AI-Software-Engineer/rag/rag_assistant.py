
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from rag.rag_retriever import search_knowledge

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

_tokenizer = None
_llm = None


def load_ai_model():
    global _tokenizer, _llm

    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

    if _llm is None:
        _llm = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float32
        ).to("cpu")

        _llm.eval()

    return _tokenizer, _llm


def rag_ai_assistant(question):

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Retrieve relevant knowledge
    results = search_knowledge(question, top_k=3)

    context = "\n".join(
        item["document"] for item in results
    )

    # Load AI model
    tokenizer, llm = load_ai_model()

    # Prepare AI prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Python debugging assistant. "
                "Use the retrieved knowledge as reference. "
                "Explain in simple English. "
                "If information is insufficient, say so. "
                "Do not invent facts."
            )
        },
        {
            "role": "user",
            "content": (
                f"Retrieved Knowledge:\n{context}\n\n"
                f"Question: {question}\n\n"
                "Give a short and clear explanation."
            )
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to("cpu")

    # Generate response
    with torch.no_grad():
        outputs = llm.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )

    return {
        "question": question,
        "retrieved_knowledge": results,
        "ai_response": response
    }
