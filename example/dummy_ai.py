'''
	The CONNSIX package should be located where this dummy_ai.py is located. 
	dummy_ai.py is an example to demonstrate the usage of CONNSIX package. Since 
	it is an example, dummy_ai.py may produce invalid input. Once it receives the
	return value from server, the message is printed to the console for checking 
	results. 

'''
import sys
sys.path.append("..")
sys.path.append("../CONNSIX")
from CONNSIX import connsix
import random
import time

OPPONENT_COLOR = ""
COLOR = ""
NULL_POINT = -9
SCORES = [[0 for i in range(19)] for j in range(19)]

# if opponent's move is in the board, return True
def check_in_the_board(point):
	if point[0] >= 0 and point[0] <= 18 and point[1] >= 0 and point[1] <= 18:
		return True
	else:
		return False


def make_random_move():
	while True:
		x = random.randint(0, 18)
		y = random.randint(0, 18)

		if connsix.get_stone_at_num((x, y)) == 'E':
			return (x, y)



def find_con_4stone(point):
	directions = [[(0, 1), (0, -1)], [(1, 0), (-1, 0)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)]]

	for direction in directions:
		count = 1
		both_ends = [point, point]

		for i in range(2):
			mul = 1
			while True:
				x = point[0] + direction[i][0] * mul
				y = point[1] + direction[i][1] * mul

				both_ends[i] = (x, y)
				
				if check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == OPPONENT_COLOR:
					count += 1
					mul += 1

				else:	
					break
		
		if count >= 4:
			for end in both_ends:
				if check_in_the_board(end) and connsix.get_stone_at_num(end) == 'E':
					SCORES[end[0]][end[1]] = 1e4

def find_sep_4stone(point):
	directions = [[(0, 1), (0, -1)], [(1, 0), (-1, 0)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)]]

	for direction in directions:

		for i in range(6):
			if not check_in_the_board((point[0] + direction[0][0] * i, point[1] + direction[0][1] * i)) \
			and not check_in_the_board((point[0] + direction[1][0] * (5 - i), point[1] + direction[1][1] * (5 - i))):
				continue
			
			count = 1
			blank_point = (NULL_POINT, NULL_POINT)
			blank_count = 0
			for j in range(6):
				x = point[0] + direction[1][0] * (5 - i) + direction[0][0] * j
				y = point[1] + direction[1][1] * (5 - i) + direction[0][1] * j
				if check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == 'E':
					blank_count += 1
				elif check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == OPPONENT_COLOR:
					count += 1
					continue
				else:
					break

				if blank_count:
					blank_point = (x, y)
		
			if count >= 4 and blank_count:
				SCORES[blank_point[0]][blank_point[1]] = 1e6

def invalid_area_for_find_sep_4stone(point1, point2):
	if not check_in_the_board(point1) or not check_in_the_board(point2):
		return True
	
	if connsix.get_stone_at_num(point1) != OPPONENT_COLOR or connsix.get_stone_at_num(point2) != OPPONENT_COLOR: 
		return True
	
	return False
	
