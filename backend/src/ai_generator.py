import os
import json
import torch
from openai import OpenAI
from transformers import AutoProcessor, Llama4ForConditionalGeneration
from typing import Dict, Any

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the processor and model for Llama-4
model_id = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
processor = AutoProcessor.from_pretrained(model_id)

device = "mps" if torch.backends.mps.is_available() else "cpu"
model = Llama4ForConditionalGeneration.from_pretrained(
    model_id,
    attn_implementation="flex_attention",
    device_map=None,  # Don't use "auto" on Mac, set device manually
    torch_dtype=torch.float16,  # bfloat16 is not supported on MPS, use float16
)
model.to(device)

def generate_challenge(
    difficulty: str) -> Dict[str, Any]:
    """
    Generate a coding challenge based on the specified difficulty level.
    """
    system_prompt = (
        "You are an expert coding challenge creator. "
        "Your task is to generate a coding question with multiple choice answers. "
        "The question should be appropriate for the specified difficulty level.\n\n"
        "For easy questions: Focus on basic syntax, simple operations, or common programming concepts.\n"
        "For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.\n"
        "For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.\n\n"
        "Return the challenge in the following JSON structure:\n"
        "{\n"
        '  "title": "The question title",\n'
        '  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],\n'
        '  "correct_answer_id": 0, // Index of the correct answer (0-3)\n'
        '  "explanation": "Detailed explanation of why the correct answer is right"\n'
        "}\n\n"
        "Make sure the options are plausible but with only one clearly correct answer."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
    ]

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
    )

    response = processor.batch_decode(outputs[:, inputs["input_ids"].shape[-1]:])[0]

    # Try to extract JSON from the response
    try:
        # Find the first and last curly braces to extract JSON
        start = response.find("{")
        end = response.rfind("}") + 1
        challenge_json = response[start:end]
        challenge_data = json.loads(challenge_json)

        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data
    except Exception as e:
        print("Failed to parse model response:", e)
        print("Raw response:", response)
        return {
            "title": "Basic Python List Operation",
            "options": [
                "my_list.append(5)",
                "my_list.add(5)",
                "my_list.push(5)",
                "my_list.insert(5)",
            ],
            "correct_answer_id": 0,
            "explanation": "In Python, append() is the correct method to add an element to the end of a list."
        }