import json
import streamlit as st
from utils.answer_generator import generate_answer

from utils.retriever import retrieve

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Conversation Intelligence System",
    layout="wide"
)

# -------------------------------
# Load Personas
# -------------------------------

try:
    with open("persona/personas.json", "r", encoding="utf-8") as f:
        personas = json.load(f)
except:
    personas = []

# -------------------------------
# Title
# -------------------------------

st.title("Conversation Intelligence System")
st.write("Retrieve conversation insights using topic summaries, message chunks, and user persona.")

st.divider()

st.info(
    "Dataset: 11,001 Conversations | "
    "Semantic Search: FAISS + Sentence Transformers | "
    "Offline Processing"
)

# -------------------------------
# Query Input
# -------------------------------

query = st.text_input(
    "Enter your question"
)

search = st.button("Search")

# -------------------------------
# Search
# -------------------------------

if search:

    if query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    results = retrieve(query)

    # ---------------------------------------
    # FINAL ANSWER
    # ---------------------------------------

    st.header("Final Answer")
    if results["topics"]:
        
        persona = None
        if results["topics"]:
            conversation_id = results["topics"][0]["conversation_id"]
            for p in personas:

                if p["conversation_id"] == conversation_id:
                    persona = p
                    break
        answer = generate_answer(
            query,
            results,
            persona
        )
        st.write(answer)
    else:
        st.write("No relevant information found.")
    st.divider()

    # ---------------------------------------
    # PERSONA
    # ---------------------------------------

    if results["topics"]:

        conversation_id = results["topics"][0]["conversation_id"]

        persona = None

        for p in personas:

            if p["conversation_id"] == conversation_id:
                persona = p
                break

        if persona:

            st.header("User Persona")

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Habits")

                if persona["habits"]:
                    for h in persona["habits"]:
                        st.write(f"- {h}")
                else:
                    st.write("Not available")

                st.subheader("Personal Facts")

                if persona["personal_facts"]:
                    for fact in persona["personal_facts"]:
                        st.write(f"- {fact}")
                else:
                    st.write("Not available")

            with col2:

                st.subheader("Communication Style")

                style = persona["communication_style"]

                st.write(f"Message Length : {style['message_length']}")
                st.write(f"Tone : {style['tone']}")

                st.subheader("Personality Traits")

                if persona["personality_traits"]:
                    for trait in persona["personality_traits"]:
                        st.write(f"- {trait}")
                else:
                    st.write("Not available")

            st.divider()

    # ---------------------------------------
    # TOPIC SUMMARIES
    # ---------------------------------------

    st.header("Retrieved Topic Summaries")

    if results["topics"]:

        for i, topic in enumerate(results["topics"][:3], start=1):

            with st.expander(f"Topic Summary {i}"):

                st.subheader("Summary")

                st.write(topic["summary"])

                st.subheader("Keywords")

                for keyword in topic["keywords"]:
                    st.write(f"• {keyword}")

    else:

        st.write("No topics retrieved.")

    st.divider()

    # ---------------------------------------
    # MESSAGE CHUNKS
    # ---------------------------------------

    st.header("Retrieved Conversation Chunks")

    if results["chunks"]:

        for i, chunk in enumerate(results["chunks"][:3], start=1):

            with st.expander(f"Conversation Chunk {i}"):

                st.write(chunk["text"])

    else:

        st.write("No conversation chunks retrieved.")