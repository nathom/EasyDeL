# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from easydel.modules.deepseek_v2.deepseek_configuration import DeepseekV2Config
from easydel.modules.deepseek_v2.modeling_deepseek_flax import (
	FlaxDeepseekV2ForCausalLM,
	FlaxDeepseekV2Model,
)

__all__ = "FlaxDeepseekV2ForCausalLM", "FlaxDeepseekV2Model", "DeepseekV2Config"
