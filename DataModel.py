from dotenv import load_dotenv
import pandas as pd
import numpy as np
from deta import Deta
import os
import streamlit as st

class DataModel:
    def __init__(self,):
        #load_dotenv(".env")
        #key = os.getenv('key')
        #deta = Deta(key)
        #db = deta.Base("minecraft_database")
        # offline test mode
        self.__create_data_object()
        
    def get(self,):
       return self.data
    
    def __create_data_object(self,):
        '''
        Method to handel data loading from database over different classes and reloadings
        load data at intial call and if reload flag is true
        else use safed data from streamlit session state
        '''
        if 'login' not in st.session_state:
            self.data = self.__load_data_offline()
            self.data = self.__clean_data(self.data)
            st.session_state = {'data':self.data,
                                'login':False,
                                'reload_flag':False,
                                'drilldown':['Province']}
        elif st.session_state['reload_flag']:
            self.data = self.__load_data_offline()
            self.data = self.__clean_data(self.data)
            st.session_state = {'data':self.data,
                                'login':False,
                                'reload_flag':False,
                                'drilldown':['Province']}
        else:
            self.data = st.session_state['data']
       
       
    def __load_data_offline(self,):
      df = pd.read_csv('Minecraft_Haus_Tabelle.csv', index_col=False)
      return df
    
    def __clean_data(self, df):
        '''
        Method for cleaning data for better visualization
        :param df: dataframe with data from database or local csv file
        :return df: cleaned dataframe for further processing and visualization
        '''
        df['Name'] = df['Name'].astype(str)
        df['Stadteil'] = df['Stadtteil'].astype(str)
        df[df['Stadteil'].isin(['', []])] = np.nan
        df['Province'] = df['Province'].astype(str)
        df[df['Province'].isin(['', []])] = np.nan
        df['Stadt'] = df['Stadt'].astype(str)
        df['Area'] = df['Area'].astype(np.float64)
        df['Etagen'] = df['Etagen'].astype(np.float64)
        df['Kueche'] = df['Kueche'].astype(np.float64)
        df['Bad'] = df['Bad'].astype(np.float64)
        df['Schlaf'] = df['Schlaf'].astype(np.float64)
        df['Garten'] = df['Garten'].astype(bool)
        df['Preis'] = df['Preis'].astype(np.float64)
        return df