from argparse import ArgumentParser

from torch import optim

from rl.simulators import ConnectFour
from rl.agents.alpha_zero import networks, train, LearnerConfig, SelfPlayConfig


parser = ArgumentParser()


if __name__ == "__main__":
    args = parser.parse_args()

    net = networks.ConnectFourNetwork()
    train(
        ConnectFour,
        8,
        LearnerConfig(),
        SelfPlayConfig(),
        net,
        optim.Adam(net.parameters(), lr=1e-3),
        save_path="models/alpha_zero/connect_four",
        save_period=60,
        train_time=120,
    )
