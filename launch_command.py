import yaml
import sys
import os

DOCKER_BASE_COMMAND = r"""docker run -it --rm \
  --network=host \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add=video \
  --ipc=host \
  --cap-add=SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --shm-size 8G \
  -e HF_TOKEN=$HF_TOKEN \
  -v $(pwd):/workspace \
  -w /workspace/notebooks \
  rocm/vllm:latest \
  bash -c """

def build_vllm_command(config):
    env = config.get("environment", {})
    vllm = config.get("vllm_config", {})

    # Include only environment variables you want in the docker run env string
    env_vars_to_include = ["VLLM_USE_TRITON_FLASH_ATTN"]
    filtered_env = {k: v for k, v in env.items() if k in env_vars_to_include}
    env_str = " ".join(f"{k}={v}" for k, v in filtered_env.items())
    
    model_id = vllm.get("model_id")
    served_model_name = vllm.get("served_model_name")
    api_key = vllm.get("api_key")
    port = vllm.get("port")

    vllm_command = f"{env_str} vllm serve {model_id} --served-model-name {served_model_name} --api-key {api_key} --port {port} --trust-remote-code"

    return vllm_command.strip()

def main():
    if len(sys.argv) != 2:
        print("Usage: python launch_command.py model_name_on_hf")
        sys.exit(1)

    yaml_path = "models/" + sys.argv[1].lower() + "/config.yaml"

    try:
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File '{yaml_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

    vllm_command = build_vllm_command(config)

    # Escape double quotes in vllm_command for bash -c
    escaped_vllm_command = vllm_command.replace('"', '\\"')

    full_command = DOCKER_BASE_COMMAND + f'"{escaped_vllm_command}"'

    print("\nFull docker command to run:\n")
    print(full_command)
    print("\nRunning docker command now...\n")

    os.system(full_command)

if __name__ == "__main__":
    main()