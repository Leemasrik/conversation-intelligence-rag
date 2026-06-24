import json
import streamlit as st

from utils.retriever import retrieve
from utils.query_router import route_query


st.set_page_config(
    page_title="Conversation Intelligence System",
    layout="wide"
)


# -----------------------------
# Load Persona
# -----------------------------
try:
    with open("persona/personas.json", "r", encoding="utf-8") as f:
        personas = json.load(f)
except:
    personas = []


# -----------------------------
# Load Persona Drift
# -----------------------------
try:
    with open("drift/drift_timeline.json", "r", encoding="utf-8") as f:
        drift_timeline = json.load(f)
except:
    drift_timeline = []


# -----------------------------
# UI
# -----------------------------
st.title("Conversation Intelligence System")

st.write(
    "Retrieve conversation insights using topic summaries, "
    "message chunks and user persona."
)

st.divider()

st.info(
    "Dataset: 11,001 Conversations | "
    "Semantic Search: FAISS + Sentence Transformers | "
    "Offline Intent Classification | "
    "Persona Drift Detection"
)

query = st.text_input(
    "Enter your question"
)

search = st.button("Search")


# ==========================================================
# Search
# ==========================================================

if search:

    if query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    results = retrieve(query)

    persona = None

    if results["topics"]:

        conversation_id = results["topics"][0]["conversation_id"]

        for p in personas:

            if p["conversation_id"] == conversation_id:

                persona = p

                break

    # ======================================================
    # Final Answer
    # ======================================================

    st.header("Final Answer")

    if results["topics"]:

        answer = route_query(
            query,
            results,
            persona
        )

        st.write(answer)

    else:

        st.write("No relevant information found.")

    st.divider()

    # ======================================================
    # User Persona
    # ======================================================

    if persona:

        st.header("User Persona")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Habits")

            if persona["habits"]:

                for h in persona["habits"]:

                    st.write(f"• {h}")

            else:

                st.write("Not available")

            st.subheader("Personal Facts")

            if persona["personal_facts"]:

                for fact in persona["personal_facts"]:

                    st.write(f"• {fact}")

            else:

                st.write("Not available")

        with col2:

            st.subheader("Communication Style")

            style = persona["communication_style"]

            st.write(
                f"Message Length : {style['message_length']}"
            )

            st.write(
                f"Tone : {style['tone']}"
            )

            st.subheader("Personality Traits")

            if persona["personality_traits"]:

                for trait in persona["personality_traits"]:

                    st.write(f"• {trait}")

            else:

                st.write("Not available")

    st.divider()

    # ======================================================
    # Persona Drift
    # ======================================================

    st.header("📈 Persona Drift Detection")

    if results["topics"]:

        conversation_id = results["topics"][0]["conversation_id"]

        drift = next(

            (
                d
                for d in drift_timeline
                if d["conversation_id"] == conversation_id
            ),

            None

        )

        if drift:

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Current Mood:** {drift['current_mood']}"
                )

                st.write(
                    f"**Previous Mood:** {drift['previous_mood']}"
                )

                st.write(
                    f"**Mood Drift:** {drift['drift']}"
                )

            with col2:

                st.write(
                    f"**Communication Tone:** {drift['tone']}"
                )

                st.write(
                    f"**Trigger:** {drift['trigger']}"
                )

        else:

            st.write("No persona drift information available.")

    st.divider()

    # ======================================================
    # Topic Checkpoints
    # ======================================================

    st.header("Retrieved Topic Checkpoints")

    if results["topics"]:

        for i, topic in enumerate(
            results["topics"][:3],
            start=1
        ):

            with st.expander(
                f"Topic Checkpoint {i}"
            ):

                st.subheader("Summary")

                st.write(
                    topic["summary"]
                )

                st.subheader("Keywords")

                for keyword in topic["keywords"]:

                    st.write(f"• {keyword}")

    else:

        st.write("No topic checkpoints retrieved.")

    st.divider()

    # ======================================================
    # Message Chunks
    # ======================================================

    st.header("Retrieved Message Chunks")

    if results["chunks"]:

        for i, chunk in enumerate(
            results["chunks"][:3],
            start=1
        ):

            with st.expander(
                f"Message Chunk {i}"
            ):

                st.write(
                    chunk["text"]
                )

    else:

        st.write("No message chunks retrieved.")