from .controller import App
from typing import Any
import json
from .models import Highscore
from pydantic import ValidationError


def main() -> None:
    """ cell = level.getMaze().getCell(0, 0)
    print("Muros del (0, 0):")
    cell.__str__()

    cell = level.getMaze().getCell(1, 0)
    print("Muros del (1, 0):")
    cell.__str__()

    cell = level.getMaze().getCell(0, 1)
    print("Muros del (0, 1):")
    cell.__str__()

    pygame = LevelView(level)
    pygame.show_view() """

    # Todo esto hay que parsear en una clase o algo, de momento es para hacerlo rapido

    path = "data/highscores.json"
    try:
        with open(path, encoding="UTF-8") as file:
            data: list[dict[str, Any]] = json.load(file)
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")

    highscores: list[Highscore] = []
    for index, item in enumerate(data):
        try:
            highscores.append(Highscore.model_validate(item))
        except ValidationError as e:
            print(f"Validarion error: {e}")

    highscores.sort(key=lambda h: h.score, reverse=True)
    print(f"Highscores={highscores}")
    print("Hola")
    App().run(highscores)


if __name__ == "__main__":
    main()
