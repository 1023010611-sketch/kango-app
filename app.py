import streamlit as st
import graphviz
import html
from diseases import SYSTEMS_DATA

st.set_page_config(
    page_title="看護病態関連図 自動生成システム Pro 100",
    page_icon="🏥",
    layout="wide"
)

CATEGORY_STYLES = {
    "原因": {"fillcolor": "#E3F2FD", "color": "#1565C0", "shape": "box", "style": "filled,rounded"},
    "病態": {"fillcolor": "#FFEBEE", "color": "#C62828", "shape": "box", "style": "filled,rounded"},
    "症状": {"fillcolor": "#FFF8E1", "color": "#F57F17", "shape": "box", "style": "filled,rounded"},
    "観察": {"fillcolor": "#E1F5FE", "color": "#0288D1", "shape": "box", "style": "filled,rounded"},
    "治療": {"fillcolor": "#E8F5E9", "color": "#2E7D32", "shape": "box", "style": "filled,rounded"},
    "影響": {"fillcolor": "#F3E5F5", "color": "#6A1B9A", "shape": "box", "style": "filled,rounded"},
    "看護問題": {"fillcolor": "#FFE0B2", "color": "#E65100", "shape": "box", "style": "filled,bold", "penwidth": "2.5"},
}

FONT_FAMILY = "Hiragino Sans, Yu Gothic, Meiryo, sans-serif"

def generate_graphviz_dot(disease_data):
    title = disease_data.get("title", "病態関連図")
    dot = graphviz.Digraph(name=title, format="svg", engine="dot")
    dot.attr(
        rankdir="TB", splines="ortho", nodesep="0.6", ranksep="0.8",
        fontname=FONT_FAMILY, fontsize="16", labelloc="t",
        label=f"<<B>{html.escape(title)}</B>>", bgcolor="#FFFFFF"
    )
    dot.attr("node", fontname=FONT_FAMILY, fontsize="11", margin="0.18,0.12")
    dot.attr("edge", fontname=FONT_FAMILY, fontsize="9", color="#555555", arrowhead="normal", penwidth="1.2")
    
    nodes = disease_data.get("nodes", {})
    for node_id, (label, cat) in nodes.items():
        style_info = CATEGORY_STYLES.get(cat, CATEGORY_STYLES["病態"])
        safe_label = html.escape(label).replace("\n", "<BR/>")
        html_label = f"<<FONT COLOR='{style_info['color']}'>{safe_label}</FONT>>"
        dot.node(node_id, label=html_label, shape=style_info["shape"], style=style_info["style"],
                 fillcolor=style_info["fillcolor"], color=style_info["color"], penwidth=style_info.get("penwidth", "1.5"))
        
    edges = disease_data.get("edges", [])
    for src, dst in edges:
        if dst.startswith("p") or src.startswith("p"):
            dot.edge(src, dst, color="#E65100", penwidth="2.3")
        elif src.startswith("o") or dst.startswith("o"):
            dot.edge(src, dst, color="#0288D1", penwidth="1.5", style="dashed")
        else:
            dot.edge(src, dst, color="#424242", penwidth="1.2")
            
    return dot

st.title("🏥 看護病態関連図 自動生成システム (100+疾患対応版)")
st.caption("系統と疾患を選択すると、解剖生理から看護診断までの因果関係を視覚化します。")

st.sidebar.header("📋 疾患データベース")
selected_system = st.sidebar.selectbox("系統を選択", list(SYSTEMS_DATA.keys()))
diseases_in_system = list(SYSTEMS_DATA[selected_system].keys())
selected_disease = st.sidebar.selectbox("疾患を選択", diseases_in_system)

data = SYSTEMS_DATA[selected_system][selected_disease]

st.subheader(f"📊 {data['title']}")
dot = generate_graphviz_dot(data)
st.graphviz_chart(dot.source, use_container_width=True)

with st.expander("📌 関連図ノード・アセスメント構成要素の一覧"):
    nodes = data.get("nodes", {})
    for nid, (lbl, cat) in nodes.items():
        st.write(f"・ **[{cat}]** {lbl.replace('\n', ' ')}")
