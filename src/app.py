# app.py
import streamlit as st
from streamlit_tags import st_tags
import pandas as pd
import json
from datetime import datetime
import re
from pathlib import Path
from HAL_search_api import fetch_hal_articles
# from facets_fetcher import fetch_facets


"""
    2️⃣ 部署到远程 / Streamlit Cloud

    这样别人就 不用本地 Python 环境 也能用：

    注册 Streamlit Cloud
    （有免费额度）

    将 app.py 和 hal_fetch.py 上传到 GitHub 仓库

    在 Streamlit Cloud 中选择你的仓库部署

    Streamlit 会自动安装依赖，生成网页链接

    用户打开网页即可操作，无需安装 Python 或任何库
"""


#====================缓存=========================#
##HAL
#code/streamlit.py
# facets/..
domain_file = Path(__file__).parent / "facets/domain_map.json"
lang_file = Path(__file__).parent / "facets/lang_map.json"
doctype_file= Path(__file__).parent / "facets/doctype_map.json"

@st.cache_data
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

DOMAIN_MAP = load_json(domain_file)
LANG_MAP=load_json(lang_file)
DOC_TYPE_MAP=load_json(doctype_file)


# 页面宽度设为 wide
st.set_page_config(page_title="HAL Articles Fetcher", page_icon="🛸", layout="wide")
st.title("Hal Articles Fetcher")

# 左右布局：左侧显示结果，右侧显示检索栏
left_col, right_col = st.columns([1, 1])  # 左:右 = 3:1

# ----------------------- 右侧检索栏 -----------------------

with left_col:

    st.subheader("Filtrer vos résultats")
    st.markdown("<br>", unsafe_allow_html=True)

    text = st_tags(
    label="📑Text",
    text="Tapez et 'Entrée' (chercher un texte dans tous les champs...)",
    value=[],
    suggestions=[],
    maxtags=10
    )

    # 文档类型
    doc_types = st.multiselect(
        "🗂️ Type de documents",
        options=list(DOC_TYPE_MAP.keys()),
        format_func=lambda x: DOC_TYPE_MAP[x],
        default=[]
    )

    domains = st.multiselect(
        "📌 Domaine",
        options=list(DOMAIN_MAP.keys()),
        format_func=lambda x: DOMAIN_MAP[x],
        default=[]
    )

    keywords = st_tags(
        label="💡 Mots-clés",
        text="Tapez et 'Entrée'",
        value=[],
        suggestions=[],
        maxtags=10
    )

    st.markdown("📅 Période")
    now = datetime.now()
    current_year, current_month = now.year, now.month
    years = [None] + list(range(current_year, 1901, -1))
    months = [None] + list(range(1, 13))

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox("Année début", years, index=years.index(2025))
    with col2:
        start_month = st.selectbox("Mois début", months, index=months.index(current_month-1))

    col3, col4 = st.columns(2)
    with col3:
        end_year = st.selectbox("Année fin", years, index=years.index(current_year))
    with col4:
        end_month = st.selectbox("Mois fin", months, index=months.index(current_month))

    # 日期校验
    invalid_date = False
    if start_year and start_month:
        if (end_year, end_month) < (start_year, start_month):
            st.error("⚠️ La fin est antérieur au début!")
            invalid_date = True

    # 语言、实验室
    languages = st.multiselect(
        "🌐 Langues",
        options=list(LANG_MAP.keys()),
        format_func=lambda x: LANG_MAP[x],
        default=[]
    )

    labs = st_tags(
        label="🔬 Laboratoire",
        text="Tapez et 'Entrée'",
        value=["Institut de Recherche en Gestion"],
        maxtags=10
    )

    # 输出字段
    default_fields = ['halId_s', "title_s", "subTitle_s", "authFullName_s","labStructName_s","domain_s", 
                      "publicationDate_s","journalTitle_s","conferenceTitle_s", "language_s", "keyword_s",
                      "abstract_s","urlFulltextEsr_s","files_s"]

    fields = st.multiselect(
        "🧾 Info à exporter",
        options=default_fields,
        default=default_fields
    )

    rows_range = list(range(0, 5001))
    max_records = st.selectbox("⬆️ Limite de requête une fois", rows_range, index=5000)

    st.markdown("<br>", unsafe_allow_html=True)

    
# ----------------------- 左侧结果区 -----------------------
with right_col:
    
    st.subheader("Commencer la requête")
    st.markdown("<br>", unsafe_allow_html=True)

    # 搜索按钮
    search_button = st.button("⚡ Chercher")

    if search_button and not invalid_date:
        with st.spinner("Chercher...⌛"):
            try:
                df = fetch_hal_articles(
                    start_year=start_year,
                    start_month=start_month,
                    end_year=end_year,
                    end_month=end_month,
                    doc_types=doc_types,
                    domains=domains,
                    keywords=keywords,
                    languages=languages,
                    labs=labs,
                    text=text,
                    fields=fields,
                    rows=100,
                    max_records=max_records
                )

                # 处理 domain
                if "domain_s" in df.columns:
                    def map_domains(codes_str):
                        if not codes_str: return ""
                        codes = codes_str.split(";")
                        mapped = []
                        for code in codes:
                            code_clean = re.sub(r"^\d+\.", "", code.strip())
                            mapped.append(DOMAIN_MAP.get(code_clean, code_clean))
                        return "; ".join(mapped)
                    df["domain_s"] = df["domain_s"].apply(map_domains)



                if df.empty:
                    st.warning("0 résultat!")
                else:
                    st.success(f"✅ {len(df)} articles trouvés!")
                    st.dataframe(df)

                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="💾 Télécharger",
                        data=csv_data,
                        file_name=f"hal_articles-{start_month}-{start_year}_{end_month}-{end_year}_{len(csv_data)}.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"⚠️ {e}")
