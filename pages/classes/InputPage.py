import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

class InputPage():
    def __init__(self):
      # --- USER AUTHENTICATION ---
      #with st.sidebar:
      #      names = ['Chriss']
      #      usernames = ['Chriss']
            
      #      file_path = Path(__file__).parent / "hashed_pw.pkl"
      #      with file_path.open("rb") as file:
      #            hashed_passwords = pickle.load(file)
            
      #      authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
      #      'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
            
      #      name, authentication_status, username = authenticator.login("Login", "main")
            
      #      if authentication_status:
      #            authenticator.logout('Logout', 'main')
      #            st.write(f'Welcome *{name}*')
      #            secrets = True
      #     elif authentication_status == False:
      #            st.error('Username/password is incorrect')
      #            secrets = False
      #      elif authentication_status == None:
      #            st.warning('Please enter your username and password')
      #            secrets = False
      # build input page layout
      self.__build_page()

    def __build_page(self,):
        with st.form('Einagbe'):
            cols = st.columns([1,2,1, 2,1])
            with cols[0]:
                  pass
            
            with cols[1]:
                  name = st.text_input('Bewohner')      
                  size = st.number_input('Wohnfläche [Blöcke]', step=1)
                  etagen = st.number_input('Etagen', step=1)
                  
                  bad = st.radio('Badzimmer', ['Nein', '1', '2', '3+'], horizontal=True)
                  garden = st.radio('Garten', ['Nein', 'Ja'], horizontal=True)

            with cols[2]:
                  pass
                  
            with cols[3]:
                  city = st.selectbox('Stadt', options=['tbc'])
                  part = st.selectbox('Stadtteil', options=['tbc'])
                  province = st.selectbox('Province', options=['tbc'])
                  
                  kitchen = st.radio('Küchenräume', ['Ofenecke', '1', '2', '3+'], horizontal=True)
                  sleep = st.radio('Schlafräume', ['Bettecke', '1', '2', '3+'], horizontal=True)
                  
            with cols[4]:
                  st.title('')
                  st.title('')
                  st.title('')
                  st.title('')
                  st.title('')
                  st.title('')
                  st.title('')
                  st.title('')
                  if st.form_submit_button('Fertig'):
                        pass

