from os import name
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random


class AgentState(TypedDict):
    name: str
    guesses: list[int]
    target: int
    attempts: int
    lower: int
    upper: int
    hint: str


def setup_node(state: AgentState) -> AgentState:
    """Welcome the players to the game"""
    state["name"] = f"Hello One and only donkey {state['name']}"
    state["target"] = random.randint(1, 20)
    state["attempts"] = 0
    state["guesses"] = []
    state["lower"] = 1
    state["upper"] = 20
    state["hint"] = "Game started try to guess it"
    print(f"{state['name']} The game has begun. I chose a number between 1 and 20.")

    return state


def guess(state: AgentState) -> AgentState:
    """Generate a smarter guess based on previous hints"""
    possible_guesses = [
        i
        for i in range(state["lower"], state["upper"] + 1)
        if i not in state["guesses"]
    ]

    if possible_guesses:
        guess = random.choice(possible_guesses)
    else:
        guess = random.randint(state["lower"], state["upper"])

    state["guesses"].append(guess)
    state["attempts"] += 1
    print(
        f"Attempt {state['attempts']}: Guessing {guess} (Current range: {state['lower']}-{state['upper']})"
    )

    return state


def hint_node(state: AgentState) -> AgentState:
    """We will give hint based on the basis of last guess and update the bound"""
    latest_guess = state["guesses"][-1]
    target = state["target"]

    if latest_guess < target:
        state["hint"] = f"The number {latest_guess} is too low. Try higher!"

        state["lower"] = max(state["lower"], latest_guess + 1)
        print(f"Hint: {state['hint']}")

    elif latest_guess > target:
        state["hint"] = f"The number {latest_guess} is too high. Try lower!"

        state["upper"] = min(state["upper"], latest_guess - 1)
        print(f"Hint: {state['hint']}")
    else:
        state["hint"] = (
            f"Correct! You found the number {target} in {state['attempts']} attempts."
        )
        print(f"Success! {state['hint']}")

    return state


def should_continue(state: AgentState) -> AgentState:
    latest_guess = state["guesses"][-1]
    if latest_guess == state["target"]:
        print("GAME OVER: Number found!")
        return "end"
    elif state["attempts"] >= 7:
        print(f"GAME OVER: Maximum attempts reached! The number was {state['target']}")
        return "end"
    else:
        print(f"CONTINUING: {state['attempts']}/7 attempts used")
        return "continue"


graph = StateGraph(AgentState)

graph.add_node("setup", setup_node)
graph.add_node("guess", guess)
graph.add_node("hint", hint_node)

graph.add_edge(START, "setup")


graph.add_edge("setup", "guess")
graph.add_edge("guess", "hint")

graph.add_conditional_edges("hint", should_continue, {"continue": "guess", "end": END})

app = graph.compile()

# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")


result = app.invoke(
    {"name": "baka", "guesses": [], "attempts": 0, "lower": 1, "upper": 20}
)
print(result["guesses"])
