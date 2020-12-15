from typing import Tuple, List, Dict
import numpy as np

from .simulator import Simulator


_DIAG_INDICES = np.array([0, 4, 8]).astype(np.int32)
_CROSS_DIAG_INDICES = np.array([2, 4, 6]).astype(np.int32)


class TicTacToe(Simulator):
    
    @classmethod
    def reset(cls, n: int) -> np.ndarray:
        states = np.zeros((n, 10))
        states[:, -1] = 1.0
        return states

    @classmethod
    def check_win(cls, states: np.ndarray) -> np.ndarray:
        batchvec = np.arange(states.shape[0])
        repeated_batchvec = np.repeat(batchvec, 3)
        tiled_diag_indices = np.tile(_DIAG_INDICES, batchvec.shape[0])
        tiled_cross_diag_indices = np.tile(_CROSS_DIAG_INDICES, batchvec.shape[0])

        player = np.reshape(states[batchvec, -1], (-1, 1))
        own_marks = states[:, :-1] == player

        row_win = np.any(np.all(np.reshape(own_marks, (-1, 3, 3)), axis=2), axis=1)
        col_win = np.any(np.all(np.reshape(own_marks, (-1, 3, 3)), axis=1), axis=1)
        diagwin = np.all(np.reshape(own_marks[repeated_batchvec, tiled_diag_indices], (-1, 3)), axis=1)
        crossdiagwin = np.all(np.reshape(own_marks[repeated_batchvec, tiled_cross_diag_indices], (-1, 3)), axis=1)

        return row_win | col_win | diagwin | crossdiagwin

    @classmethod
    def check_loss(cls, states: np.ndarray) -> np.ndarray:
        states = states.copy()
        states[:, -1] = -states[:, -1]
        return cls.check_win(states)

    @classmethod
    def step_bulk(cls, states: np.ndarray, actions: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[Dict]]:

        if np.any(cls.check_loss(states)) or np.any(cls.check_win(states)):
            raise ValueError("Cannot step from a state already in a win condition.")
        
        next_states = states.copy()
        batchvec = np.arange(next_states.shape[0])

        if np.any(next_states[batchvec, actions] != 0.0):
            raise ValueError("Cannot place a piece at an already occupied spot")

        next_states[batchvec, actions] = next_states[batchvec, -1]
        
        rewards = np.zeros(batchvec.shape[0])
        win = cls.check_win(next_states)
        rewards[win] = 1.0
        loss = cls.check_loss(next_states)
        rewards[loss] = -1.0

        terminals = win | loss

        next_states[batchvec, -1] = -states[batchvec, -1]

        return next_states, rewards, terminals, [{} for _ in range(batchvec.shape[0])]
