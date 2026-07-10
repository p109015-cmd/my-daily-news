import streamlit as st
import requests
from xml.etree import ElementTree
import datetime

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 智慧每日新聞 Pro", page_icon="📰", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 v1.2 | 核心技術：高級編碼清洗與容錯 RSS 爬蟲")

st.title("📰 AI 智慧每日新聞助理 Pro")
st.write("本系統連線至國家級通訊社（中央社），即時抓取最新、最準確的焦點頭條，拒絕垃圾農場文！")

# 獲取今天日期
today = datetime.datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 **今天是：{today}** | 正在為總工程師準備即時簡報...")
st.write("---")

# 2. 核心技術：升級版安全 RSS 爬蟲函式（內含編碼清洗）
@st.cache_data(ttl=300) # 快取縮短為 5 分鐘，即時性更高
def fetch_latest_news(rss_url):
    news_items = []
    try:
        # 加入瀏覽器標頭（User-Agent），防止有些網站阻擋雲端伺服器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        
        # 強制使用 utf-8-sig 編碼，自動過濾掉可能導致 XML 解析失敗的 BOM 頭 (\ufeff)
        response.encoding = 'utf-8-sig'
        xml_text = response.text.strip()
        
        # 尋找 xml 宣告並做安全前置清理
        if xml_text.startswith("<?xml"):
            # 尋找第一個真正的標籤開始，確保沒有雜質字元
            start_idx = xml_text.find("<rss") if "<rss" in xml_text else xml_text.find("<root")
            if start_idx != -1:
                # 重新保留合法的 XML 部分
                xml_text = xml_text[xml_text.find("<?xml"):]
        
        # 進行 XML 解析
        root = ElementTree.fromstring(xml_text)
        
        # 尋找 XML 中的新聞項目
        items = root.findall('.//item')
        if not items:
            # 有些 RSS 結構使用 entry (Atom 格式)
            items = root.findall('.//entry')
            
        for item in items[:8]: # 預設只抓最新 8 則
            try:
                title_node = item.find('title')
                link_node = item.find('link')
                date_node = item.find('pubDate') or item.find('published') or item.find('updated')
                desc_node = item.find('description') or item.find('summary')
                
                title = title_node.text if title_node is not None else "無標題"
                
                # 處理連結可能在屬性中的情況
                if link_node is not None:
                    link = link_node.text if link_node.text else link_node.get('href', '#')
                else:
                    link = '#'
                    
                pub_date = date_node.text if date_node is not None else today
                description = desc_node.text if desc_node is not None else "點擊鏈結查看全文"
                
                # 清理時間格式
                if pub_date:
                    pub_date = pub_date.replace(" +0800", "")
                
                news_items.append({
                    "title": title,
                    "link": link,
                    "date": pub_date,
                    "summary": description
                })
            except Exception:
                continue # 單則新聞解析失敗時跳過，確保整頁不崩潰
                
    except Exception as e:
        st.error(f"新聞連線解析失敗，已啟動防護機制。錯誤原因：{e}")
    return news_items

# 3. 建立穩定版中央社新聞分類選單
category_dict = {
    "🔥 重大焦點新聞": "https://feeds.feedburner.com/cnaFirstNews",
    "🇹🇼 台灣政治要聞": "https://feeds.feedburner.com/cnaPolitics",
    "💻 科技產業動態": "https://feeds.feedburner.com/cnaTech",
    "🌍 全球國際大事": "https://feeds.feedburner.com/cnaIntl",
    "📈 財經金融頭條": "https://feeds.feedburner.com/cnaFinance"
}

selected_category = st.selectbox("🎯 請選擇您想關心的焦點領域：", list(category_dict.keys()))
rss_url = category_dict[selected_category]

# 4. 當切換分類或點擊同步時
if st.button("🔄 立即同步最新頭條", use_container_width=True) or selected_category:
    with st.spinner("正在連線國家級通訊社，進行數據清洗與簡報擷取..."):
        news_list = fetch_latest_news(rss_url)
        
        if news_list:
            st.success(f"🎉 安全連線成功！已為總工程師過濾並撈出 {len(news_list)} 則最新實時要聞：")
            st.write("")
            
            for idx, news in enumerate(news_list):
                with st.container(border=True):
                    st.markdown(f"### **[{idx+1}] {news['title']}**")
                    st.caption(f"🕒 發布時間：{news['date']}")
                    
                    # 摘要清洗與長度限制
                    clean_summary = news['summary'] if news['summary'] else "無內文摘要"
                    if len(clean_summary) > 150:
                        clean_summary = clean_summary[:150] + "..."
                    st.write(f"📝 **新聞摘要：** {clean_summary}")
                    
                    st.markdown(f"[🔗 點我閱讀官方完整報導]({news['link']})")
        else:
            st.warning("⚠️ 目前該分類獲取到的資料為空，正在等待新聞台刷新，請稍後重試！")

st.write("\n---")
st.caption("⚡ Powered by Streamlit & Clean Python RSS Crawler")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 媒體串接專案，非經授權請勿複製。")
