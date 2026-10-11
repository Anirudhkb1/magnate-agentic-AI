import streamlit as st
import requests
import random
import time
import re

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="WikiBot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    .block-container {
        max-width: 760px !important;
        padding: 1rem 1.5rem 0 1.5rem !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ── Hide default title decorations ──────────────── */
    h1 { display: none; }

    /* ── Hero header ────────────────────────────────── */
    .hero {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .hero-icon {
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    .hero-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 0.15rem;
        font-weight: 400;
    }

    /* ── Chat container ─────────────────────────────── */
    div[data-testid="stChatMessage"] {
        border-radius: 14px !important;
        padding: 0.85rem 1.1rem !important;
        margin-bottom: 0.6rem !important;
        border: none !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
    }

    /* assistant bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background: #f0f4ff !important;
        border-left: 3px solid #4f6df5 !important;
    }

    /* user bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background: #f8f9fa !important;
        border-left: 3px solid #e0e0e0 !important;
    }

    /* avatars */
    div[data-testid="chatAvatarIcon-assistant"],
    div[data-testid="chatAvatarIcon-user"] {
        border-radius: 10px !important;
        width: 32px !important;
        height: 32px !important;
    }
    div[data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #4f6df5, #6c63ff) !important;
    }
    div[data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #374151, #4b5563) !important;
    }

    /* ── Chat input ─────────────────────────────────── */
    div[data-testid="stChatInput"] {
        border-radius: 14px !important;
        border: 1.5px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        padding: 0.15rem !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #4f6df5 !important;
        box-shadow: 0 0 0 3px rgba(79,109,245,0.12) !important;
    }
    div[data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }

    /* ── Markdown inside chat ───────────────────────── */
    div[data-testid="stChatMessage"] h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.4rem !important;
        color: #1e293b !important;
    }
    div[data-testid="stChatMessage"] a {
        color: #4f6df5 !important;
        text-decoration: none !important;
        font-weight: 500 !important;
    }
    div[data-testid="stChatMessage"] a:hover {
        text-decoration: underline !important;
    }
    div[data-testid="stChatMessage"] hr {
        margin: 0.6rem 0 !important;
        border-color: #e2e8f0 !important;
    }
    div[data-testid="stChatMessage"] ul {
        padding-left: 1.2rem !important;
    }

    /* ── Spinner ─────────────────────────────────────── */
    .stSpinner > div {
        border-color: #4f6df5 !important;
    }

    /* ── Sidebar ─────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: #fafbfc !important;
        border-right: 1px solid #e8ecf1 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
    }
    section[data-testid="stSidebar"] h2 {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #6b7280 !important;
        margin-bottom: 0.8rem !important;
    }

    /* ── Buttons ──────────────────────────────────────── */
    .stButton > button {
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.82rem !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.15s ease !important;
    }

    /* ── Suggestion pills ────────────────────────────── */
    .suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.6rem;
        justify-content: center;
    }
    .pill {
        display: inline-block;
        background: #eef1ff;
        color: #4f6df5;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 500;
        cursor: default;
    }

    /* ── Footer ───────────────────────────────────────── */
    .footer {
        text-align: center;
        padding: 0.8rem 0 0.4rem 0;
        font-size: 0.72rem;
        color: #9ca3af;
    }
    .footer a {
        color: #6b7280;
        text-decoration: none;
    }

    /* ── Stat cards in sidebar ────────────────────────── */
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e8ecf1;
    }
    .stat-label {
        font-size: 0.7rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        font-weight: 600;
    }
    .stat-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero Header ──────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">📚</div>
        <div class="hero-title">WikiBot</div>
        <div class="hero-sub">Real-time answers powered by Wikipedia</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session State ────────────────────────────────────────────
WELCOME_MSG = (
    "Hi there! I'm **WikiBot** — your personal Wikipedia assistant.\n\n"
    "Ask me about any person, place, concept, or event and I'll "
    "fetch a concise summary for you."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MSG}
    ]

if "num_sentences" not in st.session_state:
    st.session_state.num_sentences = 5

if "searches" not in st.session_state:
    st.session_state.searches = 0


# ── Helpers ──────────────────────────────────────────────────
def extract_query(user_message: str) -> str:
    """Strip common question prefixes to get the search topic."""
    msg = user_message.strip().rstrip("?").strip()
    prefixes = [
        r"^(can\s+you\s+tell\s+me\s+about)\s+",
        r"^(do\s+you\s+know\s+about)\s+",
        r"^(what\s+do\s+you\s+know\s+about)\s+",
        r"^(i\s+want\s+to\s+know\s+about)\s+",
        r"^(find\s+information\s+about)\s+",
        r"^(find\s+info\s+on)\s+",
        r"^(give\s+me\s+info\s+on)\s+",
        r"^(tell\s+me\s+about)\s+",
        r"^(search\s+for)\s+",
        r"^(look\s+up)\s+",
        r"^(what|who|where|when|why|how)\s+(is|are|was|were|do|does|did|can|could)\s+",
        r"^(what\s+about)\s+",
        r"^(explain)\s+",
        r"^(define)\s+",
        r"^(describe)\s+",
    ]
    for pattern in prefixes:
        msg = re.sub(pattern, "", msg, flags=re.IGNORECASE).strip()

    # Remove leading articles left over after prefix stripping
    msg = re.sub(r"^(the|a|an)\s+", "", msg, flags=re.IGNORECASE).strip()

    return msg


