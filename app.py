import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import urllib.parse

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 智慧每日全球新聞網", page_icon="📰", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 v4.0 | 核心技術：Google News 雲端全球即時新聞流")

st.title("📰 AI 智慧每日新聞助理 Google 新聞超級版")
st.write("本系統已全面對接 Google 新聞核心，24小時自動聚合全台各大主流媒體頭條，絕不漏接、永不堵塞！")

# 獲取今天日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 **今天是：{today}** | 正在為總工程師準備即時簡報...")
st.write("---")

# 2. 核心技術：Google News 專用容錯爬蟲
@st.cache_data(ttl=300) # 快取 5 分鐘
def fetch_google_news(rss_url):
    news_items = []
    try:
        # 模擬完全真實的瀏覽器標頭
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, "xml") # 用 xml 模式解析 Google 的標準 feed
        items = soup.find_all('item')
            
        for item in items[:8]: # 挑選最新 8 則
            title = item.find('title').text if item.find('title') else "最新消息"
            link = item.find('link').text if item.find('link') else "#"
            pub_date = item.find('pubDate').text if item.find('pubDate') else today
            
            # Google 新聞內文通常會包含媒體來源，幫它做漂亮清理
            clean_title = title
            source_site = "即時新聞"
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                clean_title = parts[0]
                source_site = parts[1]
            
            # 擷取並清洗描述
            desc_text = item.find('description').text if item.find('description') else "點擊鏈結查看全文"
            desc_soup = BeautifulSoup(desc_text, "html.parser")
            summary = desc_soup.get_text().strip()
            
            # 如果摘要太長或包含過多連結，截短處理
            if len(summary) > 150:
                summary = summary[:150] + "..."
                
            # 日期微調好讀
            if pub_date:
                pub_date = pub_date.replace(" GMT", "").replace("+0000", "")
            
            news_items.append({
                "title": clean_title,
                "link": link,
                "date": pub_date,
                "source": source_site,
                "summary": summary
            })
            
    except Exception as e:
        st.error(f"⚠️ 雲端安全防護通訊異常，原因：{e}")
    return news_items

# 3. 對接 Google News 台灣繁體中文分類接口
category_dict = {
    "🔥 今日重大焦點頭條": "https://news.google.com/rss/headlines/section/geo/TW?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "💻 科技產業與 AI 趨勢": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "📈 財經金融與商業產經": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "🌍 全球國際政治大事": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "🎨 娛樂八卦與藝文生活": "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
}

selected_category = st.selectbox("🎯 請選擇您想關心的焦點領域：", list(category_dict.keys()))
rss_url = category_dict[selected_category]

# 4. 渲染大數據畫面
if st.button("🔄 立即同步最新頭條", use_container_width=True) or selected_category:
    with st.spinner("正在連線 Google 新聞全球雲端中心，擷取實時數據簡報..."):
        news_list = fetch_google_news(rss_url)
        
        if news_list:
            st.success(f"🎉 連線成功！已為賴總工程師實時匯整 {len(news_list)} 則全台主流媒體報導：")
            st.write("")
            
            for idx, news in enumerate(news_list):
                with st.container(border=True):
                    # 標題與媒體來源標籤
                    st.markdown(f"### **[{idx+1}] {news['title']}**")
                    st.write(f"🏢 **新聞來源：** `{news['source']}` | 🕒 **發布時間：** {news['date']}")
                    
                    # 內文大綱
                    st.write(f"📝 **新聞大綱摘要：** {news['summary']}")
                    
                    # 傳送門
                    st.markdown(f"[🔗 點我閱讀官方完整報導]({news['link']})")
        else:
            st.error("⚠️ 資料串接暫時受阻，請點擊下方重新整理或切換分類！")

st.write("\n---")
st.caption("⚡ Powered by Streamlit & Google News Cloud API")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 媒體串接專案，非經授權請勿複製。")
