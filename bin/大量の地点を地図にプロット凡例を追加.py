import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# csvデータをローカルからダウンロード
df = pd.read_csv("/home/ec2-user/environment/observation/SYNOP/program/LongCalculation/Temp/graph/plotly/deviation/Max/hensa_Max_01.csv")

# maxtempの値に基づいて色を返す関数
def get_color(MaxTemp_minus_temp):
    if MaxTemp_minus_temp < 5:
        return 'gray'
    elif MaxTemp_minus_temp < 10:
        return 'green'
    elif MaxTemp_minus_temp < 20:
        return 'yellow'
    elif MaxTemp_minus_temp < 30:
        return 'darkorange'
    elif MaxTemp_minus_temp < 100:
        return 'red'
    else:
        return 'magenta'

# カラーカラムをDataFrameに追加
df['color'] = df['MaxTemp_minus_temp'].apply(get_color)

# Scattermapboxを生成
fig = px.scatter_mapbox(df, lat='lat', lon='lon', color='color',
                        mapbox_style='carto-positron', 
                        color_discrete_map='identity')

# Add dummy traces for the custom legend
legend_labels = ["<5", "5≦ <10", "10≦ <20", "20≦ <30", "30≦ <100", ">100"]
colors = ['gray', 'green', 'yellow', 'darkorange', 'red', 'magenta']

for label, color in zip(legend_labels, colors):
    fig.add_trace(go.Scattermapbox(
        lat=[None], # no points to show 
        lon=[None], 
        mode='markers',
        marker=go.scattermapbox.Marker(size=0, color=color), 
        showlegend=True,
        name=label
    ))

# fig.show()
fig.write_html("AveMax01.html")