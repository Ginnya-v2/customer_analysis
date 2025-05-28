import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager


# フォントパスを指定
font_path = os.path.join(os.path.dirname(__file__), "Zen_Kaku_Gothic_New", "ZenKakuGothicNew-Regular.ttf")

# フォントプロパティを作成
font_prop = font_manager.FontProperties(fname=font_path)

# matplotlib にフォントを登録・適用
plt.rcParams['font.family'] = font_prop.get_name()
print(font_prop.get_name())



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ グラフを作成する関数 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# カード作成関数
def create_card(title, value, width=4, height=1, color='#0017C1'):
    fig = plt.figure(figsize=(width, height))
    fig.patch.set_facecolor(color)
    plt.axis('off')
    plt.text(0.5, 0.8, title, ha='center', fontsize=14, color='white',fontproperties=font_prop)
    plt.text(0.5, 0.1, f"{value:,}", ha='center', fontsize=24, color='white',fontproperties=font_prop)
    return fig

# ドーナッツグラフ作成関数
def create_donut_chart(data, title, labels, colors, font_colors=None, width=4, height=4):
    fig, ax = plt.subplots(figsize=(width, height))

    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.5),
        autopct='%1.1f%%',
        pctdistance=0.75
    )

    ax.axis('equal')
    ax.set_title(title,fontproperties=font_prop)

    # フォントカラーの設定
    if font_colors:
        for autotext, color in zip(autotexts, font_colors):
            autotext.set_color(color)

    # テキストのフォントサイズとプロパティを設定        
    for text in texts:
        text.set_fontsize(5)
        text.set_fontproperties(font_prop)

    # 🔶 図（fig）の周囲に枠線を追加
    fig.patch.set_edgecolor('#0017C1')   # 枠線の色
    fig.patch.set_linewidth(1)         # 枠線の太さ

    return fig

# 棒グラフ作成関数
def create_bar_chart(labels, sizes_percent, width=2, height=1):
    fig, ax = plt.subplots(figsize=(width, height), dpi=200)  # 🔸 高DPIにする

    # 棒グラフを描画
    ax.bar(
        labels,               # 横軸のラベル
        sizes_percent,        # 縦軸の値
        color='#0017C1'       # 棒の色
    )

    ax.set_title('年代別構成比',fontproperties=font_prop)     # タイトル
    ax.set_xlabel('年代',fontproperties=font_prop)           # 横軸ラベル
    ax.set_ylabel('構成比 (%)',fontproperties=font_prop)     # 縦軸ラベル

    # 🔸 軸の目盛（tick）にフォント適用
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)
        label.set_fontsize(7)

    # 軸目盛のフォントサイズ調整
    ax.tick_params(axis='both', labelsize=5)

    # 🔶 fig に枠線を追加
    fig.patch.set_edgecolor('#0017C1')
    fig.patch.set_linewidth(1)

    ax.margins(y=0.1)           # ✅ 余白を小さく
    fig.tight_layout()          # ✅ 自動レイアウト調整

    return fig


# 線グラフ作成関数
def create_line_chart(months, sizes_2019, sizes_2020, sizes_2021, width=5, height=2, dpi=200):
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)

    # データ描画（細線・小マーカー）
    ax.plot(months, sizes_2021, color='#0017C1', marker='d', markersize=2, linewidth=1, label='2021年')
    ax.plot(months, sizes_2020, color='#4979F5', marker='d', markersize=2, linewidth=1, label='2020年')
    ax.plot(months, sizes_2019, color='#9DB7F9', marker='d', markersize=2, linewidth=1, label='2019年')

    ax.set_title('月別件数推移', fontsize=6,fontproperties=font_prop)
    ax.set_xlabel('月', fontsize=5,fontproperties=font_prop)
    ax.set_ylabel('件数', fontsize=5,fontproperties=font_prop)

    ax.set_ylim(bottom=0)
    ax.tick_params(axis='x', labelsize=4, rotation=45)
    ax.tick_params(axis='y', labelsize=4)

    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), fontsize=5)

    fig.tight_layout()
    fig.patch.set_edgecolor('#0017C1')
    fig.patch.set_linewidth(0.5)
    
    # 凡例を作成しフォントを適用
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), fontsize=5)
    for text in legend.get_texts():
        text.set_fontproperties(font_prop)
        text.set_fontsize(5)

    # 🔸 軸の目盛（tick）にフォント適用
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)
        label.set_fontsize(4)
    return fig

def render_matplotlib_fig(fig, width=None, use_column_width=True, dpi=200):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches='tight')
    buf.seek(0)  # ポインタを先頭に戻す

    # 横幅指定とカラムフィットは排他的（両方は不可）
    if use_column_width:
        st.image(buf, use_container_width=True)
    else:
        st.image(buf, width=width)





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ データの読み込み ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
df = pd.read_csv('https://raw.githubusercontent.com/Ginnya-v2/customer_analysis/refs/heads/master/01_CustomerSubscriptionDataset/02_make_simple_dashboard/00_dataset/data.csv') #データが配置されている場所を指定





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 前処理 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 年代列を追加
df['年代'] = None # 年代列を作成する。（一時的にカラにしておく）
df['年代'] = df['年齢'] // 10 # 10で割って、小数点以下を切り捨てる（10の位の値を取得）
df['年代'] = df['年代'] * 10 # 10を掛ける
df['年代'] = df['年代'].astype(str) # 文字列に変換する
df['年代'] = df['年代'] + '代' # 代という文字を付け足す
# 年月列を追加
df['年'] = None # 年の列を作成する（一時的にカラにしておく）
df['年'] = df['日時'].str[:4] # .strで指定列の文字の値を取得する ⇨ [:4]で左から4文字目までの値を取得する
df['年'] = df['年'] + '年' # 年という文字を付け足す
df['月'] = None # 月の列を作成する（一時的にカラにしておく）
df['月'] = df['日時'].str[5:7] # .strで指定列の文字の値を取得する ⇨ [5:7]で左から5~6文字目までの値を取得する(「まで」は指定したい数の一つ上の数字を記載する)
df['月'] = df['月'] + '月' # 月という文字を付け足す
# レコード集計用の列を追加
df['件数'] = 1






