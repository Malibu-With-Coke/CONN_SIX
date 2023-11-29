'''
	The CONNSIX package should be located where this dummy_ai.py is located. 
	dummy_ai.py is an example to demonstrate the usage of CONNSIX package. Since 
	it is an example, dummy_ai.py may produce invalid input. Once it receives the
	return value from server, the message is printed to the console for checking 
	results. 

'''
import sys
sys.path.append('../') # add the path to the package CONNSIX
from CONNSIX import connsix
import random 

OPPONENT_COLOR = "W"
COLOR = "B"
NULL_POINT = -9

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
			print(f'count: {count}, both_ends: {both_ends}')
			return both_ends
	
	return [(NULL_POINT, NULL_POINT), (NULL_POINT, NULL_POINT)]




def make_move(pro_move):
	provious_moves = pro_move.split(":")
	provious_move1 = connsix._a_coor_to_num(provious_moves[0])
	if provious_move1 == "BADINPUT":
		exit()
	
	provious_move2 = connsix._a_coor_to_num(provious_moves[1])
	
	next_move = find_con_4stone(provious_move1)
	if next_move[0][0] != NULL_POINT:	# if there is a con 4 or 5 stone
		if not (check_in_the_board((next_move[0][0], next_move[0][1])) and connsix.get_stone_at_num((next_move[0][0], next_move[0][1])) == 'E'):
			next_move[0] = make_random_move()
		if not (check_in_the_board((next_move[1][0], next_move[1][1])) and connsix.get_stone_at_num((next_move[1][0], next_move[1][1])) == 'E'):
			next_move[1] = make_random_move()
		
		return connsix._num_to_a_coor(next_move[0]) + ":" + connsix._num_to_a_coor(next_move[1])
	
	next_move = find_con_4stone(provious_move2)
	if next_move[0][0] != NULL_POINT:  # if there is a con 4 or 5 stone
		if not (check_in_the_board((next_move[0][0], next_move[0][1])) and connsix.get_stone_at_num((next_move[0][0], next_move[0][1])) == 'E'):
			next_move[0] = make_random_move()
		if not (check_in_the_board((next_move[1][0], next_move[1][1])) and connsix.get_stone_at_num((next_move[1][0], next_move[1][1])) == 'E'):
			next_move[1] = make_random_move()
		
		return connsix._num_to_a_coor(next_move[0]) + ":" + connsix._num_to_a_coor(next_move[1])


	return connsix._num_to_a_coor(make_random_move()) + ":" + connsix._num_to_a_coor(make_random_move())

def main():
	# ip = input("input ip: ")
	ip = '127.0.0.1'
	# port = int(input("input port number: "))
	port = 9190
	# dummy_home = input("input BLACK or WHITE: ")
	dummy_home = "WHITE"

	global COLOR
	global OPPONENT_COLOR

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
		away_move = connsix.draw_and_read("K11:L11")
		print("Received first away move from server: " + away_move)
	
	pro_move = away_move

	while 1:
		away_move = connsix.draw_and_read(make_move(pro_move))
		print("Received away move from server: " + away_move)
		pro_move = away_move


if __name__ == "__main__":
	main()
