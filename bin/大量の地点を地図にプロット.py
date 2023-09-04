#installする方法
#pip install plotly

import pandas as pd
import plotly.express as px

# サンプルデータのロード（データを適切なパスからロードしてください）
data = """
utc,lat,lon,maxtemp
2023/1/1,30,25,20
2023/1/2,25,20,-25
2023/1/3,28,24,35
"""
#csvデータをローカルからダウンロード
df = pd.read_csv("/test/test.csv")


# maxtempの値に基づいて色を返す関数
def get_color(temp):
    if temp <= -30:
        return 'purple'
    elif temp <= -20:
        return 'blue'
    elif temp <= -10:
        return 'lightblue'
    elif temp < 10:
        return 'gray'
    elif temp < 20:
        return 'green'
    elif temp < 30:
        return 'orange'
    elif temp < 40:
        return 'tomato'
    else:
        return 'magenta'

# カラーカラムをDataFrameに追加
df['color'] = df['maxtemp'].apply(get_color)

# Scattermapboxを生成
fig = px.scatter_mapbox(df, lat='lat', lon='lon', color='color',
                        mapbox_style='carto-positron', 
                        color_discrete_map='identity')

#fig.show()
fig.write_html("output_map.html")