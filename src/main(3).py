import Eva
import datetime
from API_Connect import connection

# operator's API key and id here
cnt = connection("d15a0d0bd9e4a437a749", "693")
import multiprocessing
import os
import time
import hashlib
# import Eva2
SEARCH_RANGE = 1




# CPU_number=1
CPU_number = multiprocessing.cpu_count()


#	ATTENTION:
#		NEED TO ADD:
#			funciton to generate all possible next step: all_possible_next_Step(checked)
#			EVALUATE_FUNCTION: function to compute value at leaf nodes.(checked)
#			record the best move(checked)


class Node:
    # initialize node
    #	child: initialize to empty list
    #	flag: as an indicator for which side is playing at this node(-1 for Enemy, 1 for Self, 0 for leaf)
    #	parent: pointer of the parent node
    #	depth: the depth of in the tree
    #	brd: the board map
    #	value: heuristic of current node
    def __init__(self, side, parent_Node, depthC, brd_Str, alpha1, beta1, size):
        self.child = []
        self.flag = side
        self.parent = parent_Node
        self.depth = depthC
        self.brd = brd_Str
        self.value = 0
        self.alpha = alpha1
        self.beta = beta1
        self.size = size

    #   generate board string based on current brd
    def gen_BrdString(self):
        res = []
        lines = "-" * self.size
        for i in range(0, self.size):
            res.append(lines)
        for nodes in self.brd:
            node = nodes[0]
            x = node[0]
            y = node[1]
            tmp = list(res[x])
            tmp[y] = nodes[1]
            tmp = "".join(tmp)
            res[x] = tmp
        res1 = ""
        for r in res:
            res1 += r + "\n"
        return res1

    #   find all possible next steps based on the search range
    def findSteps(self):
        
        if (self.brd ==[]):
            # initial state
            return {(self.size / 2, self.size / 2)}
        board_dic={}
        for each in self.brd:
            board_dic[each[0]]=each[1]
        else:
            dots =set()
            priority_dot_set=set()
            for coor in self.brd:
                x = coor[0][0]
                y = coor[0][1]
                dots.discard((x, y))
                lowx = x - SEARCH_RANGE
                highx = x + SEARCH_RANGE + 1
                lowy = y - SEARCH_RANGE
                highy = y + SEARCH_RANGE + 1
                if (lowx < 0):
                    lowx = 0
                if (lowy < 0):
                    lowy = 0
                if (highx > self.size):
                    highx = self.size
                if (highy > self.size):
                    highy = self.size
                for i in range(lowx, highx):
                    for j in range(lowy, highy):
                        new_dot=(i,j)
                        non_important=1
                        count_X=0
                        count_O=0
                        for direction1 in[-1,0,1]:
                            for direction2 in [-1,0,1]:
                                if (i+direction1,j+direction2) in board_dic:
                                    if(board_dic[(i+direction1,j+direction2)]=="X"):
                                        count_X=count_X+1
                                    if(board_dic[(i+direction1,j+direction2)]=="O"):
                                        count_O=count_O+1
                        if(count_O>=2 or count_X>=2):
                            non_important=0
                        stop=0
                        for direction1 in[-1,0,1]:
                            if(stop==1):
                                break
                            for direction2 in [-1,0,1]:
                                dot1=(i+direction1,j+direction2)
                                dot2=(i+direction1*2,j+direction2*2)
                                if(dot1 in board_dic and dot2 in board_dic):
                                    if(board_dic[dot1]==board_dic[dot2]):
                                        non_important=0
                                        stop=1
                                        break
                        if(non_important==1):
                            dots.add(new_dot)
                        else:
                            priority_dot_set.add(new_dot)
                    
                            #                      for each_side in ['X','O']:
                            #                if(i-1>=0):
 
            for coor in self.brd:
                x = coor[0][0]
                y = coor[0][1]
                dots.discard((x, y))
                priority_dot_set.discard((x, y))
            result=list(priority_dot_set)
            result.extend(list(dots))
            
            return result


    #   generate the search tree based on max depth
    def gen_Succ(self, task, result, hash_board_value,TARGET,Max_score,myself,MAX_DEP):
        global CPU_number
        tmp_max_node = None
        if (self.depth != MAX_DEP):
            # havent reach max depth, continue generating
            # check alpha beta
            if (self.flag == 0):
                #	leaf node, do nothing
                print("")
            elif (self.flag == 1):
                #	our turn, find max child, update alpha
                # generate children
                max = float("-inf")
                
                for brd in task:
                    # generate new brd map
                    # find side symbol
                    side_str = "X"
                    if myself == side_str:
                        side_str = "X"
                    else:
                        side_str = "O"
                    # create tuple
                    tmp_tuple = (brd, side_str)
                    tmp_brd = self.brd.copy()
                    tmp_brd.append(tmp_tuple)
                    tmp_Node = Node(0 - self.flag, self, self.depth + 1, tmp_brd, self.alpha, self.beta, self.size)
                    next_task = tmp_Node.findSteps()
                    board_str = tmp_Node.gen_BrdString()
                    hash_value=hashlib.md5(board_str.encode(encoding='utf-8')).hexdigest()
                    
                    if (hash_value in hash_board_value):
                        tmp_Score = hash_board_value[hash_value]

                    else:
                        tmp_Score = Eva.calculate_board_value(tmp_Node.gen_BrdString(), TARGET, myself)
                        hash_board_value[hash_value] = tmp_Score
                    if (self.depth != MAX_DEP - 1 and tmp_Score < Max_score):
                        # generate child's child(if possible)
                        tmp_Node.gen_Succ(next_task, result, hash_board_value,TARGET,Max_score,myself,MAX_DEP)
                    else:
                        # mark as leaf node and calculate value
                        tmp_Node.flag = 0
                        tmp_Node.value = tmp_Score
                        # tmp_Node.value = 1
                    self.child.append(tmp_Node)
                    if (tmp_Node.value > self.alpha):
                        # update alpha
                        self.alpha = tmp_Node.value
                    if tmp_Node.value > max:
                        max = tmp_Node.value
                        tmp_max_node = tmp_Node
                    if (self.alpha >= self.beta):
                        # prune
                        max = self.alpha
                        break

                self.value = max
                if (self.depth == 0):
                    result.append((self.value, tmp_max_node))



            else:
                #	enemy turn, find min child, update beta
                # generate children
                min = float("inf")

                for brd in task:
                    side_str = "O"
                    if myself == side_str:
                        side_str = "X"
                    # create tuple
                    tmp_tuple = (brd, side_str)
                    tmp_brd = self.brd.copy()
                    tmp_brd.append(tmp_tuple)
                    tmp_Node = Node(0 - self.flag, self, self.depth + 1, tmp_brd, self.alpha, self.beta, self.size)
                    next_task = tmp_Node.findSteps()
                    board_str = tmp_Node.gen_BrdString()
                    hash_value=hashlib.md5(board_str.encode(encoding='utf-8')).hexdigest()
                    
                    if (hash_value in hash_board_value):
                        tmp_Score = hash_board_value[hash_value]
            
                    else:
                        tmp_Score = Eva.calculate_board_value(board_str, TARGET, myself)
                        hash_board_value[hash_value] = tmp_Score
                    if (self.depth != MAX_DEP - 1 and tmp_Score > -Max_score):
                        # generate child's child(if possible)
                        tmp_Node.gen_Succ(next_task, result, hash_board_value,TARGET,Max_score,myself,MAX_DEP)
                    else:
                        # mark as leaf node and calculate value
                        tmp_Node.flag = 0
                        tmp_Node.value = tmp_Score
                        # tmp_Node.value = 1
                    self.child.append(tmp_Node)
                    if (tmp_Node.value < self.beta):
                        # update beta
                        self.beta = tmp_Node.value
                    if tmp_Node.value < min:
                        min = tmp_Node.value
                    if (self.alpha >= self.beta):
                        # prune
                        min = self.beta
                        break
                self.value = min

    # return the next optimal move calculated by agent
    def get_Next_Step(self, hash_board_value,TARGET,Max_score,myself,MAX_DEP):
        this_value = Eva.calculate_board_value(self.gen_BrdString(), TARGET, myself)
        all_possible_next_Step = self.findSteps()
        if (this_value == Max_score or this_value == -Max_score or all_possible_next_Step == []):
            return self
        for brd in all_possible_next_Step:
            # generate new brd map
            # find side symbol
            side_str = "X"
            if myself == side_str:
                side_str = "X"
            else:
                side_str = "O"
            # create tuple
            tmp_tuple = (brd, side_str)
            tmp_brd = self.brd.copy()
            tmp_brd.append(tmp_tuple)
            tmp_Node = Node(0 - self.flag, self, self.depth + 1, tmp_brd, self.alpha, self.beta, self.size)
            self.child.append(tmp_Node)
            score = Eva.calculate_board_value(tmp_Node.gen_BrdString(), TARGET, myself)
            if (score >= Max_score):
                return tmp_Node

        if (len(all_possible_next_Step) > CPU_number - 1):
            process_number = max(CPU_number - 1, 1)
        else:
            process_number = max(len(all_possible_next_Step),1)
    
        task_length = len(all_possible_next_Step) // process_number
        process_list = []
        processes_result = multiprocessing.Manager().list()

        for i in range(process_number):
            if (i != process_number - 1):
                task = all_possible_next_Step[i * task_length:(i + 1) * task_length]
            else:
                task = all_possible_next_Step[i * task_length:]

            p = multiprocessing.Process(target=self.gen_Succ, args=(task, processes_result, hash_board_value,TARGET,Max_score,myself,MAX_DEP))
            process_list.append(p)
            p.start()

        for p in process_list:
            p.join()

        choice = self
        max_value = -float('inf')

        for each in processes_result:

            if (each[0] > max_value):
                max_value = each[0]
                choice = each[1]

        return choice


