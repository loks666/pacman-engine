# CE811 Assignment 2 (Pacman)

**Student Registration Number:** [Your Registration Number]

---

## 1. ce811ManhattanGhostDodgerAgent (Board Layout: simpleLoopMaze)

### **Code**
*(Please paste the code for ce811ManhattanGhostDodgerAgent here)*

### **Run Summary**
*(Please paste the summary results after running 10 games, including the five summary metrics that start with an asterisk)*

### **Agent Logic Description**
The ce811ManhattanGhostDodgerAgent primarily uses Manhattan distance to decide Pacman's movement. The agent first tries to avoid contact with dangerous ghosts. If Pacman is on the same horizontal or vertical line as a ghost, the agent will attempt to move north or south to evade it. Additionally, the agent prioritizes moving west, and if westward movement is not possible, it will select the best available move to collect food. This strategy ensures that Pacman avoids ghosts while still efficiently collecting food.

---

## 2. ce811ManhattanGhostDodgerHunterAgent (Board Layout: simpleLoopMazeCapsule)

### **Code**
*(Please paste the code for ce811ManhattanGhostDodgerHunterAgent here)*

### **Run Summary**
*(Please paste the summary results after running 10 games, including the five summary metrics that start with an asterisk)*

### **Agent Logic Description**
The ce811ManhattanGhostDodgerHunterAgent builds on the ce811ManhattanGhostDodgerAgent by adding the handling of capsules. When dangerous ghosts are nearby, Pacman enters a fleeing mode and prioritizes escaping from the ghosts. The agent avoids entering the ghost house and tracks its movement history to prevent cycling between actions. This ensures that Pacman continues to evade ghosts while collecting both food and capsules efficiently.

---

## 3. ce811OneStepLookaheadManhattanAgent (Board Layout: mediumClassic)

### **Code**
*(Please paste the code for ce811OneStepLookaheadManhattanAgent here)*

### **Run Summary**
*(Please paste the summary results after running 10 games, including the five summary metrics that start with an asterisk)*

### **Agent Logic Description**
The ce811OneStepLookaheadManhattanAgent uses a one-step lookahead strategy to choose the best action. The agent evaluates the potential future states of all legal actions and selects the one with the highest expected value. The evaluation takes into account factors such as food distance, ghost proximity (both frightened and dangerous ghosts), and capsule locations. This strategy allows the agent to maximize food and capsule collection while minimizing risk by avoiding dangerous ghosts.

---

## 4. ce811OneStepLookaheadDijkstraAgent (Board Layout: mediumClassic)

### **Code**
*(Please paste the code for ce811OneStepLookaheadDijkstraAgent here)*

### **Run Summary**
*(Please paste the summary results after running 10 games, including the five summary metrics that start with an asterisk)*

### **Agent Logic Description**
The ce811OneStepLookaheadDijkstraAgent combines the one-step lookahead strategy with Dijkstra’s algorithm. By calculating the shortest paths from Pacman’s current position to various targets (food, capsules, ghosts), the agent optimizes its movement. The agent uses Dijkstra’s algorithm to dynamically adjust paths to avoid dangerous ghosts and prioritize frightened ghosts. This approach improves the agent's navigation in complex mazes and increases the efficiency of food and capsule collection.

---

## 5. ce811DijkstraRuleAgent (Board Layout: mediumClassic)

### **Code**
*(Please paste the code for ce811DijkstraRuleAgent here)*

### **Run Summary**
*(Please paste the summary results after running 10 games, including the five summary metrics that start with an asterisk)*

### **Agent Logic Description**
The ce811DijkstraRuleAgent further refines the Dijkstra-based pathfinding by introducing dynamic cost maps. It adjusts movement costs to avoid areas close to dangerous ghosts. The agent dynamically updates its target based on capsule and food locations, ensuring maximum score accumulation while maintaining safety. This rule-based strategy enables the agent to adapt to complex environments, demonstrating higher intelligence and efficiency.

---

## 6. ce811MyBestAgent (Board Layout: mediumClassic)

### **Code**
*(Please paste the code for ce811MyBestAgent here)*

### **Run Summary**
*(Please paste the summary results after running 10 games, including the five summary metrics that start with an asterisk)*

### **Agent Logic Description**
The ce811MyBestAgent is an advanced agent that integrates various strategies and optimizations. It not only uses Dijkstra’s algorithm for efficient pathfinding but also combines dynamic cost adjustment and multi-goal prioritization to ensure that Pacman avoids dangerous ghosts while collecting food and capsules. The agent maintains a history of actions and employs a fleeing mode to prevent getting stuck in action loops. These combined optimizations make ce811MyBestAgent the most performant Pacman agent.

---

## Appendix: Dijkstra Helper Functions

### **Code**
*(Please paste the code for Dijkstra helper functions like `calculate_gscores` and any other relevant functions here)*

### **Screenshots**
*(Please insert the screenshots for Assignment 2 Pacman Agents quiz, Question 4 and Question 5, to demonstrate the correctness of the Dijkstra helper functions)*