def find_sep_4stone_scenario(point):
	directions = [[(0, 1), (0, -1)], [(1, 0), (-1, 0)], [(1, 1), (-1, -1)], [(1, -1), (-1, 1)]]

	# CASE1: BLANK * 1 + OPPONENT * 4
	for direction in directions:
		positive_direction = direction[0]
		negative_direction = direction[1]

		for i in range(5):
			if invalid_area_for_find_sep_4stone((point[0] + negative_direction[0] * (4 - i), point[1] + negative_direction[1] * (4 - i)), \
			(point[0] + positive_direction[0] * i, point[1] + positive_direction[1] * i)):
				continue

			opponent_count = 0
			blank_count = 0
			blank_point = (NULL_POINT, NULL_POINT)
			for j in range(5):
				x = point[0] + negative_direction[0] * (4 - i) + positive_direction[0] * j
				y = point[1] + negative_direction[1] * (4 - i) + positive_direction[1] * j
				if check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == 'E':
					blank_count += 1
					blank_point = (x, y)
				elif check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == OPPONENT_COLOR:
					opponent_count += 1
				else:
					break

			if opponent_count == 4 and blank_count == 1:
				print(blank_point)
				SCORES[blank_point[0]][blank_point[1]] = 1e6

	# CASE2: BLANK * 1 + OPPONENT * 4
	# 의미가 있는지는 모르겠다...
	for direction in directions:
		positive_direction = direction[0]
		negative_direction = direction[1]

		for i in range(6):
			if invalid_area_for_find_sep_4stone((point[0] + negative_direction[0] * (5 - i), point[1] + negative_direction[1] * (5 - i)), \
			(point[0] + positive_direction[0] * i, point[1] + positive_direction[1] * i)):
				continue

			opponent_count = 0
			blank_count = 0
			blank_point = (NULL_POINT, NULL_POINT)
			for j in range(6):
				x = point[0] + negative_direction[0] * (5 - i) + positive_direction[0] * j
				y = point[1] + negative_direction[1] * (5 - i) + positive_direction[1] * j
				if check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == 'E':
					blank_count += 1
					blank_point = (x, y)
				elif check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == OPPONENT_COLOR:
					opponent_count += 1
				else:
					break

			if opponent_count == 5 and blank_count == 1:
				print(blank_point)
				SCORES[blank_point[0]][blank_point[1]] = 1e6

	# CASE3: BLANK * 2 + OPPONENT * 4
	for direction in directions:
		positive_direction = direction[0]
		negative_direction = direction[1]

		for i in range(6):
			if invalid_area_for_find_sep_4stone((point[0] + negative_direction[0] * (5 - i), point[1] + negative_direction[1] * (5 - i)), \
			(point[0] + positive_direction[0] * i, point[1] + positive_direction[1] * i)):
				continue

			opponent_count = 0
			blank_count = 0
			order = []
			blank_point = []
			for j in range(6):
				x = point[0] + negative_direction[0] * (5 - i) + positive_direction[0] * j
				y = point[1] + negative_direction[1] * (5 - i) + positive_direction[1] * j
				if check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == 'E':
					blank_count += 1
					blank_point.append((x, y))
					order.append(0)
				elif check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == OPPONENT_COLOR:
					opponent_count += 1
					order.append(1)
				else:
					break

			if opponent_count == 4 and blank_count == 2:
				if order == [1, 0, 0, 1, 1, 1]:
					print(blank_point[0])
					SCORES[blank_point[0][0]][blank_point[0][1]] = 1e6
				elif order == [1, 0, 1, 0, 1, 1]:
					print(blank_point[1])
					SCORES[blank_point[1][0]][blank_point[1][1]] = 1e6
				elif order == [1, 0, 1, 1, 0, 1]:
					print(blank_point[2])
					SCORES[blank_point[2][0]][blank_point[2][1]] = 1e6
				elif order == [1, 1, 0, 0, 1, 1]:
					print(blank_point[3])
					SCORES[blank_point[3][0]][blank_point[3][1]] = 1e6
				elif order == [1, 1, 0, 1, 0, 1]:
					print(blank_point[4])
					SCORES[blank_point[4][0]][blank_point[4][1]] = 1e6
				elif order == [1, 1, 1, 0, 0, 1]:
					print(blank_point[5])
					SCORES[blank_point[5][0]][blank_point[5][1]] = 1e6
				# print(blank_point)
				# SCORES[blank_point[0]][blank_point[1]] = 1e6

	# CASE4: BLANK * 2 + OPPONENT * 5
	for direction in directions:
		positive_direction = direction[0]
		negative_direction = direction[1]

		for i in range(7):
			if invalid_area_for_find_sep_4stone((point[0] + negative_direction[0] * (6 - i), point[1] + negative_direction[1] * (6 - i)), \
			(point[0] + positive_direction[0] * i, point[1] + positive_direction[1] * i)):
				continue

			opponent_count = 0
			blank_count = 0
			order = []
			blank_point = []
			for j in range(7):
				x = point[0] + negative_direction[0] * (6 - i) + positive_direction[0] * j
				y = point[1] + negative_direction[1] * (6 - i) + positive_direction[1] * j
				if check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == 'E':
					blank_count += 1
					blank_point.append((x, y))
					order.append(0)
				elif check_in_the_board((x, y)) and connsix.get_stone_at_num((x, y)) == OPPONENT_COLOR:
					opponent_count += 1
					order.append(1)
				else:
					break

			if opponent_count == 5 and blank_count == 2:
				print(order)
				if order == [1, 0, 0, 1, 1, 1, 1]: # 1
					print(blank_point[0])
					SCORES[blank_point[0][0]][blank_point[0][1]] = 0
					SCORES[blank_point[1][0]][blank_point[1][1]] = 1e6
					
					print(SCORES[blank_point[0][0]][blank_point[0][1]])
					print(SCORES[blank_point[1][0]][blank_point[1][1]])
				elif order == [1, 0, 1, 0, 1, 1, 1]: # 2
					print(blank_point[1])
					SCORES[blank_point[1][0]][blank_point[1][1]] = 1e6
				elif order == [1, 0, 1, 1, 0, 1, 1]: # 3
					print(blank_point[2])
					SCORES[blank_point[2][0]][blank_point[2][1]] = 1e6
				elif order == [1, 0, 1, 1, 1, 0, 1]: # 4
					print(blank_point[3])
					SCORES[blank_point[3][0]][blank_point[3][1]] = 1e6
				elif order == [1, 1, 0, 0, 1, 1, 1]: # 5
					print(blank_point[4])
					SCORES[blank_point[4][0]][blank_point[4][1]] = 1e6
				elif order == [1, 1, 0, 1, 0, 1, 1]: # 6
					print(blank_point[5])
					SCORES[blank_point[5][0]][blank_point[5][1]] = 1e6
				elif order == [1, 1, 0, 1, 1, 0, 1]: # 7
					print(blank_point[6])
					SCORES[blank_point[6][0]][blank_point[6][1]] = 1e6
				elif order == [1, 1, 1, 0, 0, 1, 1]: # 8
					print(blank_point[7])
					SCORES[blank_point[7][0]][blank_point[7][1]] = 1e6
				elif order == [1, 1, 1, 0, 1, 0, 1]: # 9
					print(blank_point[8])
					SCORES[blank_point[8][0]][blank_point[8][1]] = 1e6
				elif order == [1, 1, 1, 1, 0, 0, 1]: # 10
					print(blank_point[9])
					SCORES[blank_point[9][0]][blank_point[9][1]] = 1e6
				

