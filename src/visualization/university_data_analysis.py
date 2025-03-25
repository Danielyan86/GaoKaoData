import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc
import numpy as np


def estimate_missing_values(data):
    """
    估算缺失的硕士生和博士生数据
    基于硕博合计和已知数据的比例进行估算
    """
    df = pd.DataFrame(data)

    # 计算已知数据的平均比例
    known_ratio = df[df["硕士生"].notna()][["硕士生", "博士生", "硕博合计"]].copy()
    avg_master_ratio = (known_ratio["硕士生"] / known_ratio["硕博合计"]).mean()
    avg_phd_ratio = (known_ratio["博士生"] / known_ratio["硕博合计"]).mean()

    # 估算缺失值
    for idx in df.index:
        if pd.isna(df.loc[idx, "硕士生"]):
            total = df.loc[idx, "硕博合计"]
            df.loc[idx, "硕士生"] = int(total * avg_master_ratio)
            df.loc[idx, "博士生"] = int(total * avg_phd_ratio)

    return df


def create_university_table(data_file):
    """
    Create an interactive table visualization from university data with heatmap effect
    """
    # Read data from Excel/CSV file
    df = pd.read_excel(data_file)

    # 将 NaN 值替换为 "null" 字符串
    df = df.fillna("null")

    # 使用 plotly 的内置配色方案生成渐变色
    n_colors = 10  # 渐变色数量
    ratio_colors = pc.sample_colorscale(
        "Reds", [i / (n_colors - 1) for i in range(n_colors)]
    )
    ratio_colors = ratio_colors[::-1]  # 反转颜色列表，使较大值颜色更深

    min_ratio = df["研本比"].min()
    max_ratio = df["研本比"].max()

    # 创建颜色列表，只对研本比列应用热力图
    cell_colors = [[None] * len(df.columns) for _ in range(len(df))]
    ratio_col_idx = df.columns.get_loc("研本比")

    for i in range(len(df)):
        ratio = df["研本比"].iloc[i]
        normalized_ratio = (ratio - min_ratio) / (max_ratio - min_ratio)
        color_idx = int(normalized_ratio * (len(ratio_colors) - 1))
        cell_colors[i][ratio_col_idx] = ratio_colors[color_idx]

    # Create table figure
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color="rgb(0, 32, 96)",  # 深蓝色表头，匹配原图
                    font=dict(color="white", size=14, family="SimHei"),
                    align="center",
                    height=40,
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],
                    fill_color=[
                        [
                            "rgb(245, 247, 250)" if col != "研本比" else color
                            for color in [
                                cell_colors[i][ratio_col_idx] for i in range(len(df))
                            ]
                        ]
                        for col in df.columns
                    ],
                    font=dict(
                        size=13,
                        family="SimHei",
                        color=[
                            [
                                "rgb(128, 128, 128)" if str(val) == "null" else "black"
                                for val in df[col]
                            ]
                            for col in df.columns
                        ],
                    ),
                    align="center",
                    height=35,
                    line=dict(color="rgb(220, 220, 220)", width=1),  # 添加单元格边框
                ),
            )
        ]
    )

    # 更新布局
    fig.update_layout(
        title=dict(
            text="2024年研究生/本科生比排名",
            font=dict(size=24, family="SimHei"),
            y=0.95,
        ),
        width=1200,
        height=800,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=80, l=40, r=40, b=40),
    )

    return fig


def create_ratio_bar_chart(df):
    """
    Create a bar chart showing 研本比 for top universities with gradient effect
    """
    # 使用 plotly express 的内置配色方案
    fig = px.bar(
        df.head(20),
        x="院校名称",
        y="研本比",
        text="研本比",
        color="研本比",
        color_continuous_scale="Reds",  # 使用红色渐变
        title="2024年高校研究生与本科生比例排名（前20名）",
    )

    # 更新布局
    fig.update_layout(
        title=dict(
            text="2024年高校研究生与本科生比例排名（前20名）",
            font=dict(size=20, family="SimHei"),
            y=0.95,
        ),
        xaxis=dict(
            title="院校名称",
            tickangle=-45,
            tickfont=dict(size=12, family="SimHei"),
            title_font=dict(size=14, family="SimHei"),
        ),
        yaxis=dict(
            title="研究生与本科生比例",
            tickfont=dict(size=12, family="SimHei"),
            title_font=dict(size=14, family="SimHei"),
            gridcolor="rgba(189, 195, 199, 0.2)",
        ),
        height=700,
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(t=100, l=80, r=80, b=100),
    )

    # 更新文本标签位置和格式
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    # 添加参考线
    fig.add_hline(
        y=df["研本比"].mean(),
        line_dash="dash",
        line_color="rgba(52, 73, 94, 0.5)",
        annotation_text="平均值",
        annotation_font=dict(family="SimHei"),
    )

    # 移除颜色条
    fig.update_coloraxes(showscale=False)

    return fig


