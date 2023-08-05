# Other imports.
from simple_rl.agents import QLearningAgent, RandomAgent
from simple_rl.tasks import GridWorldMDP
from simple_rl.run_experiments import run_agents_on_mdp

def main():
	# Setup MDP.
	mdp = GridWorldMDP(width=10, height=3, init_loc=(1, 1), goal_locs=[(10, 3)], gamma=0.95)

	# Make agents.
	ql_agent = QLearningAgent(actions=mdp.get_actions())
	rand_agent = RandomAgent(actions=mdp.get_actions())

	# Run experiment and make plot.
	run_agents_on_mdp([ql_agent, rand_agent], mdp, instances=3, episodes=50, steps=50)

if __name__ == "__main__":
	main()
