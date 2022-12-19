# Advent of code 2022, by Ghostkeeper

import collections
import functools
import get_input_file
import re

Factory = collections.namedtuple("Factory", ["orebot", "claybot", "obsbot", "geobot"])  # Each type of bot is a tuple of the 3 resources it needs.

text = open(get_input_file.get_path(19, 1)).read()
factories = []
for match in re.finditer(r"Blueprint \d\d?: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", text):
	factories.append(Factory(orebot=(int(match.group(1)), 0, 0),
	                         claybot=(int(match.group(2)), 0, 0),
	                         obsbot=(int(match.group(3)), int(match.group(4)), 0),
	                         geobot=(int(match.group(5)), 0, int(match.group(6)))))

best_time = 0
@functools.lru_cache(maxsize=None)
def most_geodes(time_left, factory, orebots, claybots, obsbots, geobots, ores, clays, obss):
	"""
	Calculate the maximum amount of geodes you could gather with the given resources and bots in a certain amount of
	time.
	:param time_left: How much time there is left to gather geodes.
	:param orebots: The number of ore-gathering robots we have.
	:param claybots: The number of clay-gathering robots we have.
	:param obsbots: The number of obsidian-gathering robots we have.
	:param geobots: The number of geode-gathering robots we have.
	:param ores: The number of ores we have.
	:param clays: The number of pieces of clay we have.
	:param obss: The number of pieces of obsidian we have.
	:return: The maximally obtainable amount of geodes we could gather.
	"""
	best_geodes = 0

	if time_left == 0:
		return 0  # Can't build anything any more.

	# Consider the option of doing nothing for a minute.
	geodes = most_geodes(time_left - 1, factory, orebots, claybots, obsbots, geobots, ores + orebots, clays + claybots, obss + obsbots) + geobots
	best_geodes = max(best_geodes, geodes)

	# Consider the option of building an orebot.
	if ores >= factory.orebot[0] and clays >= factory.orebot[1] and obss >= factory.orebot[2]:
		geodes = most_geodes(time_left - 1, factory, orebots + 1, claybots, obsbots, geobots, ores + orebots - factory.orebot[0], clays + claybots - factory.orebot[1], obss + obsbots - factory.orebot[2]) + geobots
		best_geodes = max(best_geodes, geodes)

	# Consider the option of building a claybot.
	if ores >= factory.claybot[0] and clays >= factory.claybot[1] and obss >= factory.claybot[2]:
		geodes = most_geodes(time_left - 1, factory, orebots, claybots + 1, obsbots, geobots, ores + orebots - factory.claybot[0], clays + claybots - factory.claybot[1], obss + obsbots - factory.claybot[2]) + geobots
		best_geodes = max(best_geodes, geodes)

	# Consider the option of building an obsbot.
	if ores >= factory.obsbot[0] and clays >= factory.obsbot[1] and obss >= factory.obsbot[2]:
		geodes = most_geodes(time_left - 1, factory, orebots, claybots, obsbots + 1, geobots, ores + orebots - factory.obsbot[0], clays + claybots - factory.obsbot[1], obss + obsbots - factory.obsbot[2]) + geobots
		best_geodes = max(best_geodes, geodes)

	# Consider the option of building a geobot.
	if ores >= factory.geobot[0] and clays >= factory.geobot[1] and obss >= factory.geobot[2]:
		geodes = most_geodes(time_left - 1, factory, orebots, claybots, obsbots, geobots + 1, ores + orebots - factory.geobot[0], clays + claybots - factory.geobot[1], obss + obsbots - factory.geobot[2]) + geobots
		best_geodes = max(best_geodes, geodes)

	global best_time
	if time_left > best_time:
		best_time = max(best_time, time_left)
		print(best_time)

	return best_geodes

total_quality = 0
for i, factory in enumerate(factories):
	best_time = 0
	geodes = most_geodes(24, factory, 1, 0, 0, 0, 0, 0, 0)
	total_quality += (i + 1) * geodes
	print("Could get", geodes, "geodes, quality is", (i + 1) * geodes, "making total", total_quality)

print("The sum of quality levels for each factory is:", total_quality)