# Testing function for printing number of nodes expanded
def countNod(nd):
    if len(nd.child) != 0:
        total = 0
        for nds in nd.child:
            total += countNod(nds)
        return total
    else:
        return 1


# return the boardmap based on the gameId
def getBRD(gameId):
    global cnt
    B_map = cnt.get_board_map(gameId)['output']
    if B_map is None:
        return []
    else:
        B_map = B_map[1:len(B_map) - 1]
        ndeList = B_map.split(',')
        totalList = []
        for i in range(0, len(ndeList), 2):
            left = ndeList[i]
            right = ndeList[i + 1]
            x = left[1:len(left)]
            tmpList = right.split('"')
            y = tmpList[0]
            sign = tmpList[2]
            tpl = (int(x), int(y))
            tpl = (tpl, sign)
            totalList.append(tpl)
        return totalList


# let the agent make the choice of next move
def respond(gameId, sizeA, targ, playerId, hash_board_value,TARGET,Max_score,myself,MAX_DEP):
    # global search_Time
    # #timer
    # search_Time = datetime.datetime.now()
    
    TARGET = targ
    score = 0
    nowBrd = getBRD(gameId)
    tmpN = Node(1, None, 0, nowBrd, float("-inf"), float("inf"), sizeA)
    tmp_Score = Eva.calculate_board_value(tmpN.gen_BrdString(), TARGET, myself)
    if (tmp_Score == Max_score):
        print()
        return Max_score
    else:
        next_Step = tmpN.get_Next_Step(hash_board_value,TARGET,Max_score,myself,MAX_DEP)
        if (next_Step is None) or (len(next_Step.brd) == 0):
            next_Step = ((int(sizeA / 2), int(sizeA / 2)), myself)
            score = 0
        else:
            score = Eva.calculate_board_value(next_Step.gen_BrdString(), TARGET, myself)
            next_Step = next_Step.brd[-1]
        print(cnt.make_move(playerId, next_Step[0][0], next_Step[0][1], gameId))
        return score


