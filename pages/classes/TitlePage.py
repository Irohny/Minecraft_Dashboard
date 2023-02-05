import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class TitlePage():
    def __init__(self, df):
        self.list_of_cities = list(df['Stadt'].unique())
        self.list_of_provinces = list(df['Province'].unique())
        self.list_of_houses = list(df['Name'].unique())
        self.list_of_city_parts = list(df['Stadtteil'].unique())
        
        self.__build_page(df)

    def __build_page(self, df):
        '''
        Method for designing the first page of the minecraft frontend
        Show some basic statistics of the world
        :param df: dataframe with the data of all houses from the backend
        '''
        self.__build_gesamtstatistik_header(df.copy())
        st.markdown('____')
        self.__build_preisverteilung(df, 'Province')

    def __build_gesamtstatistik_header(self, df):
        col = st.columns([0.5, 3, 3, 3, 3, 0.5])
        with col[1]:
            # gesamte wohnfläche
            st.metric('Gesamte Wohnfläche', int(df['Area'].sum()))
            # teuerstes haus 
            name, value = self.get_param_infos(df, 'Preis', 'Name','max')
            st.metric('Teuerstes Haus', f'{name}', delta=f'{value} E')
            # billigestes haus
            name, value = self.get_param_infos(df, 'Preis', 'Name', 'min')
            st.metric('Billigstes Haus', f'{name}', delta=f'{value} E')

        with col[2]:
            # Anzahl der Häuser in der Datanbank
            st.metric('Gesamtanzahl der Häuser', len(df))
            # größtes haus
            name, value = self.get_param_infos(df, 'Area', 'Name', 'max')
            st.metric('Größtes Haus', f'{name}', delta=f'{value} Blöcke')
            # kleinstes haus
            name, value = self.get_param_infos(df, 'Area', 'Name', 'min')
            st.metric('Kleinstes Haus', f'{name}', delta=f'{value} Blöcke')

        with col[3]:
            # anzahl der verschieden städte
            cities = len(df['Stadt'].unique())
            st.metric('Gesamtanzahl der Städte', value=cities)
            # größte stadt
            df_small = df.groupby(by='Stadt').agg(sum=('Area', 'sum')).reset_index()
            st.metric('Größte Stadt', f"{df_small.at[0, 'Stadt']}", delta=f"{int(df_small.at[0, 'sum'])} Blöcke")
            # kleinste stadt
            st.metric('Kleinste Stadt', f"{df_small.at[len(df_small)-1, 'Stadt']}", delta=f"{int(df_small.at[len(df_small)-1, 'sum'])} Blöcke")

        with col[4]:
            # anzahl der provincen
            prov = len(df['Province'].unique())
            st.metric('Gesamtzahl der Provinzen', value=int(prov))
            # größte province
            df_small = df.groupby(by='Province').agg(sum=('Area', 'sum')).reset_index()
            st.metric('Größte Province', f"{df_small.at[0, 'Province']}", delta=f"{int(df_small.at[0, 'sum'])} Blöcke")
            # kleinste province
            st.metric('Kleinste Province', f"{df_small.at[len(df_small)-1, 'Province']}", delta=f"{int(df_small.at[len(df_small)-1, 'sum'])} Blöcke")

    def get_param_infos(self, df, col_agg, col_name, method):
      '''
      Method for geting min/max values from a column with respect to a other column
      :param df: data
      :param col_agg: name of the column to get the min or max value
      :param col_name: name of the column that feature is interesting with respect to the other column extrema
      :param method: string to define if min or max is choosen
      :return name: element of col_name where col_agg is extrem
      :return value: value of the extrema of col_agg 
      '''
      if method == 'max':
            idx = df[col_agg].argmax()
      elif method == 'min':
            idx = df[col_agg].argmin()
      name = df.at[idx, col_name]
      value = df.at[idx, col_agg]
      return name, value

    def __build_preisverteilung(self, df, agg_col):
        '''
        Method for creating a hous cost distribution plot
        '''
        
        df = df[-(df[agg_col].isnull())].reset_index(drop=True)
        cols = st.columns([3, 1])
        with cols[0]:
            st.header('Vergleiche die Hauspreise in den verschiedenen Regionen')
        fig, axs = plt.subplots(1, figsize=(8, 5))
        cols = st.columns([1, 3])
        with cols[0]:
            with st.form('ebenen filter'):
                ebene = st.selectbox('Wähle Kategorie', options=['Provinze', 'Stadt', 'Stadteile'])
                if ebene == 'Stadtteil':
                    drilldown = st.multiselect('Wähle Städte', options=self.list_of_cities)
                elif ebene == 'Stadt':
                    drilldown = st.multiselect('Wähle Provincen', options=self.list_of_provinces)
                else:
                    drilldown = []
                st.form_submit_button('Plot')
        with cols[1]:
            # feature for province verteilung plot
            if agg_col == 'Province':
                feature = self.list_of_provinces
                col = 'Province'
                data = df[['Province', 'Preis']]
            # feature stadt verteilung plot
            elif agg_col == 'Stadt':
                if len(drilldown)>0:
                    data = df[df['Province'].isin(drilldown)].reset_index(drop=True)
                else:
                    data = df
                feature = list(data['Stadt'].unique())
                col = 'Stadt'
            # feature for stadtteil verteilung plot
            elif agg_col == 'Stadtteil': 
                if len(drilldown)>0:
                    data = df[df['Stadt'].isin(drilldown)].reset_index(drop=True)
                else:
                    data = df
                feature = list(data['Stadtteil'].unique())
                col = 'Stadtteil'
            
            for i, feat in enumerate(feature):
                tmp = data[data[col]==feat]['Preis'].astype(float).to_numpy()
                axs.violinplot(tmp, positions=[i])
                if len(tmp)<=1:
                    continue
                axs.boxplot(tmp, positions=[i])
            axs.set_xticks(range(len(self.list_of_provinces)))
            axs.set_xticklabels(self.list_of_provinces, rotation=-80)
            axs.set_ylabel('Preis')
            axs.set_title(f'Preise zwischen allen {agg_col}')
            axs.grid()
                

            st.pyplot(fig)
