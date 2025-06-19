#Token authentification
from huggingface_hub import HfApi, HfFolder, hf_hub_download
import os

HF_TOKEN = os.getenv('HF_TOKEN')
if not HF_TOKEN:
        HF_TOKEN = input('Enter your Hugging Face token: ').strip()
HfFolder.save_token(HF_TOKEN)

model_ids = [
    'Qwen/QwQ-32B', 
    'Qwen/Qwen2-72B-Instruct',
    'Qwen/Qwen2-7B-Instruct',
    'google/gemma-2-27b',
    'deepseek-ai/deepseek-moe-16b-chat',
    'meta-llama/Llama-3.1-8B',
    'meta-llama/Llama-3.1-70B-Instruct',
    'meta-llama/Llama-3.1-405B-Instruct',
    'meta-llama/Llama-3.2-11B-Vision-Instruct',
    'meta-llama/Llama-2-7b-chat-hf',
    'meta-llama/Llama-2-70b-chat-hf',
    'amd/Llama-3.1-8B-Instruct-FP8-KV',
    'amd/Llama-3.1-70B-Instruct-FP8-KV',
    'amd/Llama-3.1-405B-Instruct-FP8-KV',
]

for model_id in model_ids:
    try: 
        print(f"Getting model card for: {model_id}...")
        # Download the README.md file directly
        readme_content = hf_hub_download(repo_id=model_id, filename="README.md", repo_type="model")
        
        #split by name
        parts = model_id.split('/')
        if len(parts) == 2:
            org, model = [part.lower() for part in parts]
        else:
            org = input("organization name: ")
            model = input("model name: ")

        #Create a directory for the model
        directory_path = os.path.join("models",org,model)
        os.makedirs(directory_path, exist_ok=True)
        filename = os.path.join(directory_path, "model_card.md")
        
        # Copy the downloaded README to our desired location
        with open(readme_content, 'r', encoding='utf-8') as source:
            content = source.read()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved model card to: {filename}")
    except Exception as e:
        print(f"Error fetching model card for {model_id}: {e}")
        