# libaries
import streamlit as st
# classes
from DataModel import DataModel
from pages.classes.TablePage import TablePage

def run():
    # get data
    dm = DataModel()
    df = dm.get()

    # create opening page and all sidetabs 
    st.title('Minecraft-Dashboard')
    TablePage(df.copy())

if __name__ == "__main__":
   run()