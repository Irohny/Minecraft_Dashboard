# libaries
import streamlit as st
# classes
from DataModel import DataModel
from pages.classes.InputPage import InputPage

def run():
    # get data
    dm = DataModel()
    df = dm.get()

    # create opening page and all sidetabs 
    st.title('Minecraft-Dashboard')
    InputPage()

if __name__ == "__main__":
   run()