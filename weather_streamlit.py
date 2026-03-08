import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Weather & News Service",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .weather-card {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .news-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-bottom: 1px solid #e0e0e0;
        text-align: left;
    }
    .news-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: left;
    }
    .news-source {
        color: #757575;
        font-size: 0.9rem;
        text-align: left;
    }
    .news-description {
        text-align: left;
    }
    .metric-card {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #757575;
    }
    .debug-info {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.8rem;
        max-height: 200px;
        overflow: auto;
        text-align: left;
    }
    /* Left alignment for all content */
    .stMarkdown, .stText, .stJson {
        text-align: left;
    }
    /* Ensure news containers are left-aligned */
    .news-container {
        text-align: left;
        width: 100%;
    }
    /* Left align column content */
    .stColumn {
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
# API_BASE_URL = "http://127.0.0.1:8000"
API_BASE_URL = "https://weather-newsapi.onrender.com"

# Initialize session state for debugging
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

# Header
st.markdown('<h1 class="main-header">🌤️ Weather & News Service</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Get real-time weather updates and latest news headlines</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/weather--v1.png", width=100)
    st.title("Navigation")
    option = st.radio(
        "Choose a service:",
        ["🏠 Home", "🌦️ Weather", "📰 News", "🗞️ Regional News", "📑 Paginated News", "📋 Daily Briefing", "🔧 Debug"]
    )

    st.markdown("---")
    st.markdown("### Settings")
    st.session_state.debug_mode = st.checkbox("Debug Mode", value=st.session_state.debug_mode)

    st.markdown("### About")
    st.info(
        "This app provides weather information and news headlines "
        "using FastAPI backend services."
    )

    # Server status
    st.markdown("---")
    st.markdown("### Server Status")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend Server: Online")
        else:
            st.error("❌ Backend Server: Error")
    except:
        st.error("❌ Backend Server: Offline")


# Helper function to safely parse response
def safe_json_response(response):
    """Safely parse JSON response handling different formats"""
    try:
        if response.headers.get('content-type') == 'application/json':
            return response.json()
        else:
            return {"raw_text": response.text}
    except:
        return {"error": "Failed to parse response", "raw_text": response.text}


# Helper function to display news articles safely (left-aligned)
def display_news_articles(articles):
    """Safely display news articles regardless of format - left aligned"""
    if isinstance(articles, dict):
        # Check if it's a wrapped response
        if 'articles' in articles:
            articles = articles['articles']
        elif 'data' in articles:
            articles = articles['data']
        else:
            # Display the dictionary as is
            st.json(articles)
            return

    if isinstance(articles, list):
        for i, article in enumerate(articles, 1):
            if isinstance(article, dict):
                title = article.get('title', article.get('headline', 'No Title'))
                source = article.get('source', {})
                if isinstance(source, dict):
                    source_name = source.get('name', source.get('title', 'Unknown'))
                else:
                    source_name = str(source)

                description = article.get('description',
                                          article.get('desc', article.get('content', 'No description available.')))

                # Left-aligned news card
                st.markdown(f"""
                <div class="news-card" style="text-align: left;">
                    <div class="news-title" style="text-align: left;">{i}. {title}</div>
                    <div class="news-source" style="text-align: left;">Source: {source_name}</div>
                    <div class="news-description" style="text-align: left;">{description}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left;'>{i}. {article}</div>", unsafe_allow_html=True)
    elif isinstance(articles, str):
        st.markdown(f"<div style='text-align: left;'>{articles}</div>", unsafe_allow_html=True)
    else:
        st.json(articles)


# Home Page
if option == "🏠 Home":
    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Weather Service", "🌦️", "Real-time data")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("News Service", "📰", "Top headlines")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Daily Briefing", "📋", "Combined info")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Quick Start Guide")

    guide_col1, guide_col2 = st.columns(2)

    with guide_col1:
        st.markdown("""
        **🌦️ Get Weather Information**
        1. Navigate to Weather section
        2. Enter city name (e.g., Delhi)
        3. Click 'Get Weather'

        **📰 Get News Headlines**
        1. Navigate to News section
        2. Enter country and limit
        3. View top headlines
        """)

    with guide_col2:
        st.markdown("""
        **🗞️ Regional News**
        1. Navigate to Regional News
        2. Select language
        3. Get localized news

        **📋 Daily Briefing**
        1. Navigate to Daily Briefing
        2. Enter your city
        3. Get weather + news combo
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# Weather Page
elif option == "🌦️ Weather":
    st.header("🌦️ Weather Information")

    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        city = st.text_input("Enter city name:", value="Delhi", placeholder="e.g., Mumbai, London, New York")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Get Weather", type="primary", use_container_width=True):
            with st.spinner("Fetching weather data..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/weather/{city}")

                    if st.session_state.debug_mode:
                        st.subheader("Debug Info")
                        st.code(f"Status Code: {response.status_code}")
                        st.json(response.json() if response.headers.get(
                            'content-type') == 'application/json' else response.text)

                    if response.status_code == 200:
                        weather_data = response.json()

                        # Display weather information
                        col_a, col_b, col_c = st.columns(3)

                        with col_a:
                            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                            st.metric("City", weather_data.get("city", "N/A"))
                            st.markdown('</div>', unsafe_allow_html=True)

                        with col_b:
                            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                            st.metric("Temperature", f"{weather_data.get('temperature', 'N/A')}°C")
                            st.markdown('</div>', unsafe_allow_html=True)

                        with col_c:
                            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                            st.metric("Condition", weather_data.get("condition", "N/A"))
                            st.markdown('</div>', unsafe_allow_html=True)

                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

# News Page
elif option == "📰 News":
    st.header("📰 Top News Headlines")

    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        country = st.text_input("Country:", value="india", placeholder="e.g., india, usa, uk")

    with col2:
        limit = st.number_input("Number of articles:", min_value=1, max_value=20, value=5)

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📰 Get News", type="primary", use_container_width=True):
            with st.spinner("Fetching news..."):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/news",
                        params={"country": country, "limit": limit}
                    )

                    if st.session_state.debug_mode:
                        st.subheader("Debug Info")
                        st.code(f"Status Code: {response.status_code}")
                        st.json(response.json() if response.headers.get(
                            'content-type') == 'application/json' else response.text)

                    if response.status_code == 200:
                        news_data = response.json()
                        display_news_articles(news_data)
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

# Regional News Page
elif option == "🗞️ Regional News":
    st.header("🗞️ Regional News")

    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        country = st.text_input("Country:", value="india", key="regional_country")

    with col2:
        language = st.selectbox(
            "Language:",
            ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi", "Gujarati"]
        )

    with col3:
        limit = st.number_input("Limit:", min_value=1, max_value=20, value=5, key="regional_limit")

    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Get Regional News", type="primary", use_container_width=True):
            with st.spinner(f"Fetching {language} news..."):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/news/language",
                        params={"country": country, "language": language, "limit": limit}
                    )

                    if st.session_state.debug_mode:
                        st.subheader("Debug Info")
                        st.code(f"Status Code: {response.status_code}")
                        st.json(response.json() if response.headers.get(
                            'content-type') == 'application/json' else response.text)

                    if response.status_code == 200:
                        news_data = response.json()
                        display_news_articles(news_data)
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

# Paginated News Page
elif option == "📑 Paginated News":
    st.header("📑 Paginated News Articles")

    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        country = st.text_input("Country:", value="india", key="page_country")

    with col2:
        language = st.selectbox(
            "Language:",
            ["English", "Hindi"],
            key="page_language"
        )

    with col3:
        if 'page' not in st.session_state:
            st.session_state.page = 1

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📖 Load Articles", type="primary", use_container_width=True):
            with st.spinner("Loading articles..."):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/news/paginated_articles",
                        params={"country": country, "language": language}
                    )

                    if st.session_state.debug_mode:
                        st.subheader("Debug Info")
                        st.code(f"Status Code: {response.status_code}")
                        st.json(response.json() if response.headers.get(
                            'content-type') == 'application/json' else response.text)

                    if response.status_code == 200:
                        articles = response.json()
                        st.session_state.articles = articles
                        st.session_state.total_articles = len(articles) if isinstance(articles, list) else 1
                        st.session_state.page = 1
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {str(e)}")

    # Display paginated articles
    if 'articles' in st.session_state and st.session_state.articles:
        articles = st.session_state.articles

        if isinstance(articles, list):
            articles_per_page = 5
            total_pages = (len(articles) + articles_per_page - 1) // articles_per_page

            # Pagination controls
            col_prev, col_page, col_next = st.columns([1, 3, 1])

            with col_prev:
                if st.button("◀ Previous") and st.session_state.page > 1:
                    st.session_state.page -= 1
                    st.rerun()

            with col_page:
                st.markdown(f"<center>Page {st.session_state.page} of {total_pages}</center>", unsafe_allow_html=True)

            with col_next:
                if st.button("Next ▶") and st.session_state.page < total_pages:
                    st.session_state.page += 1
                    st.rerun()

            # Display current page articles (left-aligned)
            start_idx = (st.session_state.page - 1) * articles_per_page
            end_idx = min(start_idx + articles_per_page, len(articles))

            for i in range(start_idx, end_idx):
                article = articles[i]
                if isinstance(article, dict):
                    st.markdown(f"""
                    <div class="news-card" style="text-align: left;">
                        <div class="news-title" style="text-align: left;">{i + 1}. {article.get('title', 'No Title')}</div>
                        <div class="news-source" style="text-align: left;">Source: {article.get('source', {}).get('name', 'Unknown') if isinstance(article.get('source'), dict) else article.get('source', 'Unknown')}</div>
                        <div class="news-description" style="text-align: left;">{article.get('description', 'No description available.')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: left;'>{i + 1}. {article}</div>", unsafe_allow_html=True)
        else:
            display_news_articles(articles)

    st.markdown("</div>", unsafe_allow_html=True)

# Daily Briefing Page
elif option == "📋 Daily Briefing":
    st.header("📋 Daily Briefing")
    st.markdown("Get weather and news together in one place!")

    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    city = st.text_input("Enter your city:", value="Delhi", key="briefing_city")

    if st.button("🚀 Get Daily Briefing", type="primary", use_container_width=True):
        with st.spinner("Preparing your daily briefing..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/briefing/city",
                    params={"city": city}
                )

                if st.session_state.debug_mode:
                    st.subheader("Debug Info")
                    st.code(f"Status Code: {response.status_code}")
                    st.json(response.json() if response.headers.get(
                        'content-type') == 'application/json' else response.text)

                if response.status_code == 200:
                    briefing_data = response.json()

                    # Weather Section
                    st.subheader("🌦️ Weather Update")
                    weather = briefing_data.get('weather', {})
                    if isinstance(weather, dict):
                        wcol1, wcol2, wcol3 = st.columns(3)

                        with wcol1:
                            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                            st.metric("City", weather.get('city', 'N/A'))
                            st.markdown('</div>', unsafe_allow_html=True)

                        with wcol2:
                            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                            st.metric("Temperature", f"{weather.get('temperature', 'N/A')}°C")
                            st.markdown('</div>', unsafe_allow_html=True)

                        with wcol3:
                            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                            st.metric("Condition", weather.get('condition', 'N/A'))
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: left;'>{weather}</div>", unsafe_allow_html=True)

                    # News Section
                    st.subheader("📰 Today's Top Headlines")
                    news = briefing_data.get('news', [])
                    display_news_articles(news)

                    # Briefing timestamp
                    st.info(f"Briefing generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

# Debug Page
elif option == "🔧 Debug":
    st.header("🔧 Debug Mode")
    st.markdown("Test individual API endpoints and see raw responses")

    # Left-aligned content
    st.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)

    endpoints = {
        "Root": "/",
        "Weather": "/weather/Delhi",
        "News": "/news?country=india&limit=3",
        "Regional News": "/news/language?country=india&language=Hindi&limit=3",
        "Paginated News": "/news/paginated_articles?country=india&language=English",
        "Daily Briefing": "/briefing/city?city=Delhi"
    }

    selected_endpoint = st.selectbox("Select endpoint to test:", list(endpoints.keys()))

    if st.button("Test Endpoint"):
        with st.spinner(f"Testing {selected_endpoint}..."):
            try:
                url = f"{API_BASE_URL}{endpoints[selected_endpoint]}"
                response = requests.get(url)

                st.subheader("Response Details")
                st.code(f"URL: {url}")
                st.code(f"Status Code: {response.status_code}")
                st.code(f"Headers: {dict(response.headers)}")

                st.subheader("Response Content")
                try:
                    json_response = response.json()
                    st.json(json_response)
                except:
                    st.code(response.text)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<p class="footer">Made with ❤️ using Streamlit & FastAPI</p>',
    unsafe_allow_html=True
)