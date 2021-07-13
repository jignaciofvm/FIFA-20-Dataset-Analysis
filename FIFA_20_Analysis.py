import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance

header = st.beta_container()
dataset = st.beta_container()
recommender = st.beta_container()
model = st.beta_container()


with header:
    st.title('FIFA 20 Analysis - Jose Ignacio Fdez')
    st.text("""
        ES: En este proyecto presentamos, por un lado, un sistema de recomendación de jugadores
        y, por otro, un modelo de predicción del valor de un futbolista en el mercado en función
        de sus características

        EN: In this project we present a player recommendation system and a prediction model of the
        player's value in the market based on its characteristics
         """)

with dataset:
    st.header('FIFA 20 Dataset')
    st.text("""
        ES: El conjunto de datos empleado se ha obtenido de Kaggle y consta de un total de 18.000
        futbolistas y 75 variables.

        EN: The dataset used was obtained from Kaggle and consists of 18,000 players and
        75 variables.
    """)
    df_similarity = pd.read_csv('FIFA-20-Dataset-Analysis/files/df_similarity.csv')
    st.write(df.head())
    st.text("""
        ES: Comentar que el dataset anterior ha sido tratado. Si quiere seguir el proyecto, acuda
        a mi [Github](https://github.com/jignaciofvm)
        EN: Please note that the previous dataset has been processed. If you want to follow the
        project, go to my [Github](https://github.com/jignaciofvm)
        """)

with recommender:
    st.header('Recommender System')
    st.text("""
            ES: Por favor, selecciona al jugador para el que desea encontrar sustituto
            EN: Please, choose player for whom you want to find a replacement""")
    sel_col,disp_col = st.beta_columns(2)
    player = sel_col.selectbox('Player', options = ['Lionel Messi',
 'C. Ronaldo dos Santos Aveiro','Neymar da Silva Santos Jr.','Jan Oblak','Kevin De Bruyne','Eden Hazard','Mohamed Salah','Virgil van Dijk','Marc-André ter Stegen','Luka Modrić','Kylian Mbappé',
 "N'Golo Kanté",'Alisson Ramses Becker','Harry Kane','Kalidou Koulibaly','Antoine Griezmann','David De Gea Quintana','Sergio Busquets Burgos','Robert Lewandowski','Luis Suárez',
 'Sergio Ramos García','Sergio Agüero','Giorgio Chiellini','Paulo Dybala','Ederson Santana de Moraes','Sadio Mané','Raheem Sterling','Paul Pogba','Thibaut Courtois','Christian Eriksen',
 'Pierre-Emerick Aubameyang','Marco Reus','Toni Kroos','Diego Godín','Edinson Cavani','David Josué Jiménez Silva','Hugo Lloris','Manuel Neuer','Samir Handanovič','Gerard Piqué Bernabeu'],
 index = 0)
    num_players = sel_col.selectbox('# of Players', options = [5, 10, 15, 20, 50], index = 0)

X = df_similarity.drop(['Name','Overall', 'Value'], axis = 1)
std=StandardScaler()
X=std.fit_transform(X)
sn=df_similarity["Name"].to_list()
sv=df_similarity["Value"].to_list()
so = df_similarity['Overall'].to_list()
sf = df_similarity['foot'].to_list()
sp = df_similarity['PAC'].to_list()
ss = df_similarity['SHO'].to_list()
spp = df_similarity['PAS'].to_list()
sd = df_similarity['DRI'].to_list()
sdd = df_similarity['DEF'].to_list()
sph = df_similarity['PHY'].to_list()

def similaridad (nombre, num_jugadores):
  p_ind=df_similarity[df_similarity["Name"]==nombre].index[0] # Indice del nombre del jugador
  cossim=[]
  for i in range (0,len(X)): # Recorremos el dataframe
      cossim.append(1 - distance.cosine(X[p_ind],X[i])) # Restamos uno para obtener el valor
  pd.Series(cossim)
  sim2={"Name":sn,"cossim":cossim, 'Value': sv, 'Overall': so, 'foot':sf, 'PAC': sp, 'SHO': ss, 'PAS': spp, 'DRI': sd, 'DEF': sdd, 'PHY': sph}
  sim2=pd.DataFrame(sim2)
  # Para transformar de nuevo la variable foot a Right or Left
  sim2['foot'] = sim2['foot'].apply(lambda x: 'Right' if x ==0 else 'Left')
  similarity = sim2.iloc[sim2["cossim"].sort_values(ascending=False).index].head(num_jugadores+1)
  sim_df = similarity.drop('cossim',axis = 1)
  sim_df['Value'] = sim_df['Value'].map('€{:,.2f}'.format)
  return sim_df.iloc[1:,:]

st.write(similaridad(player, num_players))
