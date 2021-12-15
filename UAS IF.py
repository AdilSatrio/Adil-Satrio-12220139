import streamlit as st
import pandas as pd
import numpy as np
import json

DATA = 'data/produksi_minyak_mentah.csv'
CODE = 'data/kode_negara_lengkap.json'

st.set_page_config(layout="wide")

@st.cache
def load_data():
    df = pd.read_csv(DATA)
    loc = pd.read_json(CODE)
    data = df.join(loc.set_index('alpha-3'),on='kode_negara')[['kode_negara', 'tahun', 'produksi','name','region','sub-region']].pivot(index=['name','kode_negara','region','sub-region'],columns='tahun',values='produksi').reset_index()
    data = data[~data['name'].isnull()]
    data = pd.melt(data,id_vars=data.columns[:4],value_vars=data.columns[4:],value_name='produksi').sort_values(by=['name','tahun']).reset_index(drop=True)
    data['produksi'] = data['produksi'].fillna(0)
    data['produksi'] = data['produksi'].astype(float)
    data['name'] = data['name'].astype(str)
    return data

data = load_data()

negara = st.sidebar.selectbox(
    "Pilih Negara",
    sorted(data['name'].unique().tolist()),
)

tahun = st.sidebar.slider(
    'Pilih Tahun', 
    min(data['tahun']), 
    max(data['tahun']), 
    max(data['tahun'])
)


st.title(f'Produksi Minyak {negara}')

chart_data1 = data[data['name']==negara][['tahun','produksi']]
chart_data1['tahun'] = pd.to_datetime(chart_data1['tahun'], format='%Y')
chart_data1 = chart_data1.set_index('tahun')
chart_data1 = chart_data1.fillna(0)

top10yr = list(sorted(data[data['tahun']==tahun].sort_values('produksi',ascending=False).head(10)['name'].values.tolist() + [negara]))
chart_data2 = data[(data['tahun']==tahun) & (data['name'].isin(top10yr))][['name','produksi']].sort_values('produksi',ascending=False).set_index('name')

top10all = list(sorted(data.groupby('name')['produksi'].sum().sort_values(ascending=False).head(10).reset_index()['name'].values.tolist() + [negara]))
chart_data3 = data[data['name'].isin(top10all)].groupby('name')['produksi'].sum()

topyear = data[data['tahun']==tahun].sort_values('produksi',ascending=False).drop('tahun',axis=1).iloc[0]
topall = data.groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().sort_values(ascending=False).reset_index().iloc[0]

minyear = data[(data['tahun']==tahun) & (data['produksi']>0)].sort_values('produksi').drop('tahun',axis=1).iloc[0]
minall = data.groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().reset_index()
minall = minall[minall['produksi']>0].sort_values(by='produksi').iloc[0]

zeroyear = data[(data['tahun']==tahun) & (data['produksi']==0)].reset_index(drop=True).drop(['tahun','produksi'],axis=1)
zeroall = data.groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().reset_index()
zeroall = zeroall[zeroall['produksi']==0].reset_index(drop=True).drop('produksi',axis=1)

st.header("Produsen Tertinggi dan Terendah")
cola,colb,colc,cold = st.columns(4)

with cola:
    st.subheader(f"Produsen Tertinggi {tahun}")
    st.components.v1.html(
        f'''
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div class="card">
            <p style="margin-bottom:0"><b>Negara : </b>{topyear['name']}</p>
            <p style="margin-bottom:0"><b>Kode Negara : </b>{topyear['kode_negara']}</p>
            <p style="margin-bottom:0"><b>Region : </b>{topyear['region']}</p>
            <p style="margin-bottom:0"><b>Sub-Region : </b>{topyear['sub-region']}</p>
            <p style="margin-bottom:0"><b>Produksi : </b>{topyear['produksi']}</p>
        </div>
        '''
    )

with colb:
    st.subheader(f"Produsen Tertinggi")
    st.components.v1.html(
        f'''
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div class="card">
            <p style="margin-bottom:0"><b>Negara : </b>{topall['name']}</p>
            <p style="margin-bottom:0"><b>Kode Negara : </b>{topall['kode_negara']}</p>
            <p style="margin-bottom:0"><b>Region : </b>{topall['region']}</p>
            <p style="margin-bottom:0"><b>Sub-Region : </b>{topall['sub-region']}</p>
            <p style="margin-bottom:0"><b>Produksi : </b>{topall['produksi']}</p>
        </div>
        '''
    )

with colc:
    st.subheader(f"Produsen Terendah {tahun}")
    st.components.v1.html(
        f'''
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div class="card">
            <p style="margin-bottom:0"><b>Negara : </b>{minyear['name']}</p>
            <p style="margin-bottom:0"><b>Kode Negara : </b>{minyear['kode_negara']}</p>
            <p style="margin-bottom:0"><b>Region : </b>{minyear['region']}</p>
            <p style="margin-bottom:0"><b>Sub-Region : </b>{minyear['sub-region']}</p>
            <p style="margin-bottom:0"><b>Produksi : </b>{minyear['produksi']}</p>
        </div>
        '''
    )

with cold:
    st.subheader(f"Produsen Terendah")
    st.components.v1.html(
        f'''
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div class="card">
            <p style="margin-bottom:0"><b>Negara : </b>{minall['name']}</p>
            <p style="margin-bottom:0"><b>Kode Negara : </b>{minall['kode_negara']}</p>
            <p style="margin-bottom:0"><b>Region : </b>{minall['region']}</p>
            <p style="margin-bottom:0"><b>Sub-Region : </b>{minall['sub-region']}</p>
            <p style="margin-bottom:0"><b>Produksi : </b>{minall['produksi']}</p>
        </div>
        '''
    )

st.header("Grafik Time-series")
st.line_chart(chart_data1)

col1, col2 = st.columns(2)

with col1:
    st.header(f'Produksi {negara} vs Top 10 Produsen pada Tahun {tahun}')
    st.bar_chart(chart_data2)

with col2:
    st.header(f'Produksi {negara} vs Top 10 Produsen Kumulatif')
    st.bar_chart(chart_data3)

col3, col4 = st.columns(2)

with col3:
    st.header(f'Negara dengan Produksi Nol pada Tahun {tahun}')
    st.dataframe(zeroyear)

with col4:
    st.header('Negara Non-produsen Minyak')
    st.dataframe(zeroall)
