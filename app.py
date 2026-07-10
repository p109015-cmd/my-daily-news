import streamlit as st
import requests
from xml.etree import ElementTree
import datetime

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 智慧每日新聞 Pro+", page_icon="📰", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 v2.0 | 核心技術：多來源穩定新聞流擷取技術")

st.title("📰 AI 智慧每日新聞助理 Pro+")
st.write("本系統已連線至華視新聞及科技頭條，即時抓取最新、最準確的焦點頭條！")

# 獲取今天日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 **今天是：{today}** | 正在為總工程師準備即時簡報...")
st.write("---")

# 2. 核心技術：全自動新聞 RSS 爬蟲函式
@st.cache_data(ttl=300) # 快取 5 分鐘
def fetch_latest_news(rss_url):
    news_items = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 移除可能導致解析失敗的空白字元
        xml_text = response.text.strip()
        
        # 進行 XML 解析
        root = ElementTree.fromstring(xml_text)
        
        # 尋找 XML 中的新聞項目
        items = root.findall('.//item')
            
        for item in items[:8]: # 抓取最新 8 則
            title_node = item.find('title')
            link_node = item.find('link')
            date_node = item.find('pubDate')
            desc_node = item.find('description')
            
            title = title_node.text if title_node is not None else "最新消息"
            link = link_node.text if link_node is not None else "#"
            pub_date = date_node.text if date_node is not None else today
            description = desc_node.text if desc_node is not None else "點擊鏈結查看全文"
            
            # 清理摘要中的 HTML 標籤（常見於華視或科技新聞）
            if description:
                import re
                description = re.sub('<[^<]+?>', '', description) # 用正規表達式拔掉 HTML 標籤
            
            # 格式化日期，只保留到分鐘
            if pub_date:
                pub_date = pub_date.replace(" +0800", "").replace(" GMT", "")
            
            news_items.append({
                "title": title,
                "link": link,
                "date": pub_date,
                "summary": description
            })
            
    except Exception as e:
        st.error(f"⚠️ 該線路暫時堵塞，請點擊同步按鈕或切換分類。錯誤：{e}")
    return news_items

# 3. 更換為極度穩定的全新新聞來源
category_dict = {
    "🔥 華視．即時重大焦點": "https://news.cts.com.tw/rss/news.xml",
    "💻 TechNews．科技新報": "https://technews.tw/feed/",
    "🌍 華視．全球國際大事": "https://news.cts.com.tw/rss/international.xml",
    "📈 華視．財經金融頭條": "https://news.cts.com.tw/rss/finance.xml",
    "🇹🇼 華視．台灣政治要聞": "https://news.cts.com.tw/rss/politics.xml"
}

selected_category = st.selectbox("🎯 請選擇您想關心的焦點領域：", list(category_dict.keys()))
rss_url = category_dict[selected_category]

# 4. 渲染新聞畫面
if st.button("🔄 立即同步最新頭條", use_container_width=True) or selected_category:
    with st.spinner("正在安全連線新聞伺服器，擷取最新大數據簡報..."):
        news_list = fetch_latest_news(rss_url)
        
        if news_list:
            st.success(f"🎉 成功撈出 {len(news_list)} 則實時焦點新聞！")
            st.write("")
            
            for idx, news in enumerate(news_list):
                with st.container(border=True):
                    # 新聞標題
                    st.markdown(f"### **[{idx+1}] {news['title']}**")
                    
                    # 時間標籤
                    st.caption(f"🕒 發布時間：{news['date']}")
                    
                    # 摘要限制
                    clean_summary = news['summary'] if news['summary'] else "無內文摘要"
                    if len(clean_summary) > 150:
                        clean_summary = clean_summary[:150] + "..."
                    st.write(f"📝 **新聞大綱摘要：** {clean_summary}")
                    
                    # 傳送門
                    st.markdown(f"[🔗 點我閱讀官方完整報導]({news['link']})")
        else:
            st.error("目前獲取到的資料有誤，請嘗試切換其他分類管道！")

st.write("\n---")
st.caption("⚡ Powered by Streamlit & Multi-source RSS Crawler")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 媒體串接專案，非經授權請勿複製。")