def calculate_score_for_position(x, y):
   if not check_in_the_board((x, y)) or connsix.get_stone_at_num((x, y)) != 'E':
      return -1

   score = 0
   directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

   for dx, dy in directions:
      stones = []

      for i in range(1, 6):
         nx, ny = x - dx * i, y - dy * i
         if check_in_the_board((nx, ny)):
            stones.insert(0, connsix.get_stone_at_num((nx, ny)))
         else:
            stones.insert(0, None)

      stones.append(COLOR)

      for i in range(1, 6):
         nx, ny = x + dx * i, y + dy * i
         if check_in_the_board((nx, ny)):
            stones.append(connsix.get_stone_at_num((nx, ny)))
         else:
            stones.append(None)

      # pattern check
      for i in range(len(stones)-5):
         pattern6 = stones[i: i+6]
         if pattern6.count(COLOR) == 6:
            score += 1e5
         elif pattern6.count(COLOR) == 5 and pattern6.count('E') == 1:
            score += 1e4
         elif pattern6.count(COLOR) == 4 and pattern6.count('E') == 2:
            score += 1e2
         elif pattern6.count(COLOR) == 3 and pattern6.count('E') == 3:
            score += 1e1
         elif pattern6.count(COLOR) == 2 and pattern6.count('E') == 4:
            score += 1e0

   return score

