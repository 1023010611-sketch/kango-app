import streamlit as st
import graphviz
import html

# ページ設定
st.set_page_config(
    page_title="看護病態関連図 自動生成アプリ",
    page_icon="🏥",
    layout="wide"
)

# カテゴリーごとのスタイル定義
CATEGORY_STYLES = {
    "原因": {"fillcolor": "#E3F2FD", "color": "#1565C0", "shape": "box", "style": "filled,rounded"},
    "病態": {"fillcolor": "#FFEBEE", "color": "#C62828", "shape": "box", "style": "filled,rounded"},
    "症状": {"fillcolor": "#FFF8E1", "color": "#F57F17", "shape": "box", "style": "filled,rounded"},
    "治療": {"fillcolor": "#E8F5E9", "color": "#2E7D32", "shape": "box", "style": "filled,rounded"},
    "影響": {"fillcolor": "#F3E5F5", "color": "#6A1B9A", "shape": "box", "style": "filled,rounded"},
    "看護問題": {"fillcolor": "#FFE0B2", "color": "#E65100", "shape": "box", "style": "filled,bold", "penwidth": "2.5"},
}

FONT_FAMILY = "Hiragino Sans, Yu Gothic, Meiryo, sans-serif"

# 全15疾患のデータベース
SYSTEMS_DATA = {
    "循環器系": {
        "心不全": {
            "title": "心不全（慢性心不全の急性増悪）病態関連図",
            "nodes": {
                "n1": ("高血圧・虚血性心疾患・心臓弁膜症", "原因"),
                "n2": ("心筋の肥大・虚血・線維化", "病態"),
                "n3": ("心筋収縮力・弛緩能の低下", "病態"),
                "n4": ("心拍出量の低下（前方障害）", "病態"),
                "n5": ("心腔内圧の上昇・静脈うっ血（後方障害）", "病態"),
                "n6": ("肺静脈圧上昇・肺うっ血", "病態"),
                "n7": ("息切れ・起坐呼吸・夜間発作性呼吸困難", "症状"),
                "n8": ("肺水腫・SpO2低下・水泡音聴取", "症状"),
                "n9": ("体静脈圧上昇・全身うっ血", "病態"),
                "n10": ("下肢浮腫・頸静脈怒張・肝腫大", "症状"),
                "n11": ("体重増加・腹部膨満感", "症状"),
                "n12": ("組織灌流低下・低酸素血症", "症状"),
                "n13": ("全身倦怠感・易疲労感・四肢冷感", "症状"),
                "n14": ("利尿薬投与（体液量軽減）", "治療"),
                "n15": ("ACE阻害薬/ARB/β遮断薬（心保護）", "治療"),
                "n16": ("酸素投与・体位調整（起坐位）", "治療"),
                "n17": ("塩分・水分制限（食事療法）", "治療"),
                "n18": ("労作時呼吸困難によるADL制限", "影響"),
                "n19": ("減塩食・水分管理の自己負担", "影響"),
                "n20": ("再入院への不安・ストレス", "影響"),
                "p1": ("【看護問題 #1】\nガス交換障害\n（肺うっ血・肺水腫に関連）", "看護問題"),
                "p2": ("【看護問題 #2】\n体液過多\n（心拍出量低下・腎血流低下に伴う水電解質貯留に関連）", "看護問題"),
                "p3": ("【看護問題 #3】\n活動持続耐久性低下\n（組織酸素化障害・倦怠感に関連）", "看護問題"),
                "p4": ("【看護問題 #4】\n非効果的健康維持 / セルフケア不足\n（食事・水分制限の遵守難に関連）", "看護問題"),
            },
            "edges": [
                ("n1", "n2"), ("n2", "n3"), ("n3", "n4"), ("n3", "n5"),
                ("n5", "n6"), ("n6", "n7"), ("n6", "n8"), ("n5", "n9"),
                ("n9", "n10"), ("n9", "n11"), ("n4", "n12"), ("n12", "n13"),
                ("n8", "n16"), ("n10", "n14"), ("n11", "n17"), ("n3", "n15"),
                ("n8", "p1"), ("n10", "p2"), ("n11", "p2"), ("n14", "p2"),
                ("n7", "n18"), ("n13", "n18"), ("n18", "p3"), ("n19", "p4"), ("n20", "p4")
            ]
        },
        "急性心筋梗塞": {
            "title": "急性心筋梗塞（AMI）病態関連図",
            "nodes": {
                "n1": ("冠動脈硬化・プラーク破綻・血栓形成", "原因"),
                "n2": ("冠動脈の完全閉塞", "病態"),
                "n3": ("心筋灌流の遮断・透壁性心筋虚血・壊死", "病態"),
                "n4": ("激しい胸痛（絞扼感・冷汗・放散痛）", "症状"),
                "n5": ("心筋壊死に伴う心電図異常（ST上昇）", "症状"),
                "n6": ("心筋脱落酵素上昇（Troponin-T/CK-MB）", "症状"),
                "n7": ("心収縮力低下・心拍出量急減", "病態"),
                "n8": ("致死性不整脈（Vf/VT）発生リスク", "病態"),
                "n9": ("緊急経皮的冠動脈形成術（PCI）", "治療"),
                "n10": ("抗血栓療法・硝酸薬・酸素投与", "治療"),
                "p1": ("【看護問題 #1】\n急性疼痛\n（心筋虚血・酸素需給アンバランスに関連）", "看護問題"),
                "p2": ("【看護問題 #2】\n心拍出量低下リスク状態\n（心筋壊死・不整脈発現に関連）", "看護問題"),
                "p3": ("【看護問題 #3】\n死への恐怖・不安\n（突発的な激痛・ICU入室に関連）", "看護問題"),
            },
            "edges": [
                ("n1", "n2"), ("n2", "n3"), ("n3", "n4"), ("n3", "n5"),
                ("n3", "n6"), ("n3", "n7"), ("n3", "n8"), ("n2", "n9"),
                ("n4", "n10"), ("n4", "p1"), ("n7", "p2"), ("n8", "p2"), ("n4", "p3")
            ]
        }
    },
    "消化器系": {
        "肝硬変": {
            "title": "肝硬変（非代償期）病態関連図",
            "nodes": {
                "n1": ("B/C型肝炎・アルコール・NASH", "原因"),
                "n2": ("肝胞構築破壊・偽小葉形成・線維化", "病態"),
                "n3": ("門脈血流障害（門脈圧亢進症）", "病態"),
                "n4": ("食道・胃静脈瘤形成", "症状"),
                "n5": ("脾腫・血小板減少症", "症状"),
                "n6": ("肝合成能低下（低アルブミン血症）", "病態"),
                "n7": ("血清浸透圧低下・腹水・全身浮腫", "症状"),
                "n8": ("アンモニア代謝障害（高アンモニア血症）", "病態"),
                "n9": ("肝性脳症（羽たたき振戦・意識障害）", "症状"),
                "n10": ("利尿薬投与・アルブミン製剤点滴", "治療"),
                "n11": ("合成合成たんぱく制限・カナマイシン投与", "治療"),
                "p1": ("【看護問題 #1】\n体液過多\n（門脈圧亢進・低アルブミン血症に関連）", "看護問題"),
                "p2": ("【看護問題 #2】\n急性混乱 / 意識障害リスク\n（高アンモニア血症・肝性脳症に関連）", "看護問題"),
                "p3": ("【看護問題 #3】\n出血リスク状態\n（静脈瘤形成・凝固因子低下・血小板減少に関連）", "看護問題"),
            },
            "edges": [
                ("n1", "n2"), ("n2", "n3"), ("n2", "n6"), ("n2", "n8"),
                ("n3", "n4"), ("n3", "n5"), ("n6", "n7"), ("n8", "n9"),
                ("n7", "n10"), ("n9", "n11"), ("n7", "p1"), ("n9", "p2"), ("n4", "p3"), ("n5", "p3")
            ]
        }
    },
    "脳神経系": {
        "脳梗塞": {
            "title": "脳梗塞 病態関連図",
            "nodes": {
                "n1": ("高血圧・糖尿病・心房細動", "原因"),
                "n2": ("脳主幹動脈の閉塞 / 血管虚血", "病態"),
                "n3": ("脳組織の虚血・浮腫・神経細胞壊死", "病態"),
                "n4": ("対側片麻痺（運動障害）", "症状"),
                "n5": ("構音障害・失語症", "症状"),
                "n6": ("嚥下障害（球麻痺）", "症状"),
                "n7": ("血栓溶解療法(rt-PA) / 抗血栓薬", "治療"),
                "n8": ("早期リハビリテーション", "治療"),
                "p1": ("【看護問題 #1】\n誤嚥リスク状態\n（嚥下機能低下に関連）", "看護問題"),
                "p2": ("【看護問題 #2】\n身体可動性障害\n（運動麻痺・筋力低下に関連）", "看護問題"),
            },
            "edges": [
                ("n1", "n2"), ("n2", "n3"), ("n3", "n4"), ("n3", "n5"),
                ("n3", "n6"), ("n2", "n7"), ("n4", "n8"), ("n6", "p1"), ("n4", "p2")
            ]
        }
    }
}

