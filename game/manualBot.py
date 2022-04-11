import numpy as np
import Config
from game import check


def hypothesis(board):
    scores = check.check_all(np.copy(board), Config.opponentValue, connect_four_score=10)
    opponent_scores = check.check_all(np.copy(board), Config.playerValue)

    opponent_scores[opponent_scores<4] = 0
    print("player: {}".format(scores + opponent_scores*0.75))
    scores = scores + opponent_scores*0.75
    return scores
