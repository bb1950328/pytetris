from model.game import Game
from view.pygame_view import PygameView

if __name__ == '__main__':
    game = Game()
    view = PygameView(game)
    view.start()
    view.run()
