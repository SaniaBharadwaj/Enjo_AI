import json

class Subconscious:
    """
    FUTURE-PROOF VERSION:
    Extracts ANY fact and categorizes it dynamically.
    """

    def get_analysis_prompt(self, user_text):
        return f"""
        Analyze the user's input for ANY permanent facts, preferences, or life details.
        Return a JSON dictionary where:
        - Keys are short, standardized category names (snake_case).
        - Values are the specific details.

        Examples:
        - "I'm allergic to nuts" -> {{"allergies": ["nuts"]}}
        - "My dog is Rover" -> {{"pets": "Dog named Rover"}}
        - "I live in Tokyo" -> {{"location": "Tokyo"}}
        - "I sold my Tesla stock" -> {{"stocks": []}} (Context awareness)

        Rules:
        1. If no permanent facts are found, return {{}}.
        2. Use existing categories if possible (name, stocks, projects).
        3. Create NEW categories if needed.

        User Input: "{user_text}"

        Output (JSON ONLY):
        """

    def parse_result(self, llm_response_text):
        try:
            clean_text = llm_response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)

            return data if data else None
        
        except Exception:
            return None