#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ダッシュボード画面の表示 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Streamlitの設定
st.set_page_config(
    page_title="ダッシュボード",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)


#--- サイドバーにフィルタを設置 ---
# サイドバーのヘッダー
st.sidebar.header("🔍 フィルタ条件")

# 性別フィルタ（マルチセレクト）
sex_options = df['性別'].unique().tolist()
selected_sex = st.sidebar.multiselect("性別", options=sex_options, default=sex_options)

# 商品フィルタ（セレクトボックス）
product_options = df['商品'].unique().tolist()
selected_product = st.sidebar.multiselect("商品", options=product_options, default=product_options)

# 年代フィルタ（セレクトボックス）
age_options = df['年代'].unique().tolist()
selected_age = st.sidebar.multiselect("年代", options=age_options, default=age_options)

# 年フィルタ（セレクトボックス）
year_options = df['年'].unique().tolist()
selected_year = st.sidebar.multiselect("年", options=year_options, default=year_options)

# フィルタリング処理
df_filtered = df[df['性別'].isin(selected_sex)].copy()  # 選択された性別でフィルタリング
df_filtered = df_filtered[df_filtered['年代'].isin(selected_age)]  # 選択された年代でフィルタリング
df_filtered = df_filtered[df_filtered['商品'].isin(selected_product)]  # 選択された商品でフィルタリング
df_filtered = df_filtered[df_filtered['年'].isin(selected_year)]  # 選択された年でフィルタリング


#--- タイトルと説明 ---
st.title("ダッシュボード")
st.write("カスタマサポートのデータを可視化するダッシュボードです。")


#--- 1行目 ---
col1_1, col1_2, col1_3 = st.columns(3)

# カードの作成
value_card = df_filtered['件数'].sum() # 件数の合計を取得する
with col1_1:
    st.pyplot(create_card("カスタマサポート対応件数", value_card, width=3, height=1, color='#0017C1')) # カードを作成する

# フィルタ条件の表示（性別、商品）
with col1_2:
    col1_2_1,col1_2_2 = st.columns([1,2])
    with col1_2_1:
        st.write('性別')
        st.write('商品')
    with col1_2_2:
        st.badge("、".join(selected_sex)) # 選択された性別を表示
        st.badge("、".join(selected_product)) # 選択された商品を表示

# フィルタ条件の表示（年代、年）
with col1_3:
    col1_3_1,col1_3_2 = st.columns([1,2])
    with col1_3_1:
        st.write('年代')
        st.write('年')
    with col1_3_2:
        st.badge("、".join(selected_age)) # 選択された年代を表示
        st.badge("、".join(selected_year)) # 選択された年を表示


# --- 2行目 ---
col2_1, col2_2, col2_3 = st.columns(3)

# ドーナッツグラフ（性別構成比）
with col2_1:
    grouped = df_filtered.groupby('性別')['件数'].sum()
    fig = create_donut_chart(
        data=grouped.values,
        title="性別構成比",
        labels=grouped.index.tolist(),
        colors=['#0017C1', '#D9E6FF'],
        font_colors=['white', 'black'],
        width=3,
        height=3
    )
    render_matplotlib_fig(fig, use_column_width=True)  # ← ここで余白を持たせた描画

# ドーナッツグラフ（商品別構成比）
with col2_2:
    grouped = df_filtered.groupby('商品')['件数'].sum()
    st.pyplot(create_donut_chart(
        data=grouped.values,
        title="商品別構成比",
        labels=grouped.index.tolist(),
        colors=['#0017C1', '#D9E6FF'],
        font_colors=['white', 'black'],
        width=3,
        height=3
    ))

# 棒グラフ（年代別構成比）
with col2_3:
    grouped = df_filtered.groupby('年代')['件数'].sum()
    st.pyplot(create_bar_chart(
        labels=grouped.index.tolist(),
        sizes_percent=grouped.values,
        width=3,
        height=2.47
    ))


# --- 3行目 ---
# 月別件数推移グラフ

# 月・年別に件数を集計した前提（例）
df_tmp = df_filtered.groupby(['年', '月'])['件数'].sum().reset_index()
df_pivot = df_tmp.pivot(index='月', columns='年', values='件数').fillna(0)

# 月順に並べ替え（01月～12月）
month_order = sorted(df_pivot.index, key=lambda x: int(x.replace('月', '')))
df_pivot = df_pivot.loc[month_order]

months = df_pivot.index.tolist()
sizes_2019 = df_pivot.get('2019年', pd.Series([0]*len(months))).tolist()
sizes_2020 = df_pivot.get('2020年', pd.Series([0]*len(months))).tolist()
sizes_2021 = df_pivot.get('2021年', pd.Series([0]*len(months))).tolist()

# グラフ作成 & 表示
fig = create_line_chart(months, sizes_2019, sizes_2020, sizes_2021)
render_matplotlib_fig(fig, width=1600, use_column_width=False)
