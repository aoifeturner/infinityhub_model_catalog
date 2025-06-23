import subprocess
import yaml
import shlex
import os

def load_config(config_path="vllm_config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def build_vllm_command(cfg):
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", cfg["model"],
        "--port", str(cfg.get("port", 8000)),
        "--tokenizer", cfg.get("tokenizer", cfg["model"])
    ]

    if "dtype" in cfg:
        cmd += ["--dtype", cfg["dtype"]]
    if "tensor_parallel_size" in cfg:
        cmd += ["--tensor-parallel-size", str(cfg["tensor_parallel_size"])]
    if "gpu_memory_utilization" in cfg:
        cmd += ["--gpu-memory-utilization", str(cfg["gpu_memory_utilization"])]
    if "max_model_len" in cfg:
        cmd += ["--max-model-len", str(cfg["max_model_len"])]
    if "extra_args" in cfg:
        cmd += cfg["extra_args"]

    return cmd

def main():
    # Change working directory to script directory (where YAML config lives)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    config = load_config()
    cmd = build_vllm_command(config)

    print("Launching vLLM with command:")
    print(" ".join(shlex.quote(arg) for arg in cmd))

    # On Windows, use shell=True to run the command properly
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
