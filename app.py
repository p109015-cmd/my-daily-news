import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 智慧每日新聞 終極穩定版", page_icon="📰", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 v3.0 | 核心技術：BeautifulSoup 萬能容錯解析架構")

st.title("📰 AI 智慧每日新聞助理 終極穩定版")
st.write("本系統已全面升級為工業級網頁清洗引擎，100% 免疫任何格式錯誤，穩定提供即時新聞！")

# 獲取今天日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 **今天是：{today}** | 正在為總工程師準備即時簡報...")
st.write("---")

# 2. 核心技術：使用 BeautifulSoup 進行萬能容錯解析
@st.cache_data(ttl=300) # 快取 5 分鐘
def fetch_latest_news_v3(rss_url):
    news_items = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 使用 html.parser 進行寬鬆解析，自動忽略任何標籤不對稱的錯誤
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 抓取所有的新聞項目標籤
        items = soup.find_all('item')
            
        for item in items[:8]: # 精選最新 8 則
            # 寬鬆擷取各個欄位，找不到就給預設值
            title = item.find('title').text if item.find('title') else "最新消息"
            link = item.find('link').text if item.find('link') else "#"
            pub_date = item.find('pubdate').text if item.find('pubdate') else today
            
            # 清理摘要內文
            desc_tag = item.find('description')
            description = desc_tag.text if desc_tag else "點擊鏈結查看全文"
            
            # 進一步將內文中的所有殘留 HTML 標籤徹底清空
            if description:
                description = BeautifulSoup(description, "html.parser").get_text().strip()
            
            # 格式化日期清理
            if pub_date:
                pub_date = pub_date.replace(" +0800", "").replace(" GMT", "")
            
            news_items.append({
                "title": title,
                "link": link,
                "date": pub_date,
                "summary": description
            })
            
    except Exception as e:
        st.error(f"⚠️ 擷取失敗，錯誤原因：{e}")
    return news_items

# 3. 新聞來源選單
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
    with st.spinner("正在啟動高級清洗引擎，擷取實時新聞流..."):
        news_list = fetch_latest_news_v3(rss_url)
        
        if news_list:
            st.success(f"🎉 成功過濾並撈出 {len(news_list)} 則實時焦點新聞！")
            st.write("")
            
            for idx, news in enumerate(news_list):
                with st.container(border=True):
                    st.markdown(f"### **[{idx+1}] {news['title']}**")
                    st.caption(f"🕒 發布時間：{news['date']}")
                    
                    # 摘要長度限制
                    clean_summary = news['summary'] if news['summary'] else "無內文摘要"
                    if len(clean_summary) > 150:
                        clean_summary = clean_summary[:150] + "..."
                    st.write(f"📝 **新聞大綱摘要：** {clean_summary}")
                    
                    st.markdown(f"[🔗 點我閱讀官方完整報導]({news['link']})")
        else:
            st.error("目前該線路資料獲取失敗，請嘗試切換其他分類管道！")

st.write("\n---")
st.caption("⚡ Powered by Streamlit & BeautifulSoup4 Parser")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 媒體串接專案，非經授權請勿複製。")
