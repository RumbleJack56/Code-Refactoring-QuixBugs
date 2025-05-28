import openai
import ast
from pathlib import Path

class CodeRepairAgent:
    def __init__(self, model="gpt-4", api_key="your-api-key"):
        self.model = model
        openai.api_key = api_key
        self.prompt_template = """Fix this Python bug:\n\n{code}\n\nError: {error}\n\nReturn ONLY the corrected code in a markdown block (```python ... ```)."""

    def fix_code(self, code, error):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt_template.format(code=code, error=error)}],
            temperature=0.2
        )
        return self._extract_code(response.choices[0].message.content)

    def _extract_code(self, response):
        if '```python' in response:
            return response.split('```python')[1].split('```')[0].strip()
        return response.strip()