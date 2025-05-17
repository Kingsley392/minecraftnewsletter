import streamlit as st
from datetime import datetime
import pytz
from firebase_utils import initialize_firebase
auth, database = initialize_firebase()

def show(database):
    """Display the weekly SMP newsletter in a classic newspaper layout."""

    # ----------  Style ---------- #
    st.markdown(
        """
        <style>
        .news-container {
            max-width: 900px;
            margin: auto;
            font-family: 'Times New Roman', serif;
        }
        .news-header {
            text-align: center;
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 0;
        }
        .news-subheader {
            text-align: center;
            font-size: 22px;
            margin-top: 0;
            margin-bottom: 40px;
            font-style: italic;
        }
        .section-title {
            font-size: 28px;
            font-weight: 700;
            border-bottom: 2px solid #000;
            margin-top: 30px;
        }
        .article {
            text-align: justify;
            font-size: 18px;
            line-height: 1.65;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📰 SMP Times")

    # ----------  Retrieve editions ---------- #
    try:
        newsletters_ref = (
            database.collection("newsletters")
            .order_by("week_start", direction="DESCENDING")
            .limit(10)
        )
        docs = newsletters_ref.get()
    except Exception as e:
        st.error(f"Could not load newsletters: {e}")
        return

    if not docs:
        st.info("No newsletters have been generated yet. Check back later!")
        return

    tz = pytz.timezone("America/Los_Angeles")
    editions: list[tuple[str, dict]] = []
    for d in docs:
        data = d.to_dict()
        start = data.get("week_start")
        if isinstance(start, datetime):
            label = start.astimezone(tz).strftime("%B %d, %Y")
        else:
            label = str(start)
        editions.append((label, data))

    labels = [lbl for lbl, _ in editions]
    selected_label = st.sidebar.selectbox("Edition", labels, index=0)
    selected_newsletter = next(data for lbl, data in editions if lbl == selected_label)

    # ----------  Build newsletter ---------- #
    headline = selected_newsletter.get("headline", "SMP Weekly Recap")
    subheadline = selected_newsletter.get("subheadline", f"Week of {selected_label}")
    sections = selected_newsletter.get("sections", [])
    if isinstance(sections, str):
        sections = [{"title": "Full Story", "body": sections}]

    st.markdown(
        f"""
        <div class="news-container">
            <div class="news-header">{headline}</div>
            <div class="news-subheader">{subheadline}</div>
        """,
        unsafe_allow_html=True,
    )

    for section in sections:
        title = section.get("title", "")
        body = section.get("body", "")
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="article">{body}</div>', unsafe_allow_html=True)

show(database)
