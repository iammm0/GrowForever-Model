from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import os

# 1. 加载预训练模型与分词器（可换成中文模型或自己微调后的模型）
MODEL_NAME = os.getenv("GPT_MODEL_NAME", "gpt2")
CACHE_DIR = os.getenv("HF_CACHE_DIR", None)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)

# 2. 生成配置（可根据需要调整）
gen_config = GenerationConfig(
    max_new_tokens=200,
    temperature=0.8,
    top_p=0.9,
    do_sample=True,
    num_return_sequences=1,
)

def generate_expansion_text(title: str, 
                            description: str,
                            depth: int = 0) -> str:
    """
    根据节点 title 与 description 生成扩展的长文本。
    depth 可用于在 prompt 中控制生成的层级或风格。
    """
    prompt = (
        f"【Node Title】: {title}\n"
        f"【Node Description】: {description}\n"
        f"【Expansion Depth】: {depth}\n\n"
        "请基于以上信息，为该节点生成若干后续想法的详细描述，"
        "用中文分段或英文句子描述均可："
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs, 
        generation_config=gen_config,
        pad_token_id=tokenizer.eos_token_id
    )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 去掉 prompt 本身，只保留模型生成部分
    return text[len(prompt):].strip()
