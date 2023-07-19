# This is v2
# streamlit run main.py
# https://github.com/0xnanako/ma-database-test.git
import pathlib
import datetime
import time
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder
from PIL import Image



df = pd.read_csv("log_00.csv")
df['Name_Link'] = df['名前'] +'$'+ df['LINE NFT']
df=df[['Token type',
       'Name_Link',
       'Total tokens',
       'Supply',
       'Holders',
       'WeeklyTx',
       'imgURL',
       'シリーズ',
       'カテゴリ',
       '名前']]
st.set_page_config(page_title = "シール図鑑",
                   page_icon = '📚',
                   layout="centered")

# タイトルを表示する
st.title('シール図鑑')

# 更新日を表示する
p = pathlib.Path('log_00.csv')
dt = datetime.datetime.fromtimestamp(p.stat().st_mtime)
st.text("更新日 " + dt.strftime('%Y年%m月%d日 %H:%M:%S'))

# 詳細を検索
with st.expander("フィルター"):
    # シール名を検索
    search_title = st.text_input('シール名', '',key="str")
    df = df[df['名前'].str.contains(search_title)]
    #カテゴリにある全ての項目をリスト化する
    category_list = list(df['カテゴリ'].unique())
    category_selected = st.multiselect('カテゴリを選択', category_list, default= category_list)
    df = df[(df['カテゴリ'].isin(category_selected))]
    #シリーズにある全ての項目をリスト化する
    series_list = list(df['シリーズ'].unique())
    series_selected = st.multiselect('シリーズを選択', series_list, default=series_list)
    df = df[(df['シリーズ'].isin(series_selected))]
    
Renderer_Name = JsCode("""
        class Renderer_Name {
          init(params) {
            const[name,link] = params.value.split("$");
            this.eGui = document.createElement('a');
            this.eGui.innerText = name;
            this.eGui.setAttribute('href', link);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)

Render_Tokentype = JsCode("""
        class Renderer_TokenType {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = params.value;
            this.eGui.setAttribute('href', "https://explorer.blockchain.line.me/finschia/item-token-type/db8c702e/"+params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)

gd=GridOptionsBuilder.from_dataframe(df)
gd.configure_default_column(groupable=True, 
                            value=True, 
                            enableRowGroup=True,
                            floatingFilter = True,)
gd.configure_column("Token type", "Token",
                    cellRenderer=Render_Tokentype,
                    minWidth = 110,
                    maxWidth = 110)
gd.configure_column("Name_Link", "名前",
                    cellRenderer=Renderer_Name,
                    minWidth = 150,
                    maxWidth = 350
                    )
nums_list = ['Total tokens',
             'Supply','Holders',
             'WeeklyTx']
width_num = 85
gd.configure_columns(nums_list,
                     minWidth = width_num,
                     maxWidth = width_num
                     )

gd.configure_column("Total tokens", "Total",)
gd.configure_column("WeeklyTx", "7dTx",)

hide_list=['名前','imgURL','カテゴリ','シリーズ']
gd.configure_columns(hide_list, hide = True)

gd.configure_selection(selection_mode="single", 
                       use_checkbox=True, 
                       pre_selected_rows = [0])

gd.configure_grid_options(rowHeight=28)
gd.configure_auto_height(False)
gridoptions=gd.build()

# dataframeを表示する
grid = AgGrid(df, 
       gridOptions=gridoptions, 
       theme = "streamlit",
       allow_unsafe_jscode=True, 
       fit_columns_on_grid_load=True,
       height = 600
       )

# サイドバーの表示設定

sel_row = grid["selected_rows"]
if sel_row:
    st.sidebar.write (sel_row[0]['名前'])
    st.sidebar.image (sel_row[0]['imgURL'])
    
    side_list = [sel_row[0]['Token type'],
                 sel_row[0]['カテゴリ'],
                 sel_row[0]['シリーズ'],
                 sel_row[0]['Total tokens'],
                 sel_row[0]['Supply'],
                 sel_row[0]['Holders'],
                 sel_row[0]['WeeklyTx'],
                     ]
    side_df = pd.DataFrame(side_list)
    side_df.index = ['Token type',
                     'カテゴリ',
                     'シリーズ',
                     'Total tokens',
                     'Supply',
                     'Holders',
                     'WeeklyTx']
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    
    st.sidebar.dataframe(side_df, use_container_width = True)
    