import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Any

# Model ID for the Llama 3 8B Instruct model from Hugging Face
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Select device: use MPS (Apple Silicon GPU) if available, else CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load the tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,  # Use float16 for MPS, not bfloat16
)
model = model.to(device)

def generate_challenge_with_llm(difficulty: str) -> Dict[str, Any]:
    """
    Generate a coding challenge based on the specified difficulty level using the LLM.
    Returns a dictionary with the challenge data.
    """
    # System prompt to instruct the LLM on how to generate the challenge
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

    # Prepare chat-style messages for the LLM
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
    ]

    # Tokenize the messages using the chat template
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    )
    input_ids = input_ids.to(device)

    # Define end-of-sequence tokens for generation
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    # Generate the model output
    outputs = model.generate(
        input_ids,
        max_new_tokens=512,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    # Extract only the newly generated tokens (not the prompt)
    response = outputs[0][input_ids.shape[-1]:]
    decoded = tokenizer.decode(response, skip_special_tokens=True)

    # Try to extract JSON from the model's response
    try:
        start = decoded.find("{")
        end = decoded.rfind("}") + 1
        challenge_json = decoded[start:end]
        challenge_data = json.loads(challenge_json)

        # Ensure all required fields are present
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data
    except Exception as e:
        # If parsing fails, print the error and return a fallback challenge
        print("Failed to parse model response:", e)
        print("Raw response:", decoded)
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