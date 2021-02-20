## Taylan Unal CMPSC442-AI SP21
## Project 1: Search, Due Sunday 2/21 at 11:59pm

## Activate Conda Environment
1. conda create --name <env-name> python=3.6 
2. source activate <env-name>

If you run python -V, should see Python 3.6.x

## Leaving Conda Environment
1. source deactivate

If you run python -V, should see Python 3.8.x


## Notes
- Fringe (in AI Search Context) is the set of all nodes at the end of all visited paths. Also known as fringe, frontier, border
- Use Stack, Queue, PriorityQueue from util.py