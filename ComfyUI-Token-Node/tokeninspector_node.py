import torch
import json
from safetensors.torch import load_file
from transformers import CLIPTokenizer, CLIPTextModel, CLIPTextConfig
from torch.nn.functional import cosine_similarity

class TokenCheckpointAnalytics:
    MAX_CHUNK_SIZE = 77  # pro Encoder-Limit, Chunks bis 420 Tokens möglich

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "A red ball on floor."}),
                "checkpoint_file": ("STRING", {"default": ""}),
                "reference_prompt": ("STRING", {"default": "A red ball on floor."}),
                "SAL_IN": ("FLOAT",)  
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "Token Analytics"

    @staticmethod
    def chunk_list(lst, chunk_size):
        """Teilt eine Liste in Chunks."""
        return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

    @staticmethod
    def process(prompt: str, checkpoint_file: str, reference_prompt: str, SAL_IN):
        try:
            # Überprüfung auf SAL_IN
            if SAL_IN is None:
                raise Exception("Missing Math-Algorythm ClipWeight")

            tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")

            # Tokenize prompt & reference
            encoded_prompt = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)
            input_ids = encoded_prompt['input_ids'].squeeze(0)
            token_strings = tokenizer.convert_ids_to_tokens(input_ids)

            encoded_ref = tokenizer(reference_prompt, return_tensors="pt", add_special_tokens=True)
            ref_ids = encoded_ref['input_ids'].squeeze(0)
            ref_tokens = tokenizer.convert_ids_to_tokens(ref_ids)

            # TextEncoder
            config = CLIPTextConfig(
                hidden_size=2048,
                intermediate_size=8192,
                num_attention_heads=32,
                num_hidden_layers=24,
                vocab_size=49408,
                max_position_embeddings=420
            )
            text_encoder = CLIPTextModel(config)

            # Load checkpoint
            state_dict = load_file(checkpoint_file, device="cpu")
            prefix = "model.text_encoder."
            new_state_dict = {k[len(prefix):]: v for k, v in state_dict.items() if k.startswith(prefix)}
            text_encoder.load_state_dict(new_state_dict, strict=False)
            text_encoder.eval()

            # Chunking
            input_chunks = TokenCheckpointAnalytics.chunk_list(input_ids.tolist(), TokenCheckpointAnalytics.MAX_CHUNK_SIZE)
            token_chunks = TokenCheckpointAnalytics.chunk_list(token_strings, TokenCheckpointAnalytics.MAX_CHUNK_SIZE)
            ref_chunks = TokenCheckpointAnalytics.chunk_list(ref_ids.tolist(), TokenCheckpointAnalytics.MAX_CHUNK_SIZE)

            token_scores = []
            composed_count = 0

            with torch.no_grad():
                for ic, tc, rc in zip(input_chunks, token_chunks, ref_chunks):
                    ic_tensor = torch.tensor(ic).unsqueeze(0)
                    rc_tensor = torch.tensor(rc).unsqueeze(0)

                    prompt_emb = text_encoder(ic_tensor).last_hidden_state.squeeze(0)
                    ref_emb = text_encoder(rc_tensor).last_hidden_state.squeeze(0)

                    min_len = min(prompt_emb.shape[0], ref_emb.shape[0])
                    for i in range(min_len):
                        score = float(cosine_similarity(prompt_emb[i].unsqueeze(0), ref_emb[i].unsqueeze(0)).item())

                        # Subtoken depth
                        subtoken = tc[i]
                        depth = 1
                        j = i
                        while not subtoken.endswith("</w>") and j + 1 < len(tc):
                            j += 1
                            subtoken = tc[j]
                            depth += 1

                        token_type = "direct_training" if depth == 1 else "composed_token"
                        if token_type == "composed_token":
                            composed_count += 1

                        token_scores.append({
                            "token": tc[i],
                            "score_known": score,
                            "subtoken_depth": depth,
                            "token_type": token_type
                        })

            total_tokens = len(token_scores)
            composed_ratio = composed_count / max(total_tokens, 1)

            # Risikobewertung
            if composed_ratio < 0.2:
                risk_level = "Low"
            elif composed_ratio < 0.5:
                risk_level = "Medium"
            else:
                risk_level = "High"

            weighted_risk_score = composed_ratio * (1 - (sum(t["score_known"] for t in token_scores) / max(total_tokens, 1)))
            prompt_score = sum(t["score_known"] for t in token_scores) / max(total_tokens, 1)

            node_properties = {
                "prompt_score": prompt_score,
                "token_count": total_tokens,
                "composed_token_count": composed_count,
                "composed_ratio": composed_ratio,
                "risk_level": risk_level,
                "weighted_risk_score": weighted_risk_score
            }

            result = {
                "tokens": token_scores,
                "prompt_score": prompt_score,
                "node_properties": node_properties
            }

            return (json.dumps(result, indent=2),)

        except Exception as e:
            return (f"EXCEPTION: {str(e)}",)


NODE_CLASS_MAPPINGS = {
    "TokenCheckpointAnalytics": TokenCheckpointAnalytics,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TokenCheckpointAnalytics": "TokenCheckpointAnalytics",
}

# =====================================================
# NOTE / LICENSE
# =====================================================
#
# Script & Function by: https://github.com/solongeran54
# Built in 2025
#
# MIT License
#(You are free to use, modify, and integrate this node in commercial and non-commercial
# projects.)
#   
# Please respect the author’s work and time
#
# All Rights Reserved © 2025
#
# You are welcome to share and contribute to the Open Source community.
# 
# This Node is developed in the great EU (Germany2025)
# =====================================================
