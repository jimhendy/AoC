class CannotMoveException(Exception):
    pass


class NoTargetsException(CannotMoveException):
    pass


class NoPossibleAdjacentLocsException(CannotMoveException):
    pass


class NoPossiblePathsException(CannotMoveException):
    pass


class GameOverException(Exception):
    pass
