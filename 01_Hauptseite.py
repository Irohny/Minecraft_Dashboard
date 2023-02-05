#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 10:47:10 2022

@author: christoph
"""
# libaries
import streamlit as st
# classes
from DataModel import DataModel
from pages.classes.TitlePage import TitlePage
from pages.classes.Layout import insert_layout_htmls

def run():
    insert_layout_htmls()
    # get data
    dm = DataModel()
    df = dm.get()

    # create opening page and all sidetabs 
    st.title('Minecraft-Dashboard')
    TitlePage(df.copy())

if __name__ == "__main__":
   run()