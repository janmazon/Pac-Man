from .models import Level
from mazegenerator import MazeGenerator
from .controller import App
# from .view import LevelView


def main() -> None:

    maze_gen = MazeGenerator()
    maze_gen.generate()
    seed = maze_gen._seed
    level = Level(maze_gen.maze)
    print(f"Seed={seed}")

    level.print_info()
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

    App(level).run()


if __name__ == "__main__":
    main()
