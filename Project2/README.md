## Taylan Unal CMPSC442-AI SP21
## Project 2: Multi-Agent Search, Due Sunday 2/21 at 11:59pm

## Activate Conda Environment
1. conda create --name <env-name> python=3.6
2. source activate <env-name>
If you run python -V, should see Python 3.6.x

## Leaving Conda Environment
1. source deactivate
If you run python -V, should see Python 3.6.x

## COMMANDS TO RUN:
### Question1 Reflex
- python autograder.py -q q1
- python autograder.py -q q1 --no-graphics

### Question2 Minimax
- python autograder.py -q q2
- python autograder.py -q q2 --no-graphics
- python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4

Odd case, ends game ASAP when death is unavoidable:
- python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3

### Question3 Alpha-Beta Pruning
- python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
- python autograder.py -q q3
- python autograder.py -q q3 --no-graphics

### Question4 Expectimax
- python autograder.py -q q4
- python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
- python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
- python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10

### Question5 Evalutaion function
- python autograder.py -q q5
- python autograder.py -q q5 --no-graphics

## Notes
- float("inf") is a very large value used in evalulation. Can also use -float(inf) to represent a very large negative value.
- Fringe (in AI Search Context) is the set of all nodes at the end of all visited paths. Also known as fringe, frontier, border
- Use Stack, Queue, PriorityQueue from util.py