def save_figure(fig, base_name):
    """
    Save figure in both HTML and static image formats
    """
    # 保存为HTML（交互式）
    fig.write_html(f"{base_name}.html")

    # 保存为PNG（静态图片）
    fig.write_image(f"{base_name}.png", scale=2)  # scale=2 提供更高的分辨率

    # 保存为PDF（适合打印）
    fig.write_image(f"{base_name}.pdf")


def main():
    # 完整数据，包含所有列
    data = {
        "排名": list(range(1, 36)),  # 扩展到35所高校
        "属性": ["985"] * 17 + ["211"] * 3 + ["985"] * 10 + ["211"] * 5,
        "院校名称": [
            "北京大学",
            "复旦大学",
            "清华大学",
            "南京大学",
            "北京理工大学",
            "华东师范大学",
            "中国人民大学",
            "同济大学",
            "北京航空航天大学",
            "西安交通大学",
            "西北工业大学",
            "天津大学",
            "电子科技大学",
            "浙江大学",
            "厦门大学",
            "南开大学",
            "中国农业大学",
            "中山大学",
            "北京科技大学",
            "上海大学",
            "西北大学",
            "兰州大学",
            "东北大学",
            "中国海洋大学",
            "哈尔滨工业大学（三区）",
            "武汉大学",
            "对外经济贸易大学",
            "云南大学",
            "大连理工大学",
            "北京师范大学（珠海）",
            "华东理工大学",
            "中国政法大学",
            "北京邮电大学",
            "湖南大学",
            "中央财经大学",
        ],
        "本科生": [
            3389,
            4337,
            3800,
            4038,
            3900,
            3740,
            2945,
            4436,
            4378,
            6229,
            4388,
            4909,
            5041,
            6503,
            5364,
            4193,
            3687,
            8255,
            3530,
            4781,
            3447,
            5054,
            5075,
            4590,
            7934,
            7325,
            2269,
            5082,
            6350,
            1923,
            4262,
            2274,
            3930,
            5631,
            2535,
        ],
        "硕士生": [
            6936,
            None,
            None,
            None,
            None,
            None,
            None,
            5919,
            None,
            None,
            5686,
            None,
            6669,
            None,
            None,
            4506,
            3989,
            None,
            3925,
            6056,
            4325,
            5363,
            5534,
            4930,
            None,
            6774,
            2580,
            5536,
            6349,
            2001,
            4180,
            None,
            None,
            5178,
            2636,
        ],
        "博士生": [
            3867,
            None,
            None,
            None,
            None,
            None,
            None,
            2212,
            None,
            None,
            1705,
            None,
            1258,
            None,
            None,
            1617,
            1380,
            None,
            1094,
            731,
            494,
            1352,
            1143,
            954,
            None,
            2426,
            229,
            661,
            1389,
            335,
            901,
            None,
            None,
            1328,
            240,
        ],
        "硕博合计": [
            10803,
            12321,
            9000,
            8848,
            8000,
            7670,
            5500,
            8131,
            7866,
            11129,
            7391,
            8200,
            7927,
            10000,
            8093,
            6123,
            5369,
            12000,
            5019,
            6787,
            4819,
            6715,
            6677,
            5884,
            10000,
            9200,
            2809,
            6197,
            7738,
            2336,
            5081,
            2700,
            4560,
            6506,
            2876,
        ],
        "研本比": [
            3.19,
            2.84,
            2.37,
            2.19,
            2.05,
            2.05,
            1.87,
            1.83,
            1.80,
            1.79,
            1.68,
            1.67,
            1.57,
            1.54,
            1.51,
            1.46,
            1.46,
            1.45,
            1.42,
            1.42,
            1.40,
            1.33,
            1.32,
            1.28,
            1.26,
            1.26,
            1.24,
            1.22,
            1.22,
            1.21,
            1.19,
            1.19,
            1.16,
            1.16,
            1.13,
        ],
    }

    # 估算缺失值
    df = estimate_missing_values(data)

    # 保存完整数据到Excel
    df.to_excel("university_data.xlsx", index=False)

    # Create visualizations
    table_fig = create_university_table("university_data.xlsx")
    ratio_fig = create_ratio_bar_chart(df)

    # 保存为多种格式
    save_figure(table_fig, "university_table")
    save_figure(ratio_fig, "ratio_chart")


if __name__ == "__main__":
    main()
