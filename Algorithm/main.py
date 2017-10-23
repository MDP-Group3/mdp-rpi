import time,sys
from simulator.simulator import Simulator
from robot.robot import Robot
from arena.arena import Arena
from arena.arenautils import ArenaUtils
from arena.arenaconstant import ArenaConstant
from algorithm.exploration import Exploration
from algorithm.fastestpath import FastestPath
from comm.comm import CommMgr

def main():
	robot = Robot((18,1), True)
	#robot.set_speed(100)
	
	#_real_map = Arena(robot)
	#ArenaUtils.load_arena_from_file(_real_map, 'map/SampleWeek11.txt')
	_explore_map = Arena(robot)
	_explore_map.set_allunexplored()

	CommMgr.connect()
	_explore = Exploration(_explore_map, robot, 300, 3600)
	_explore.run()
	CommMgr.close()

	#simulator = Simulator(False)
	#simulator.run_exploration(robot, 'map/17_week8.txt')


	
if __name__ == "__main__":
	main()