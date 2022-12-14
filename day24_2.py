# Advent of code 2022, by Ghostkeeper

import get_input_file
import math
import queue

# Parse the input grid.
lines = open(get_input_file.get_path(24, 1)).readlines()
grids = []  # 3D grid, one frame per minute of the 2D field. First dimension is T, second dimension is Y, third dimension is X.
grids.append([])
for line in lines:
	grids[0].append([])
	for char in line.strip()[1:-1]:
		if char == ".":
			grids[0][-1].append(0)
		elif char == ">":
			grids[0][-1].append(1 << 0)
		elif char == "^":
			grids[0][-1].append(1 << 1)
		elif char == "<":
			grids[0][-1].append(1 << 2)
		elif char == "v":
			grids[0][-1].append(1 << 3)
		elif char == "#":
			grids[0][-1].append(-1)
		else:
			raise Exception("Unknown input:", char)

width = len(grids[0][0])
height = len(grids[0]) - 2
cycle = width
while cycle / height != int(cycle / height):
	cycle += width

def step(grid):
	"""
	Compute new grid from the previous grid state. This moves the blizzards in the grid to their new positions.
	:param grid: A new grid with blizzards moved.
	:return: A new grid.
	"""
	new_grid = [[0 for _ in line] for line in grid]
	for y, line in enumerate(grid):
		for x, cell in enumerate(line):
			if cell == -1:
				new_grid[y][x] = -1
				continue
			if cell & (1 << 0):  # Blizzard going right.
				new_grid[y][(x + 1) % width] += 1 << 0
			if cell & (1 << 1):  # Blizzard going up.
				new_grid[(y - 2) % height + 1][x] += 1 << 1
			if cell & (1 << 2):  # Blizzard going left.
				new_grid[y][(x - 1) % width] += 1 << 2
			if cell & (1 << 3):  # Blizzard going down.
				new_grid[y % height + 1][x] += 1 << 3
	return new_grid

# Pre-simulate all stages in the blizzards cycle.
for i in range(1, cycle):
	grids.append(step(grids[-1]))

startx = 0
starty = 0
endx = width -1
endy = height + 1
def estimate(x, y, tox, toy):
	"""
	Estimate the distance from a point to the destination of a journey.
	:param x: The X coordinate to estimate the distance from.
	:param y: The Y coordinate to estimate the distance from.
	:param tox: The X coordinate to estimate the distance to.
	:param toy: The Y coordinate to estimate the distance to.
	:return: The estimate distance to the destination.
	"""
	dx = tox - x
	dy = toy - y
	return math.sqrt(dx * dx + dy * dy)

def get_neighbours(x, y, t):
	"""
	Find which cells we could move to from a given position.
	:param x: The X coordinate of the current position.
	:param y: The Y coordinate of the current position.
	:param t: The time frame of the current position.
	:return: A sequence of tuples of X,Y coordinates to which we could move from here.
	"""
	nextt = (t + 1) % cycle
	if grids[nextt][y][x] == 0:
		yield x, y  # We could stand still.
	if x < width - 1 and grids[nextt][y][x + 1] == 0:
		yield x + 1, y  # We could move right.
	if y > 0 and grids[nextt][y - 1][x] == 0:
		yield x, y - 1  # We could move up.
	if x > 0 and grids[nextt][y][x - 1] == 0:
		yield x - 1, y  # We could move left.
	if y < height + 1 and grids[nextt][y + 1][x] == 0:
		yield x, y + 1  # We could move down.

# Now find the shortest path to the exit using A*.
def astar(fromx, fromy, fromt, tox, toy):
	# Set-up state.
	open = queue.PriorityQueue()  # Queue of coordinates yet to be processed. Each coordinate is a tuple of (estimate, x, y, t)
	open.put((estimate(fromx, fromy, tox, toy), fromx, fromy, fromt))  # Start position on T=0.
	open_set = {(fromx, fromy, fromt)}
	to_start = [[[float("inf") for _ in grids[0][0]] for _ in grids[0]] for _ in grids]
	to_start[fromt][fromy][fromx] = 0
	total_dist = [[[float("inf") for _ in grids[0][0]] for _ in grids[0]] for _ in grids]
	total_dist[fromt][fromy][fromx] = estimate(fromx, fromy, tox, toy)

	while open_set:
		_, x, y, t = open.get()
		open_set.remove((x, y, t))

		if x == tox and y == toy:
			# Found the shortest path! T is now the time it took.
			return t

		while len(to_start) <= t + 1:
			to_start.append([[float("inf") for _ in grids[0][0]] for _ in grids[0]])
			total_dist.append([[float("inf") for _ in grids[0][0]] for _ in grids[0]])

		for neighbourx, neighboury in get_neighbours(x, y, t):
			dist_so_far = to_start[t][y][x] + 1
			if dist_so_far < to_start[t + 1][neighboury][neighbourx]:  # Better approached from this direction.
				to_start[t + 1][neighboury][neighbourx] = dist_so_far
				total_dist[t + 1][neighboury][neighbourx] = dist_so_far + estimate(neighbourx, neighboury, tox, toy)
				if (x, y, t) not in open_set:
					open.put((total_dist[t + 1][neighboury][neighbourx], neighbourx, neighboury, t + 1))
					open_set.add((neighbourx, neighboury, t + 1))
	raise Exception("Could not find a route!")

leg1 = astar(startx, starty, 0, endx, endy)
leg2 = astar(endx, endy, 228, startx, starty)
leg3 = astar(startx, starty, leg2, endx, endy)

print("The shortest path there, back and there again takes this amount of time:", leg3)