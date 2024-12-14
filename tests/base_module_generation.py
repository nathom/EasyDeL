# fmt:off
import os
import sys
import threading
import time

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import easydel as ed
# fmt:on
import jax
import torch
from huggingface_hub import HfApi
from jax import numpy as jnp
from jax import sharding

import transformers


PartitionSpec, api = sharding.PartitionSpec, HfApi()


def log_mem():
	while True:
		ed.utils.analyze_memory.SMPMemoryMonitor(5).print_current_status()
		time.sleep(5)


threading.Thread(target=log_mem)  # .start()


def main():
	sharding_axis_dims = (1, 1, 1, -1)
	max_length = 6144

	pretrained_model_name_or_path = "meta-llama/Llama-3.2-1B-Instruct"
	dtype = jnp.float16
	partition_axis = ed.PartitionAxis()

	dtype = jnp.float16

	model = ed.AutoEasyDeLModelForCausalLM.from_pretrained(
		pretrained_model_name_or_path,
		auto_shard_model=True,
		sharding_axis_dims=sharding_axis_dims,
		config_kwargs=ed.EasyDeLBaseConfigDict(
			freq_max_position_embeddings=max_length,
			mask_max_position_embeddings=max_length,
			attn_dtype=jnp.float16,
			gradient_checkpointing=ed.EasyDeLGradientCheckPointers.NONE,
			kv_cache_quantization_method=ed.EasyDeLQuantizationMethods.NONE,
			attn_mechanism=ed.AttentionMechanisms.VANILLA,
		),
		quantization_method=ed.EasyDeLQuantizationMethods.NONE,
		platform=ed.EasyDeLPlatforms.TRITON,
		param_dtype=dtype,
		dtype=dtype,
		torch_dtype=torch.float16,
		partition_axis=partition_axis,
		precision=jax.lax.Precision("fastest"),
	)

	tokenizer = transformers.AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
	tokenizer.padding_side = "left"
	tokenizer.pad_token_id = tokenizer.eos_token_id
	model.eval()
	model = model.quantize(
		method=ed.EasyDeLQuantizationMethods.A8BIT,
		block_size=128,
		quantization_pattern=".*(gate_proj|up_proj).*",
	)

	prompt = "Find the value of $x$ that satisfies the equation $4x+5 = 6x+7$."

	messages = [
		{
			"role": "system",
			"content": "Please reason step by step, and put your final answer within \\boxed{}. and give 3 different responses",
		},
		{"role": "user", "content": prompt},
	]

	ids = tokenizer.apply_chat_template(
		messages,
		return_tensors="jax",
		return_dict=True,
		max_length=max_length - 1024,
		padding="max_length",
		add_generation_prompt=True,
	)
	model.generation_config.max_new_tokens = 1024
	output = model.generate(**ids, generation_config=model.generation_config)
	print(output)


if __name__ == "__main__":
	main()
