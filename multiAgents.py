# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def euclideanDist(pos,goal):
	x1,y1 = pos
	x2,y2 = goal
	return ((abs(x1-x2)**2)+(abs(y1-y2)**2))**0.5
def manhattanDist(pos,goal):
	x1,y1 = pos
	x2,y2 = goal
	return ((abs(x1-x2))+(abs(y1-y2)))

class ReflexAgent(Agent):
	"""
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.

	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]



	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		"*** YOUR CODE HERE ***"
		currPos = currentGameState.getPacmanPosition()

		
		nextGhost = 999999
		for ghost in newGhostStates:
			if nextGhost > manhattanDist(newPos,ghost.getPosition()):
				nextGhost = manhattanDist(newPos,ghost.getPosition())
		currentGhost = 999999
		for ghost in newGhostStates:
			if currentGhost > manhattanDist(currPos,ghost.getPosition()):
				currentGhost = manhattanDist(currPos,ghost.getPosition())
		threatFurther = (nextGhost>currentGhost) #true if pacman increased the distance between the nearest ghost this round and the nearest ghost from next round (they can be different)

		willEat = (len(currentGameState.getFood().asList()) != len(newFood.asList())) # true if pacman will eat next round

		foodPositions = newFood.asList()
		nextFood = 999999
		for food in foodPositions:
			if nextFood > manhattanDist(newPos,food):
				nextFood = manhattanDist(newPos,food)
		currentFood = 999999   
		for food in foodPositions:
			if currentFood > manhattanDist(currPos,food):
				currentFood = manhattanDist(currPos,food)
		foodCloser = (currentFood>nextFood)#if pacman reduced distance with closest food from one round to anotehr (food can be different again)
		

		score = 0
		if (threatFurther):#if ghost further +10
			score+=10
		if (willEat):#if pacman will eat next round +20
			score+=20
		if (foodCloser):#if food closer than last time +20
			score+=20
		else:           #if food further, -5
			score-=5
		if (nextGhost<2): #if ghost too close, SNAKE !!! ABORT THE MISSION !!!
			score = 0
		
		return score

def scoreEvaluationFunction(currentGameState):
	"""
	This default evaluation function just returns the score of the state.
	The score is the same one displayed in the Pacman GUI.

	This evaluation function is meant for use with adversarial search agents
	(not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.

	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.

		Here are some method calls that might be useful when implementing minimax.

		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1

		gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action

		gameState.getNumAgents():
		Returns the total number of agents in the game

		gameState.isWin():
		Returns whether or not the game state is a winning state

		gameState.isLose():
		Returns whether or not the game state is a losing state
		"""
		"*** YOUR CODE HERE ***"
		ghostCount = gameState.getNumAgents()-1#reduce computation

		def Minimax_Decision(gameState):
			actions = gameState.getLegalActions(0)
			maxUtility = -99999
			for i in actions:
				successor = gameState.generateSuccessor(0, i)
				currentUtility = Min_Value(successor,self.depth,1)#begin with agent 1 a.k.a ghost 1
				if maxUtility < currentUtility:
					maxUtility = currentUtility
					maxAction = i
			return maxAction


		def Min_Value(gameState,depth,agentIndex):
			if gameState.isWin() or gameState.isLose():
				return self.evaluationFunction(gameState)
			actions = gameState.getLegalActions(agentIndex)
			value = 999999
			for i in actions:
				successor = gameState.generateSuccessor(agentIndex,i)
				if(agentIndex==ghostCount):
					value = min(value, Max_Value(successor,depth-1))#we finished with ghosts
					
				else:
					value = min(value, Min_Value(successor,depth,agentIndex+1))#or we didn't
					
			return value


		def Max_Value(gameState,depth):
			if gameState.isWin() or gameState.isLose() or depth == 0:
				return self.evaluationFunction(gameState)
			actions = gameState.getLegalActions(0) #0 = pacman
			value = -999999
			for i in actions:
				successor= gameState.generateSuccessor(0,i)
				value = max(value, Min_Value(successor,depth,1))
			return value

		return Minimax_Decision(gameState)   

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		ghostCount = gameState.getNumAgents()-1#reduce computation

		def Minimax_Decision(gameState):
			actions = gameState.getLegalActions(0)
			maxUtility = -99999
			a = -999999
			b = 999999
			for i in actions:
				successor = gameState.generateSuccessor(0, i)
				currentUtility = Min_Value(successor,self.depth,1,a,b)#begin with agent 1 a.k.a ghost 1
				if maxUtility < currentUtility:
					maxUtility = currentUtility
					maxAction = i
				if maxUtility > b:
					return maxAction
				a = max(a,maxUtility)				
			return maxAction


		def Min_Value(gameState,depth,agentIndex,a,b):
			if gameState.isWin() or gameState.isLose():
				return self.evaluationFunction(gameState)
			actions = gameState.getLegalActions(agentIndex)
			value = 999999
			for i in actions:
				successor = gameState.generateSuccessor(agentIndex,i)
				if(agentIndex==ghostCount):
					value = min(value, Max_Value(successor,depth-1,a,b))#we finished with ghosts

				else:
					value = min(value, Min_Value(successor,depth,agentIndex+1,a,b))#or we didn't
				if value < a:
					return value
				b = min(b,value)					
			return value


		def Max_Value(gameState,depth,a,b):
			if gameState.isWin() or gameState.isLose() or depth == 0:
				return self.evaluationFunction(gameState)
			actions = gameState.getLegalActions(0) #0 = pacman
			value = -999999
			for i in actions:
				successor= gameState.generateSuccessor(0,i)
				value = max(value, Min_Value(successor,depth,1,a,b))
				if value > b:
					return value
				a = max(a,value)
			return value

		return Minimax_Decision(gameState)   

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		Returns the expectimax action using self.depth and self.evaluationFunction

		All ghosts should be modeled as choosing uniformly at random from their
		legal moves.
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).

	DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
