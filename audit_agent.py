# audit_agent.py - TRACK 1: DIRECT PYTORCH + TRANSFORMERS ON MI300X
import os
import warnings
import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.tools import DuckDuckGoSearchRun

warnings.filterwarnings("ignore")
load_dotenv()

# 🔁 GLOBAL CACHE: Load model once, reuse for every audit request
_model = None
_tokenizer = None

def _get_model():
    """Loads Qwen 2.5 on MI300X (cached across calls)."""
    global _model, _tokenizer
    if _model is None:
        model_id = os.getenv("MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")
        print(f"Loading {model_id} onto MI300X...")
        _tokenizer = AutoTokenizer.from_pretrained(model_id)
        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
    return _model, _tokenizer

def create_audit_agent():
    """Returns a callable agent function for AuditEye."""
    search_tool = DuckDuckGoSearchRun(max_results=3)
    
    def agent_fn(prompt: str, use_web_search: bool = True) -> str:
        model, tokenizer = _get_model()
        
        # 🔍 Dynamic web search query based on item being audited
        market_info = ""
        if use_web_search:
            try:
                search_query = f"market price {prompt[:100]} Philippines procurement"
                market_info = search_tool.run(search_query)
                # Filter out irrelevant stock/industry analysis
                if any(kw in market_info.lower() for kw in ["stock market", "market analysis", "industry report", "usps", "vulnerability"]):
                    market_info = "Web search returned analysis, not specific pricing data."
            except Exception:
                market_info = "Web search unavailable."
        
        # 🔥 ULTRA-SIMPLE PROMPT (7B-friendly, prevents echoing)
        full_prompt = f"""Analyze: {prompt} | Web: {market_info}
Rules: 1) PHP default. 2) Baseline: Internal>Web>INSUFFICIENT. 3) Markup=((L-B)/B)*100. 4) Anomaly=TRUE if |markup|>threshold. 5) Output 5 lines ONLY:
Listed Price: [num]₱
Baseline: [num]₱(src) or INSUFFICIENT₱
Markup: [num]% or N/A
Anomaly: TRUE/FALSE
Reasoning: [1 short sentence]
If no price found: use INSUFFICIENT, Markup=N/A, Anomaly=FALSE. No notes. No repeats."""
        
        # 🔁 Run inference directly on MI300X
        inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.0,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        return tokenizer.decode(output[0], skip_special_tokens=True)
    
    return agent_fn

# 🔬 Local CLI test (optional)
if __name__ == "__main__":
    print("Booting AuditEye on MI300X (PyTorch + ROCm)...")
    agent = create_audit_agent()
    result = agent("Item: Blood Analyzer, Price: 2059420, Threshold: 50%", use_web_search=True)
    print(result)
