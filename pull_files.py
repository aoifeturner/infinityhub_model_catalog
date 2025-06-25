#Token authentification
from huggingface_hub import HfApi, HfFolder, hf_hub_download
import os
import yaml

HF_TOKEN = os.getenv('HF_TOKEN')
if not HF_TOKEN:
        HF_TOKEN = input('Enter your Hugging Face token: ').strip()
HfFolder.save_token(HF_TOKEN)

with open('model_ids.txt', 'r') as file:
    model_ids = file.read().splitlines()

for model_id in model_ids:
    #Creating the model cards
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



        #Creating the yaml files
        yaml_content = {
            'environment': {
                'HIP_VISIBLE_DEVICES': "0",               # Optional, change if needed
                'VLLM_USE_TRITON_FLASH_ATTN': "0",
            },
            'vllm_config': {
                'model_id': model_id,                     # e.g., deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
                'served_model_name': model,               # e.g., deepseek-r1-distill-qwen-32b
                'api_key': 'abc-123',
                'port': 8000,
                'trust_remote_code': True,
                'tp': 8
            }
        }


        #Same yaml file in proper folder
        yaml_path = os.path.join(directory_path, "config.yaml")
        with open(yaml_path, 'w', encoding='utf-8') as yf:
            yaml.dump(yaml_content, yf, default_flow_style=False)
        print(f"Saved config YAML to: {yaml_path}")

    except Exception as e:
        print(f"Error fetching model card for {model_id}: {e}")
        