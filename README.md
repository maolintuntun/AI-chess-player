# AI-chess-player
Wrap-up
1.	Implement Adversarial Search algorithm with python, guarantee 80% chance to win people. 

2.	Upgrade the performance using Multi Processing to shorten running time at least 2 times (control one step in 5s)

3.	Greatly decrease the needed calculation by 60% by saving the search result data from previous game

4.	Design an evaluation function based on Pruning to improve optimal position decision for the next step and move 
  
# Brief description about algorithm
    In this project, we tried to apply the adversarial search algorithm to the tic-tac-toe game. 
    Our strategy is to build min-max tree by iteration. In this tree, each tree node represents the next accessible board state. When it starts searching, Alpha-Beta pruning is added into the algorithm to prevent the agent from searching unnecessary node so that the speed will be largely increased .
    In addition, we hash the board string and save its hash_value and its evaluation score in dict (hash map) , when such board string is firstly met during search. The data in dictionary will be saved to TXT file after the game ends and will be read when next round begins. It can save time from repeating evaluate the score of the same board_string during search.
    
 # How to run
    First, run the main.py with python3 installed; then, choose Human-Computer Fighting mode or AI versus mode.
File hierarchy:

    main.py: main function for the agent
    
    API_Connect.py: API utility functions
    
    Eva.py: Evaluation function
    
    Training_data_X_Y.txt: trained data for X by X board with target of Y
    

# About Evaluation function:
 1.	For N target, the evaluation score is from -n**（n-1) to +n**(n-1). If the target is 5, for example, -625 means this AI is lost, and 625 means this AI win. The beginning score is 0. If the game doesn’t end, the score is not allowed to be greater than 625 and smaller than -624.

2.	When Target=5, for example. One 5-piece row is rated as 625, 4-piece row is rated as 125 (625/target), 3-piece row is 25, 2-piece row is 5. 1 piece is rated as 1. The ratio is determined according to target. If one end of row is blocked, the rating for this row is reduced by half. If both two ends of this row are blocked by opponent, one piece is this row is counted as one point.

3.	If the game doesn’t end, getting this_AI score by adding the score of all rows which belong to this_AI, and add the score of opponent by the same method. Notice this_AI’s score is a positive number and opponent’s score is changed to be a corresponding negative number. This_AI’s score+opponent score is the final evaluation score of this board’s situation.

4.	If one side (this AI or opponent) has won, directly return the max value or min value, such as +625 or -625 when target is 5.


# 估分规则
1. 对于n子棋，整个棋局的分数为-n**（n-1)到+n**(n-1)分。以五子棋为例，-625表示己方输对方赢，+625表示己方(AI)赢，开局分数为0；若棋盘下满后仍未分胜负，设为平局。若棋局未结束，最高分不得超过624，最低分不得低于-624.

2.以五子棋为例，如棋局中己方有1一条5子连线，则己方评分为625分，有1条4子连线，125分；一条3子连线，25分；一条二字连线5分，一子1分 （这里的倍数根据N子棋中的N决定）

3.将所有己方连线情况相加（若游戏尚未结束，最高不超过5**(n-1)-1分），如果一端已有封堵，则该条线评分减半；如果两端均有封堵，则该条线一子一分,一子不考虑封堵情况；(后期可考虑此时是己方下还是对方下，据此进行加权）

4.对对手棋子的评分也采用以上办法，不同之处为将分值改为负分

5.关于第一步下法，如服务器返回空棋盘，则下载棋盘中间；如果对方先下棋，则下载对方旁边（哪侧距离边缘更远下在哪侧）

# About the search
Used machine specs:  
    python 3.7, CPU i7 8086K, six-core twelve-thread
    
Environment:
    fully observed，Single-agent，episodic，dynamic, deterministic
    
Search space: 
    Extend 2 or other circles around the current chess piece, equal to a 5x5 board, this is a global parameter which can be adjusted in code
    
Description of the agent:
     Read the chess board, based on the board using minmax algorithm and evaluation function to decide the optimal position for the next step and move.
     
# Indicate if the game is a loss, win
   When the return value of the evaluation function is negative maximum, it loss; when value is maximum (625 points when target=5), it wins; when there are no position left for move, it draw.
   
# Result：
1.The accuracy of evaluation function increases greatly as the movements going on. Especially when the board size is big, the accuracy and rationality become very high. When the chess board is rather small (like 3x3), the agent prefers to defense and tend to block off opponent’s action line. 

2.In EVE mode, Currently the tree’s depth is 4 levels (actually 5 futural step, from level 0). This means 2 steps will be considered for opponent and three for this AI agent, which is a possible range for a player to make an irreversible attack. In PVE mode, the search depth will be dynamically adjusted according to running time, from 3 levels to 6 levels (4 futural steps to 7)

3. Multi_processing was used to improve efficiency of the agent. This feature allows the nodes on the first level to generating successors simultaneously. The running time is shortened at least 2 times comparing to before. The effect is depending on CPU, the more CPU cores/threads one computer has, the better the effect will be.

4.The searching results (evaluation score for different possible boards’ situation) from previous games will be saved as references for later games, which greatly decrease the needed calculation.



Question：

  1.为什么是-n**（n-1)到+n**(n-1)
  
  2.Eva中的m其实是target？
  
  3.为什么对方先下子就下在对方旁边（离边缘更远的那一边）
  
  4.为什么棋盘越大 准确性越高
  
  5.以前生成的数据是如何在这一次调用的