# select side based on the board map
#   alternating myself and FIRST_HAND
def choose_Side(brd):
    # O is first hand
    count = 0
    for pie in brd:
        side = pie[1]
        if side == 'X':
            count += 1
        else:
            count -= 1
    if count >= 0:
        # our turn, we are first hand, O
        myself = 'O'
        FIRST_HAND = True
        return ('O',True)
    else:
        # our turn, we are not first hand, X
        myself = 'X'
        FIRST_HAND = False
        return ('X',False)

# print the board map with labels, based on the board string
def print_board_str(str):
    maplist = str.split('\n')

    maplist = maplist[:-1]

    header = " "

    le = len(maplist)

    for i in range(0, le):

        lt = list(maplist[i])

        for j in range(0, len(lt)):
            lt[j] = '   ' + lt[j]

        maplist[i] = "".join(lt)

        le1 = len(i.__str__())

        for j in range(0, 4 - le1):
            header += " "

        maplist[i] = i.__str__() + maplist[i]

        header = header + i.__str__()

    res = []

    res = [header]

    res.extend(maplist)

    for lines in res:
        print(lines)


# testing main
def maintest1():
    TARGE=5
    Max_score=625
    myself='O'
    MAX_DEP=4
    hash_board_value = multiprocessing.Manager().dict()
    #   testing
    a = [((6, 2), 'O'), ((1, 3), 'X'), ((0, 2), 'O'), ((2, 4), 'X'), ((0, 4), 'O'), ((3, 5), 'X')]
    myself=choose_Side(a)
    tmpN = Node(1, None, 0, a, float("-inf"), float("inf"), 8)
    # tmpN.gen_Succ()
    print('hello')
    start_time = datetime.datetime.now()
    next_Step = tmpN.get_Next_Step(hash_board_value)
    end_time = datetime.datetime.now()
    print((end_time - start_time))
    print(next_Step.brd)
    # for ele in tmpN.child:
    #    for a1 in ele.child:
    #        print(a1.brd)
    map = [["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "], ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "],
           ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "], ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "],
           ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "], ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "],
           ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "], ["* ", "* ", "* ", "* ", "* ", "* ", "* ", "* "]]
    # print(tmpN.child[5].brd)
    for ele in next_Step.brd:
        coor = ele[0]
        x = coor[0]
        y = coor[1]
        map[x][y] = ele[1] + " "
    for i in range(0, 8):
        for j in range(0, 8):
            print(map[i][j], end="")
        print()


