import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

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

options = st.sidebar.multiselect(
    'Pilih Negara Pembanding',
    sorted(data['name'].unique().tolist()),
    [])

tahun = st.sidebar.slider(
    'Pilih Tahun', 
    min(data['tahun']), 
    max(data['tahun']), 
    (min(data['tahun']),max(data['tahun']))
)


st.title(f'Produksi Minyak {negara}')

chart_data1 = data[data['name']==negara][['tahun','produksi']]
chart_data1['tahun'] = pd.to_datetime(chart_data1['tahun'], format='%Y')
chart_data1 = chart_data1.set_index('tahun')
chart_data1 = chart_data1.fillna(0)


if len(list(set(options+[negara])))>1:
    chart_data2 = data[(data['tahun']>=tahun[0]) & (data['tahun']<=tahun[-1]) & (data['name'].isin(list(set(options+[negara]))))][['name','tahun','produksi']]
else:
    chart_data2 = data[(data['tahun']>=tahun[0]) & (data['tahun']<=tahun[-1])]

top10all = list(sorted(data.groupby('name')['produksi'].sum().sort_values(ascending=False).head(10).reset_index()['name'].values.tolist() + [negara]))
chart_data3 = data[data['name'].isin(top10all)].groupby('name')['produksi'].sum()

topyear = data[data['tahun'].isin(list(set(tahun)))].groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().sort_values(ascending=False).reset_index().iloc[0]#.sort_values(['produksi'],ascending=False)#.drop('tahun',axis=1).iloc[0]
topall = data.groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().sort_values(ascending=False).reset_index().iloc[0]

minyear = data[(data['tahun'].isin(list(set(tahun)))) & (data['produksi']>0)].sort_values('produksi').drop('tahun',axis=1).iloc[0]
minall = data.groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().reset_index()
minall = minall[minall['produksi']>0].sort_values(by='produksi').iloc[0]

zeroyear = data[(data['tahun'].isin(list(set(tahun)))) & (data['produksi']==0)].reset_index(drop=True).drop(['tahun','produksi'],axis=1)
zeroall = data.groupby(['name','kode_negara','region','sub-region'])['produksi'].sum().reset_index()
zeroall = zeroall[zeroall['produksi']==0].reset_index(drop=True).drop('produksi',axis=1)

st.header("Negara Produsen Minyak")
cola,colc = st.columns(2)

Y = sorted(set(tahun))
Y = Y[0] if len(Y)==1 else f"{Y[0]}-{Y[-1]}" 

with cola:
    st.subheader(f"Tertinggi Selama Tahun {Y}")
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

with colc:
    st.subheader(f"Terendah Selama Tahun {Y}")
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

st.header(f"Grafik Time-series Produksi Minyak {negara}")

ts = alt.Chart(chart_data1.reset_index()).mark_area(
    line={'color':'darkblue'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='white', offset=0),
               alt.GradientStop(color='darkblue', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    alt.X('tahun:T'),
    alt.Y('produksi:Q')
)

st.altair_chart(ts, use_container_width=True)


st.header(f"Perbandingan Jumlah Produksi Minyak")

col3, col4 = st.columns(2)

chart_data2 = chart_data2.fillna(0)

if len(chart_data2['tahun'].unique()) == 1 and options!=[]:
    gr = alt.Chart(chart_data2).mark_bar().encode(
        x='name:N',
        y='produksi:Q',
    )

else:
    chart_data2['tahun'] = pd.to_datetime(chart_data2['tahun'], format='%Y')
    gr = alt.Chart(chart_data2).mark_area().encode(
        x="tahun:T",
        y="produksi:Q",
        color="name:N"
    )

with col3:
    st.subheader(f'Perbandingan Produksi Tahun {Y}')
    st.altair_chart(gr, use_container_width=True)

with col4:
    st.subheader(f'Negara dengan Produksi Nol pada Tahun {Y}')
    st.dataframe(zeroyear)