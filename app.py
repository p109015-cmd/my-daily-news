import streamlit as st
import requests
from xml.etree import ElementTree
import datetime

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 智慧每日新聞", page_icon="📰", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 v1.0 | 核心技術：RSS 即時新聞爬蟲與動態排版技術")

st.title("📰 AI 智慧每日新聞助理")
st.write("本系統連線至國家級通訊社（中央社），即時抓取最新、最準確的焦點頭條，拒絕垃圾農場文！")

# 獲取今天日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 **今天是：{today}** | 正在為總工程師準備即時簡報...")
st.write("---")

# 2. 核心技術：即時新聞 RSS 爬蟲函式
@st.cache_data(ttl=600) # 快取 10 分鐘，避免頻繁請求被新聞網站封鎖
def fetch_latest_news(rss_url):
    news_items = []
    try:
        response = requests.get(rss_url, timeout=10)
        response.encoding = 'utf-8'
        # 解析 XML 格式的新聞資料
        root = ElementTree.fromstring(response.text)
        
        # 尋找 XML 中的新聞項目
        for item in root.findall('.//item')[:8]: # 預設只抓最新 8 則，精簡好讀
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            description = item.find('description').text if item.find('description') is not None else "點擊鏈結查看全文"
            
            # 清理一下發布時間的格式（移除多餘的時區字串）
            if pub_date:
                pub_date = pub_date.replace(" +0800", "")
            
            news_items.append({
                "title": title,
                "link": link,
                "date": pub_date,
                "summary": description
            })
    except Exception as e:
        st.error(f"新聞連線失敗：{e}")
    return news_items

# 3. 建立新聞分類選單
category_dict = {
    "🔥 重大焦點新聞": "https://feeds.feedburner.com/cnaFirstNews",
    "🇹🇼 台灣政治要聞": "https://feeds.feedburner.com/cnaPolitics",
    "💻 科技產業動態": "https://feeds.feedburner.com/cnaTech",
    "🌍 全球國際大事": "https://feeds.feedburner.com/cnaIntl",
    "📈 財經金融頭條": "https://feeds.feedburner.com/cnaFinance"
}

selected_category = st.selectbox("🎯 請選擇您想關心的焦點領域：", list(category_dict.keys()))
rss_url = category_dict[selected_category]

# 4. 當點擊重新整理或切換分類時
if st.button("🔄 立即同步最新頭條", use_container_width=True) or selected_category:
    with st.spinner("正在連線中央社資料庫，擷取最新大數據新聞..."):
        news_list = fetch_latest_news(rss_url)
        
        if news_list:
            st.success(f"🎉 成功為您撈出 {len(news_list)} 則實時焦點新聞！")
            st.write("")
            
            # 逐則渲染新聞卡片
            for idx, news in enumerate(news_list):
                with st.container(border=True):
                    # 新聞標題
                    st.markdown(f"### **[{idx+1}] {news['title']}**")
                    
                    # 時間標籤
                    st.caption(f"🕒 發布時間：{news['date']}")
                    
                    # AI 簡要導讀大綱（利用預覽內文呈現）
                    clean_summary = news['summary'][:150] + "..." if len(news['summary']) > 150 else news['summary']
                    st.write(f"📝 **新聞大綱摘要：** {clean_summary}")
                    
                    # 傳送門按鈕
                    st.markdown(f"[🔗 點我閱讀官方完整報導]({news['link']})")
        else:
            st.warning("目前該分類暫無新消息，請稍後再試！")

st.write("\n---")
st.caption("⚡ Powered by Streamlit & Python RSS Crawler")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 媒體串接專案，非經授權請勿複製。")