def count_threats():
	count_of_threats = 0
	for x in range(19):
		for y in range(19):
			if SCORES[x][y] == 1e6:
				count_of_threats += 1
	
	return count_of_threats


def update_scores(pro_move):

	for x in range(19):
		for y in range(19):
			SCORES[x][y] = calculate_score_for_position(x, y)

	# opponent's 4 stone --> high scores
	provious_moves = pro_move.split(":")
	for move in provious_moves:
		coor = connsix._a_coor_to_num(move)
		if coor != "BADINPUT":
			find_con_4stone(coor)
			if count_threats() < 2:
				# find_sep_4stone(coor)
				find_sep_4stone_scenario(coor)



def find_best_move():
	max_score = -1
	best_move = (NULL_POINT, NULL_POINT)

	# board check
	# for x in range(19):
	# 	for y in range(19):
	# 		print(connsix._lcs_board[x][y], end = '\t')
	# 	print()
	# print()

	# # SCORES check
	# for x in range(19):
	# 	for y in range(19):
	# 		print(SCORES[x][y], end = '\t')
	# 	print()
	# print()

	for x in range(19):
		for y in range(19):
			if SCORES[x][y] > max_score and connsix.get_stone_at_num((x, y)) == 'E':
				max_score = SCORES[x][y]
				best_move = (x, y)
	return best_move



def make_move(pro_move):

	# scores 계산 -> 모든 방향으로 어떤 구조가 만들어지냐에 따라
	update_scores(pro_move)


	first_move = find_best_move()

	if first_move != (NULL_POINT, NULL_POINT):
		connsix._lcs_board[first_move[0]][first_move[1]] = 1 if COLOR == 'B' else 2

		update_scores(pro_move)
		second_move = find_best_move()

		connsix._lcs_board[first_move[0]][first_move[1]] = 0
	else:
		second_move = (NULL_POINT, NULL_POINT)

	if first_move == (NULL_POINT, NULL_POINT):
		first_move = make_random_move()
	if second_move == (NULL_POINT, NULL_POINT):
		second_move = make_random_move()

	return connsix._num_to_a_coor(first_move) + ":" + connsix._num_to_a_coor(second_move)


def first_move():
	from itertools import combinations
	first_move_list = []
	
	for i in ('J', 'K', 'L'):
		for j in range(9, 12):
			stone_place = i + str(j)
			if stone_place != "K10" and connsix.get_stone_at(stone_place) == 'E':
				first_move_list.append(stone_place)
	
	return_comb = list(combinations(first_move_list, 2))[0]


	return return_comb[0] + ":" + return_comb[1]


def main():
	# ip = input("input ip: ")
	ip = '127.0.0.1'
	# port = int(input("input port number: "))
	port = 9190
	# dummy_home = input("input BLACK or WHITE: ")
	dummy_home = "BLACK"
	# dummy_home = "WHITE"

	global COLOR
	global OPPONENT_COLOR
	global POINTS

	if dummy_home == "BLACK":
		COLOR = "B"
		OPPONENT_COLOR = "W"

	else:
		COLOR = "W"
		OPPONENT_COLOR = "B"

	red_stones = connsix.lets_connect(ip, port, dummy_home)
	if len(red_stones):	
		print("Received red stones from server: " + red_stones)

	if dummy_home == "BLACK":
		away_move = connsix.draw_and_read("K10")
		print("Received first away move from server: " + away_move)
	else:
		away_move = connsix.draw_and_read("")
		print("Received first away move from server: " + away_move)
		away_move = connsix.draw_and_read(first_move())
		print("Received second away move from server: " + away_move)
	
	pro_move = away_move

	while 1:
		away_move = connsix.draw_and_read(make_move(pro_move))
		print("Received away move from server: " + away_move)
		pro_move = away_move



if __name__ == "__main__":
	main()