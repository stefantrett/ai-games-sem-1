## Commands

Run reference agent against test.py:

`java -jar Project_Java/ManKalah.jar "python3 Project_Python/main.py" "java -jar Project_Java/MKRefAgent.jar"`


## Pie Rule

The pile rule is implemented as follows:

1. If we are moving second, then we check how would we move if we were the opposing player
2. If we would have made the same move, then we decide to SWAP
3. Otherwise, we stick up to the previously assigned role
