import copy
from sqlalchemy import func
from layernode import tools
from layernode.service import lockit


class StateDatabase:
    """
    StateDatabase is where we evaluate and store the current state of blockchain.
    User accounts referring addresses, jobs, authorities and many more are stored here.
    State change can be triggered by only adding or removing a block.
    A state can be simulated against a transaction, multiple transactions or blocks.
    These simulations can be recorded or removed upon the result of simulation.
    Simulations are basically not committed database changes.
    """

    def __init__(self, engine):
        self.engine = engine
        self.db = self.engine.db
        self.blockchain = self.engine.blockchain