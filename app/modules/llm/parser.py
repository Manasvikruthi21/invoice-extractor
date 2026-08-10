import json


class ResponseParser:
    @staticmethod
    def parse(response: str):
        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()

        return json.loads(response)