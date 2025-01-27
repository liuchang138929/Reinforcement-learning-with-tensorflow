from matlab_env import m_e
from RL_brain import DeepQNetwork


def run_m_e():
    step = 0
    for episode in range(300):
        # initial observation
        observation = env.reset()
        step2 = 0
        while True:
            # fresh env
            # env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)
            RL.store_transition(observation, action, reward, observation_)

            if (step > 50) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1
            step2 += 1
            print(step2)
            print(step)

    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    # maze game
    env = m_e()
    print(env.n_features)
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    print("start training")
    run_m_e()
    RL.plot_cost()
