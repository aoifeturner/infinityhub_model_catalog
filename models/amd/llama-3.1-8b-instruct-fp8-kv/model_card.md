---
base_model: meta-llama/Meta-Llama-3.1-8B-Instruct
license: other
license_name: llama3.1
license_link: https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/LICENSE
---
# Meta-Llama-3.1-8B-Instruct-FP8-KV
- ## Introduction
  This model was created by applying [Quark](https://quark.docs.amd.com/latest/index.html) with calibration samples from Pile dataset.
- ## Quantization Stragegy
  - ***Quantized Layers***: All linear layers excluding "lm_head"
  - ***Weight***: FP8 symmetric per-tensor
  - ***Activation***: FP8 symmetric per-tensor
  - ***KV Cache***: FP8 symmetric  per-tensor
- ## Quick Start
1. [Download and install Quark](https://quark.docs.amd.com/latest/install.html)
2. Run the quantization script in the example folder using the following command line:
```sh
export MODEL_DIR = [local model checkpoint folder] or meta-llama/Meta-Llama-3.1-8B-Instruct 
# single GPU
python3 quantize_quark.py \
        --model_dir $MODEL_DIR \
        --output_dir Meta-Llama-3.1-8B-Instruct-FP8-KV \
        --quant_scheme w_fp8_a_fp8 \
        --kv_cache_dtype fp8 \
        --num_calib_data 128 \
        --model_export quark_safetensors \
        --no_weight_matrix_merge \
        --custom_mode fp8

# If model size is too large for single GPU, please use multi GPU instead.
python3 quantize_quark.py \
        --model_dir $MODEL_DIR \
        --output_dir Meta-Llama-3.1-8B-Instruct-FP8-KV \
        --quant_scheme w_fp8_a_fp8 \
        --kv_cache_dtype fp8 \
        --num_calib_data 128 \
        --model_export quark_safetensors \
       --no_weight_matrix_merge \
        --multi_gpu \
        --custom_mode fp8
```
## Deployment
Quark has its own export format and allows FP8 quantized models to be efficiently deployed using the vLLM backend(vLLM-compatible).

## Evaluation
Quark currently uses perplexity(PPL) as the evaluation metric for accuracy loss before and after quantization.The specific PPL algorithm can be referenced in the quantize_quark.py.
The quantization evaluation results are conducted in pseudo-quantization mode, which may slightly differ from the actual quantized inference accuracy. These results are provided for reference only.

#### Evaluation scores
<table>
  <tr>
   <td><strong>Benchmark</strong>
   </td>
   <td><strong>Meta-Llama-3.1-8B-Instruct </strong>
   </td>
   <td><strong>Meta-Llama-3.1-8B-Instruct-FP8-KV(this model)</strong>
   </td>
  </tr>
  <tr>
   <td>Perplexity-wikitext2
   </td>
   <td>7.2169
   </td>
   <td>7.2752
   </td>
  </tr>
  
</table>



#### License
Modifications copyright(c) 2024 Advanced Micro Devices,Inc. All rights reserved.
