from src.models import Highscore
import json
from typing import Any
from pydantic import ValidationError


class Parser:

    @staticmethod
    def load_highscores(path: str = "data/highscores.json") -> list[Highscore]:
        data: list[dict[str, Any]] = []

        try:
            with open(path, encoding="UTF-8") as file:
                raw = json.load(file)
                if isinstance(raw, list):
                    data = raw
        except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
            print(f"Error loading {path}: {e}")
            return []

        highscores: list[Highscore] = []
        for item in data:
            try:
                highscores.append(Highscore.model_validate(item))
            except ValidationError as e:
                print(f"Validation error: {e}")

        highscores.sort(key=lambda h: h.score, reverse=True)

        return highscores
