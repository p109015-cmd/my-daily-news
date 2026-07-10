# 2. 核心技術：Google News 專用容錯爬蟲（免安裝額外解析器版）
@st.cache_data(ttl=300) # 快取 5 分鐘
def fetch_google_news(rss_url):
    news_items = []
    try:
        # 模擬完全真實的瀏覽器標頭
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 🟢 關鍵修正：改用內建的 html.parser 繞過 xml 解析器缺失的問題
        soup = BeautifulSoup(response.text, "html.parser") 
        items = soup.find_all('item')
            
        for item in items[:8]: # 挑選最新 8 則
            title = item.find('title').text if item.find('title') else "最新消息"
            link = item.find('link').text if item.find('link') else "#"
            pub_date = item.find('pubdate').text if item.find('pubdate') else today
            
            # Google 新聞內文通常會包含媒體來源，幫它做漂亮清理
            clean_title = title
            source_site = "即時新聞"
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                clean_title = parts[0]
                source_site = parts[1]
            
            # 擷取並清洗描述
            desc_tag = item.find('description')
            desc_text = desc_tag.text if desc_tag else "點擊鏈結查看全文"
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
