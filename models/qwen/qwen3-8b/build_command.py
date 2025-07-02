import yaml
from pathlib import Path
import subprocess

def build_and_run_docker_command():
    yaml_path = Path("config.yaml")

    if not yaml_path.is_file():
        print("config.yaml not found in current directory.")
        return

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    # Environment variables - exclude HIP_VISIBLE_DEVICES
    env_vars = config.get("environment", {})
    filtered_env_vars = {k: v for k, v in env_vars.items() if k != "HIP_VISIBLE_DEVICES"}
    env_str = " ".join(f"{k}={v}" for k, v in filtered_env_vars.items())

    # vLLM config
    vllm = config.get("vllm_config", {})
    model_id = vllm.get("model_id")
    served_model_name = vllm.get("served_model_name")
    api_key = vllm.get("api_key")
    port = vllm.get("port")

    if not all([model_id, served_model_name, api_key, port]):
        print("Missing required vllm_config values.")
        return

    # Build the vllm serve command
    cmd_parts = []
    if env_str:
        cmd_parts.append(env_str)
    cmd_parts.append(f"vllm serve {model_id}")
    cmd_parts.append(f"--served-model-name {served_model_name}")
    cmd_parts.append(f"--api-key {api_key}")
    cmd_parts.append(f"--port {port}")
    cmd_parts.append("--trust-remote-code")
    vllm_command = " ".join(cmd_parts)

    # Escape double quotes in the vllm command for bash -c
    vllm_command_escaped = vllm_command.replace('"', '\\"')

    # Build the full docker run command
    docker_command = (
        'docker run -it --rm '
        '--network=host '
        '--device=/dev/kfd '
        '--device=/dev/dri '
        '--group-add=video '
        '--ipc=host '
        '--cap-add=SYS_PTRACE '
        '--security-opt seccomp=unconfined '
        '--shm-size 8G '
        '-v "$(pwd)":/workspace '
        '-w /workspace/notebooks '
        'rocm/vllm:latest '
    )

    print(f"Running Docker command:\n{docker_command}\n")
    print(f"\n\nInside docker command: \n{vllm_command_escaped}\n")

    # Run the docker command
    subprocess.run(docker_command, shell=True)

if __name__ == "__main__":
    build_and_run_docker_command()