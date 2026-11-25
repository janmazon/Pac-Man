from .controller import App
from src.utils import Parser


def main() -> None:

    highscores = Parser.load_highscores()
    App().run(highscores)


if __name__ == "__main__":
    main()