# Testing main
def maintest2():
    a = [((1, 3), 'X'), ((0, 2), 'O'), ((2, 4), 'X'), ((0, 4), 'O'), ((3, 5), 'X'), ((0, 3), 'O')]
    print(choose_Side(a))


def main():

    MAX_DEP=4
    FIRST_HAND = True
    TARGET = 6
    Max_score = TARGET ** (TARGET - 1)
    myself = "O"
    
    hash_board_value = multiprocessing.Manager().dict()
    write_to_file = 1
    already_record = set()
    option = input("Select mode: 1.PVE 2.EVE: ")
    if option == '1':
        # PVE mode
        human_oppo_piece = ''
        score = 0
        sz = eval(input("Enter game size: "))

        TARGET = int(input("Enter game target: "))
        Max_score = TARGET ** (TARGET - 1)
        oppo_first = eval(input("Input 0 to let you drop piece first, input 1 to let AI drop piece first："))
        print("Wait,the game is being initialized; it may take up to 30 seconds")
        files_list = os.listdir()
        file_name = "training_data" + "_" + str(sz) + "_" + str(TARGET) + ".txt"
        # find if there is already training data saved for this situation, if there is, read the training data
        if (file_name in files_list):
            t1 = time.time()
            buffer = open(file_name, 'r')
            while (True):
                if (time.time() - t1 > 30):
                    write_to_file = 0
                    break
                data = buffer.readline()
                if (data == ""):
                    break
                data = data.strip().split()
                hash_board_value[data[0]] = float(data[1])
                already_record.add(data[0])
            buffer.close()
        if (oppo_first == 0):
            FIRST_HAND = False
            myself = 'X'
            human_oppo_piece = 'O'
        else:
            FIRST_HAND = True
            myself = 'O'
            human_oppo_piece = 'X'

        board = []
        board_step_map = []
        for i in range(sz):
            board.append(['-'] * sz)

        print("This is the board")
        board_str = ''
        for i in board:

            for j in i:
                board_str = board_str + str(j)

            board_str = board_str + '\n'
        print_board_str(board_str)
        # if this AI plays first, then it drops piece at the middle, if it's one target, directly return AI wins
        if (FIRST_HAND == True):
            board[int(sz / 2)][int(sz / 2)] = myself
            board_step_map.append(((int(sz / 2), int(sz / 2)), myself))
            print("This is AI's move")
            print("AI drops pieces at x:", int(sz / 2), "y:", int(sz / 2))
            board_str = ''
            for i in board:

                for j in i:
                    board_str = board_str + str(j)

                board_str = board_str + '\n'
            print_board_str(board_str)
            if (TARGET == 1):
                print("AI wins,game over")
                return

        while (True):
            # player's move
            while (True):
                x = eval(input("Enter x: "))
                y = eval(input("Enter y: "))
                if (x < 0 or x >= sz or y < 0 or y >= sz or board[x][y] != '-'):
                    print("Invalid drop,try again")
                else:
                    break
            board[x][y] = human_oppo_piece
            board_step_map.append(((x, y), human_oppo_piece))
            print("This is your move")
            # generate board string
            board_str = ''
            for i in board:

                for j in i:
                    board_str = board_str + str(j)

                board_str = board_str + '\n'
            print_board_str(board_str)
            print("\n")
            score = Eva.calculate_board_value(board_str, TARGET, myself)
            if (score == Max_score or score == -Max_score or '-' not in board_str):
                break
            # this AI's move
            print("CPU is thinking...")
            time1 = time.time()
            tmpN = Node(1, None, 0, board_step_map, float('-inf'), float('inf'), sz)
            next_step = tmpN.get_Next_Step(hash_board_value,TARGET,Max_score,myself,MAX_DEP)
            score = Eva.calculate_board_value(tmpN.gen_BrdString(), TARGET, myself)
            next_step = next_step.brd[-1]
            board[next_step[0][0]][next_step[0][1]] = myself
            board_step_map.append(((next_step[0][0], next_step[0][1]), myself))
            print("This is AI's move")
            print("The search depth is:", MAX_DEP + 1)
            time_diff=time.time() - time1
            if (time_diff> 20):  # adjust search depth dynamically according to computer running time
                MAX_DEP = max(MAX_DEP - 1, 3)

            if (time_diff< 3):
                MAX_DEP = min(MAX_DEP + 1, 6)

            print("AI drops pieces at x:", next_step[0][0], "y:", next_step[0][1])
            # generate board string
            board_str = ''
            for i in board:

                for j in i:
                    board_str = board_str + str(j)

                board_str = board_str + '\n'
            print_board_str(board_str)
            score = Eva.calculate_board_value(board_str, TARGET, myself)
            print("\n")
            if (score == Max_score or score == -Max_score or '-' not in board_str):
                break
        print("End of game")
        if (score >= Max_score):
            print("AI Wins")
        else:
            print("Congratulations, you win")
        print("The programming is saving the training data, please don't kill the program; it may take up to 30 seconds")
        # saving the training data
        if (write_to_file == 1):
            buffer = open(file_name, 'a')
            time1 = time.time()
            for all_hash in hash_board_value:
                if (time.time() - time1 > 30):  # if training data is too large to be saved,the program just runs for 30 seconds
                    break
                if (all_hash not in already_record):
                    buffer.write(all_hash + " " + str(hash_board_value[all_hash]) + "\n")
            buffer.close()


    else:
        # EVE
        # EVE
        signal = input("Enter 1 if there is an existing game. 2 if otherwise.")
        if signal == '1':
            gid = input("Enter game id")
            sz = int(input("Enter game size"))
            tgt = int(input("Enter game target"))
        else:
            team1 = input("Enter first team's Id")
            team2 = input("Enter second team's Id")
            sz = int(input("Enter game size"))
            tgt = int(input("Enter game target"))
            gid = cnt.create_game(team1, team2, sz, tgt)['gameId']
            print(gid)
        TARGET=tgt
        Max_score = TARGET ** (TARGET - 1)
        files_list = os.listdir()
        file_name = "training_data" + "_" + str(sz) + "_" + str(tgt) + ".txt"
        # find if there is already training data saved for this situation, if there is, read the training data
        print("Wait,the game is being initialized; it may take up to 30 seconds")
        if (file_name in files_list):
            t1 = time.time()
            buffer = open(file_name, 'r')
            while (True):
                if (time.time() - t1 > 30):
                    write_to_file = 0
                    break
                data = buffer.readline()
                if (data == ""):
                    break
                data = data.strip().split()
                hash_board_value[data[0]] = float(data[1])
                already_record.add(data[0])
            buffer.close()
        empty = input("Press Enter to proceed.")
        (myself,FIRST_HAND)=choose_Side(getBRD(gid))
        signal2 = input("Is this our turn now? 1 for yes 2 for no")
        if signal2 == "2":
            if myself == 'O':
                myself = 'X'
            else:
                myself = 'O'
            FIRST_HAND = not FIRST_HAND
        score=0
        while (True):
            if (cnt.get_move_list(gid, 6)['code'] == 'FAIL' and myself == 'O') or (
                    cnt.get_move_list(gid, 6)['code'] != 'FAIL' and (
            not (cnt.get_move_list(gid, 6)['moves'][0]['symbol'] == myself))):
                print("Opponent's move detected, proceeding to next step...")
                print("CPU is thinking...")
                time1=time.time()
                score = respond(gid, sz, tgt, 1112, hash_board_value,TARGET,Max_score,myself,MAX_DEP)
                print("The search depth is:", MAX_DEP + 1)
                time_diff=time.time() - time1
                if (time_diff> 20):  # adjust search depth dynamically according to computer running time
                    MAX_DEP = max(MAX_DEP - 1, 4)
            
                if (time_diff< 3):
                    MAX_DEP = min(MAX_DEP + 1, 4)
                print_board_str(cnt.get_board_string(gid)['output'])
                print("\n")
                print("\n")
                print("\n")
                print("\n")
            if (score == Max_score or score == -Max_score or len(getBRD(gid))>=sz*sz):
                break
        print("End of game")
        if (score < Max_score):
            print("AI Wins")
        else:
            print("Congratulations, you win")
        # saving the training data
        print("The programming is saving the training data, please don't kill the program; it may take up to 30 seconds")
        if (write_to_file == 1):
            buffer = open(file_name, 'a')
            time1 = time.time()
            for all_hash in hash_board_value:
                if (time.time() - time1 > 30):  # if training data is too large to be saved,the program just runs for 30 seconds
                    break
                if (all_hash not in already_record):
                    buffer.write(all_hash + " " + str(hash_board_value[all_hash]) + "\n")
            buffer.close()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