def is_conversational(msg: str) -> str | None:
    lower = msg.lower().strip()
    if re.search(r"\b(hello|hi|hey|greetings|howdy)\b", lower):
        return random.choice([
            "Hey! 👋 What would you like to learn about today?",
            "Hello! Give me a topic and I'll look it up for you.",
        ])
    if any(w in lower for w in ["bye", "goodbye", "see you"]):
        return "Goodbye! Happy exploring! 👋"
    if any(w in lower for w in ["thanks", "thank you", "thx"]):
        return "You're welcome! Anything else you'd like to know?"
    if any(w in lower for w in ["who are you", "your name", "what are you"]):
        return (
            "I'm **WikiBot** — a Wikipedia-powered assistant built with "
            "Streamlit. I search Wikipedia in real time, no API keys needed!"
        )
    return None


def _wiki_api(session: requests.Session, params: dict) -> dict | None:
    """Call the MediaWiki action API and return parsed JSON, or None."""
    url = "https://en.wikipedia.org/w/api.php"
    params.setdefault("format", "json")
    params.setdefault("formatversion", "2")
    try:
        resp = session.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except requests.exceptions.RequestException:
        pass
    return None


def search_wikipedia(query: str, num_sentences: int = 5) -> str:
    """Search Wikipedia using the MediaWiki API (search-first approach)."""
    if len(query) < 2:
        return "Please provide a topic to search. For example: *Tell me about the solar system*"

    session = requests.Session()
    session.headers.update({"User-Agent": "WikiBot/1.0 (Streamlit Chatbot)"})

    # ── Step 1: Search for matching articles ─────────────────
    search_data = _wiki_api(session, {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 5,
    })

    if not search_data:
        return f"I couldn't reach Wikipedia right now. Please check your internet connection and try again."

    search_results = search_data.get("query", {}).get("search", [])

    if not search_results:
        return (
            f"I couldn't find anything about **\"{query}\"** on Wikipedia.\n\n"
            f"Try rephrasing or using different keywords!"
        )

    # ── Step 2: Get the summary of the best match ────────────
    best_title = search_results[0]["title"]

    extract_data = _wiki_api(session, {
        "action": "query",
        "titles": best_title,
        "prop": "extracts|info",
        "exintro": True,
        "explaintext": True,
        "inprop": "url",
    })

    if extract_data:
        pages = extract_data.get("query", {}).get("pages", [])
        if pages:
            page = pages[0]
            title = page.get("title", best_title)
            extract = page.get("extract", "")
            page_url = page.get("fullurl", f"https://en.wikipedia.org/wiki/{best_title.replace(' ', '_')}")

            # Trim to requested number of sentences
            if extract:
                sentences = re.split(r'(?<=[.!?])\s+', extract.strip())
                trimmed = " ".join(sentences[:num_sentences])

                result = f"### {title}\n\n{trimmed}"
                result += f"\n\n---\n[Read full article on Wikipedia →]({page_url})"

                # Show other suggestions if available
                if len(search_results) > 1:
                    others = "\n".join(f"- {r['title']}" for r in search_results[1:4])
                    result += f"\n\n**Related topics:**\n{others}"

                return result

    # ── Fallback: list search results as links ───────────────
    results_list = "\n".join(
        f"- [{r['title']}](https://en.wikipedia.org/wiki/{r['title'].replace(' ', '_')})"
        for r in search_results
    )
    return (
        f"Here's what I found for **\"{query}\"**:\n\n"
        f"{results_list}\n\n"
        f"Try asking about one of these!"
    )


def get_bot_response(user_message: str) -> str:
    conv = is_conversational(user_message)
    if conv:
        return conv
    query = extract_query(user_message)
    st.session_state.searches += 1
    return search_wikipedia(query, st.session_state.num_sentences)


# ── Chat History ─────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show suggestions only when it's a fresh session (just the welcome message)
if len(st.session_state.messages) == 1:
    st.markdown(
        """
        <div class="suggestions">
            <span class="pill">Albert Einstein</span>
            <span class="pill">Quantum Computing</span>
            <span class="pill">The Great Wall of China</span>
            <span class="pill">Machine Learning</span>
            <span class="pill">NASA</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── User Input ───────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching Wikipedia…"):
            response = get_bot_response(prompt)

        placeholder = st.empty()
        streamed = ""
        delay = 0.008 if len(response) > 400 else 0.015
        for char in response:
            streamed += char
            placeholder.markdown(streamed + "▌")
            time.sleep(delay)
        placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ── Footer ───────────────────────────────────────────────────
st.markdown(
    '<div class="footer">WikiBot · Powered by '
    '<a href="https://en.wikipedia.org">Wikipedia</a> · '
    'Built with <a href="https://streamlit.io">Streamlit</a></div>',
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Settings")

    st.session_state.num_sentences = st.slider(
        "Response length",
        min_value=2,
        max_value=10,
        value=st.session_state.num_sentences,
        help="Number of sentences per Wikipedia summary.",
    )

    st.markdown("")

    if st.button("🗑  Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MSG}
        ]
        st.session_state.searches = 0
        st.rerun()

    st.markdown("---")
    st.markdown("## Stats")

    msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Messages</div>
            <div class="stat-value">{msg_count}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Wikipedia Searches</div>
            <div class="stat-value">{st.session_state.searches}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("## About")
    st.markdown(
        "**WikiBot** searches Wikipedia in real time to answer "
        "your questions — no API keys, no sign-up.\n\n"
        "Built with [Streamlit](https://streamlit.io) & "
        "[wikipedia](https://pypi.org/project/wikipedia/).",
    )
