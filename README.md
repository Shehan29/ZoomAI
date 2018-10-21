# ZoomAI
## Project Description
Reinforcement Q-Learning with Python - Train AI to Self-Drive

## Training
The training is done for 30,000 epochs, where each epoch is a single game.
Set `render = True` (within the `main` method), if you would like to visually see the training (it is set to `False` by default in order to speed up training).

`python3 Train.py`

## Watch the AI in Action
The AI will load the trained model from `model.npy` and play the game by itself.

`python3 AIPlay.py`

## Play the Game
Play the game yourself to see if you can beat the AI. It has a current high score of **936** and achieves an average score of **737**.

`python3 HumanPlay.py`
