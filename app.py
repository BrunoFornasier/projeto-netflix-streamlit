import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregamento de dados
df = pd.read_csv("netflix_titles.csv")
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df = df.dropna(subset=['release_year', 'date_added'])

# Filtro por ano
anos = sorted(df['release_year'].unique())
ano = st.selectbox("Selecione o ano de lançamento", anos)
df_filtrado = df[df['release_year'] == ano]

st.title("Dashboard Netflix - Streamlit")

# Gráfico de linha - Número de títulos lançados por mês
st.subheader("Lançamentos por mês")
linha = df_filtrado['date_added'].dt.month.value_counts().sort_index()
st.line_chart(linha)

# Gráfico de barra - Tipos (filme ou série)
st.subheader("Distribuição de tipos (Filmes vs Séries)")
bar = df_filtrado['type'].value_counts()
st.bar_chart(bar)

# Gráfico de dispersão - ano vs duração
st.subheader("Duração vs Ano de Lançamento")
df_temp = df_filtrado[df_filtrado['duration'].str.contains("min", na=False)].copy()
df_temp['minutos'] = df_temp['duration'].str.extract("(\d+)").astype(float)
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df_temp, x='release_year', y='minutos', ax=ax1)
st.pyplot(fig1)

# Gráfico de pizza - Ratings
st.subheader("Distribuição por classificação etária (Rating)")
fig2, ax2 = plt.subplots()
df_filtrado['rating'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2)
ax2.set_ylabel("")
st.pyplot(fig2)

# Tabela
st.subheader("Dados filtrados")
st.dataframe(df_filtrado[['title', 'type', 'release_year', 'rating', 'duration']])
