
        # 🧠 Compatible AI Models

    Enjo is designed to work with **Free Tier** high-performance models.
    You can swap these model names in your `data/config.json` file.

    ## 💎 Google Gemini (Primary Brain)
    *Requires `GEMINI_API_KEY` in .env*

    | Model Name | Description | Best For |
    | :--- | :--- | :--- |
    | **`gemini-2.5-flash** | Fast, high-context, efficient. | **Default.** Best balance of speed/smarts. |
    |  **"gemini-Flash-Lite",       # Reliable fallback
        **"gemini-3-flash-preview"   # High intelligence fallback

    ## ⚡ Groq (Speed Layer)
    *Requires `GROQ_API_KEY` in .env*

    | Model Name | Description | Best For |
    | :--- | :--- | :--- |
    | **`openai/gpt-oss-120b`** | Meta's Llama 3 (70B). Smart & fast. | **Default.** Excellent all-rounder. |
    | `llama3-8b-8192` | Meta's Llama 3 (8B). Blazing fast. | Simple commands, very low latency. |
    | `mixtral-8x7b-32768` | Mistral's MoE model. | Creative writing or roleplay. |

    ## 🏠 Local (Offline)
    *Requires a local server like LM Studio or Ollama*

    * `llama-3`
    * `mistral-v0.3`
    * `phi-3`