# InfinityHub Model Catalog (WIP)

This project automates the deployment of ML models through generating and configuring YAML files seamlessly on DigitalOcean. With a single call, the project creates a Docker container configured to run the model on a vLLM backend, allowing for a scalable and easy-to-use model instance with minimal user set-up. Each model’s README files are also pulled from HuggingFace.

> **Note**: This was designed for DigitalOcean.

---

## Installation & Usage

### Access the Code

1. SSH into your DigitalOcean droplet.
2. Clone the repository:

   ```bash
   git clone https://github.com/aoifeturner/infinityhub_model_catalog

### Update/Add Models (if needed)

You only need to install requirements if you plan to update any of the `model_card.md` files or support additional model versions.

#### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Inside the virtual environment, install the requirements

```bash
pip install -r requirements.txt
```

#### 3. Support More Models (if needed)
If you hope to support more models, update the model_ids.txt. You can use nano as a text editor. On a new line, copy and paste the exact model name from HuggingFace. It should look like Organization/Model-Name. Make sure to save your changes.

```bash
nano model_ids.txt
```

Update the model cards. Do this if you want to update existing model cards or after you have included another model to support. This will update the model’s README.md files and reset their  config.yaml files.
```bash
python3 pull_files.py
```
You will be asked to include a HuggingFace token as input. Add as needed.
Newly added models should be found under infinityhub_model_catalog/models. 

#### 4. Deactivate the Virtual Environment.
Once you have checked that it was updated accordingly, deactivate the venv.
```bash
deactivate
```
---
### Launching Models

#### Time to launch the models. In the place that says [insert hf model name], add the exact model name from HuggingFace. It should look like Organization/Model-Name. This tells the computer which model you hope to run.
```bash
cd infinityhub_model_catalog
python3 launch_command.py [insert hf model name]
```
#### Once loaded, ssh into the same droplet on a separate terminal. Your ML is now running. You can now ask it questions (must be prompted in proper format, see model’s specific details).

---
### Configurations

#### Changing the config.yaml files. SO far, they look like this:
```bash
environment:
    HIP_VISIBLE_DEVICES: '0'
    VLLM_USE_TRITON_FLASH_ATTN: '0'
vllm_config:
    api_key: abc-123
    model_id: [insert hf model name]
    port: 8000
    served_model_name: qwen3-8b
    tp: 8
```

#### As this is a WIP, Tensor Parallel (tp) and HIP_VISIBLE_DEVICES has not been properly implemented. In the future, this will allow users to specify the number of GPU nodes they want used/which they want used. For now, to change the port that the model runs on, simply change the port on the yaml file before launching. 

---
### Contact
#### Contact aoturner@amd.com with inquiries. This is a WIP and a small scale of the final product.