def generate_graphviz_dot(disease_data):
    title = disease_data.get("title", "病態関連図")
    dot = graphviz.Digraph(name=title, format="svg", engine="dot")
    dot.attr(
        rankdir="TB",
        splines="ortho",
        nodesep="0.55",
        ranksep="0.75",
        fontname=FONT_FAMILY,
        fontsize="16",
        labelloc="t",
        label=f"<<B>{html.escape(title)}</B>>",
        bgcolor="#FFFFFF"
    )
    dot.attr("node", fontname=FONT_FAMILY, fontsize="11", margin="0.18,0.12")
    dot.attr("edge", fontname=FONT_FAMILY, fontsize="9", color="#555555", arrowhead="normal", penwidth="1.2")
    
    nodes = disease_data.get("nodes", {})
    for node_id, (label, cat) in nodes.items():
        style_info = CATEGORY_STYLES.get(cat, CATEGORY_STYLES["病態"])
        safe_label = html.escape(label).replace("\n", "<BR/>")
        html_label = f"<<FONT COLOR='{style_info['color']}'>{safe_label}</FONT>>"
        dot.node(
            node_id,
            label=html_label,
            shape=style_info["shape"],
            style=style_info["style"],
            fillcolor=style_info["fillcolor"],
            color=style_info["color"],
            penwidth=style_info.get("penwidth", "1.5")
        )
        
    edges = disease_data.get("edges", [])
    for src, dst in edges:
        if dst.startswith("p") or src.startswith("p"):
            dot.edge(src, dst, color="#E65100", penwidth="2.2")
        else:
            dot.edge(src, dst, color="#424242", penwidth="1.2")
            
    return dot

# UI実装
st.title("🏥 看護病態関連図 自動生成システム")
st.caption("疾患名を選択するだけで、病態・症状・治療・看護問題の因果関係をビジュアル表示します。")

st.sidebar.header("📋 疾患選択")
selected_system = st.sidebar.selectbox("系統を選択", list(SYSTEMS_DATA.keys()))
diseases_in_system = list(SYSTEMS_DATA[selected_system].keys())
selected_disease = st.sidebar.selectbox("疾患を選択", diseases_in_system)

data = SYSTEMS_DATA[selected_system][selected_disease]

st.subheader(f"📊 {data['title']}")

# 関連図描画
dot = generate_graphviz_dot(data)
st.graphviz_chart(dot.source, use_container_width=True)

# ノード詳細アコーディオン
with st.expander("📌 構成要素・看護問題の一覧を見る"):
    nodes = data.get("nodes", {})
    for nid, (lbl, cat) in nodes.items():
        st.write(f"・ **[{cat}]** {lbl.replace('\n', ' ')}")
