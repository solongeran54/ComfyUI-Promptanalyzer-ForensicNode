class BGNodeJS:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_input": ("STRING", {"default": "SET_BACK$5c_"}),
                "number_input": ("NUMBER", {"default": 42, "min": 0, "max": 100}),
                "flag": ("BOOLEAN", {"default": True})
            }
        }

    RETURN_TYPES = ("STRING", "NUMBER", "BOOLEAN")  # gibt genau das zurück
    FUNCTION = "run"
    CATEGORY = "BG_Node_JS"

    def run(self, text_input="SET_BACK$5c_", number_input=42, flag=True, **kwargs):
        # Einfach alles unverändert zurückgeben
        return (text_input, number_input, flag)


# Node Registry
NODE_CLASS_MAPPINGS = {
    "BGNodeJS": BGNodeJS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BGNodeJS": "Background Image NodeJS"
}

# This Function is a Placeholder for later Versions.
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