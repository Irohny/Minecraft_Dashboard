import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

class TablePage():
    def __init__(self, df):
        self.list_of_cities = list(df['Stadt'].unique())
        self.list_of_provinces = list(df['Province'].unique())
        self.list_of_houses = list(df['Name'].unique())
        self.list_of_city_parts = list(df['Stadtteil'].unique())
        self.list_of_feature = list(df.columns)
        self.__build_page(df)

    def __build_page(self, df):
        '''
        Method for generating a research table page with all info of cities, provinces and houses
        :param df: dataframe data from the database
        '''
        # choose feature to display in the search table
        with st.form('feature selecting'):
            col = st.columns([1,3,3,1])
            with col[1]:
                    feature = st.multiselect('Wähle Eigenschaften', options=self.list_of_feature, default=self.list_of_feature)
            col = st.columns([1,3,3,1])
            with col[2]:
                    st.form_submit_button('Zeige Eigenschaften')
        
        # build filter and get objects
        prov, cities, parts, name = self.__build_dynamic_filter_components(feature)

        df_select = self.__filter_dataframe(df, feature, prov, cities, parts, name)
        AgGrid(df_select)

    def __build_dynamic_filter_components(self, feature):
        '''
        Method for creating filter options based on the shown features in the search table
        :param feature: list of feature that are shown in the search table
        :return prov: list of choosen provinces for displaying in the search table
        :return cities: list of choosen cities for displaying in the search table
        :return parts: list of choosen city parts for displaying in the search table
        :return name: list of choosen hous names for displaying in the search table
        '''
        # if name, stadt or province is choosen show more filters
        ds = pd.Series(feature)
        if ds.isin(['Province', 'Stadt', 'Name', 'Statdteil']).any():
            with st.form('More feature selection'):
                filter = ds[ds.isin(['Province', 'Stadt', 'Name', 'Stadtteil'])].reset_index(drop=True)
                # loop over all optional filter oportunities
                for i in range(len(filter)):
                    # province filter
                    if filter.at[i] == 'Province':
                        prov = st.multiselect('Wähle Provinzen', options=self.list_of_provinces)
                    else:
                        prov = []
                    # stadt filter
                    if filter.at[i] == 'Stadt':
                        cities = st.multiselect('Wähle Städte', options=self.list_of_cities)
                    else:
                        cities = []
                    # statdteil filter
                    if filter.at[i] == 'Stadtteil':
                        parts = st.multiselect('Wähle Stadtteile', options=self.list_of_city_parts)
                    else:
                        parts = []
                    # name filter
                    if filter.at[i] == 'Name':
                        name = st.multiselect('Wähle Häuser', options=self.list_of_houses)
                    else:
                        name = []
                # submit
                st.form_submit_button('Filter bestätigen')
        else: 
            prov = []
            cities = []
            parts = []
            name = []
        return prov, cities, parts, name

    def __filter_dataframe(self, df, feature, prov, cities, parts, name):
        return df[feature]
