import streamlit as st
import random

# This function is called whenever a user makes a new guess
def user_guess():
    st.session_state["data"].tries += 1

# Make sure the persistent state is initialised properly. The state is
# stored in an object of the following class:
class GameData:
    
    def __init__(self):
        self.number = random.randint(1, 100)
        self.tries = 0

# If we aren't already remembering an object of class GameData, then make
# one and store it.
if not("data" in st.session_state):
    st.session_state["data"] = GameData()
    
"I've thought of a number between 1 and 100. Can you guess what it is?"

data = st.session_state["data"]
guess = st.number_input("Your guess:", 
                        min_value=0, max_value=100, step=1, value=0,
                        on_change=user_guess)

if data.tries == 0:
    "A first hint: it is more than zero."
else:
    if guess < data.number:
        "You guessed too low."
    elif guess > data.number:
        "You guessed too high."
    else:
        f"Amazing! You got it in {data.tries} tries!"

st.write("this is a test")        
