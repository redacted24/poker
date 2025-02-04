try:
    from poker.classes.game import *
    from poker.classes.eval import *
except:
    from game import *      # type: ignore
    from eval import *      # type: ignore

class Poki(Player):
    