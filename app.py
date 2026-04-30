import streamlit as st
from transformers import pipeline
from datetime import date

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

# ---------- GENERATE AI CONTENT ----------
def generate_content(role, skills, company, tone):

    tone_prompt = {
        "Formal": "Write in a professional tone.",
        "Friendly": "Write in a friendly tone.",
        "Confident": "Write in a confident tone.",
        "Short": "Write briefly in 3-4 lines."
    }

    prompt = f"""
    Write a short professional paragraph for a cover letter.

    Job Role: {role}
    Company: {company}
    Skills: {skills}

    {tone_prompt[tone]}
    """

    result = generator(prompt, max_length=120, temperature=0.7)
    text = result[0]['generated_text']

    clean = text.replace(prompt, "").strip()
    return clean


# ---------- FORMAT LETTER ----------
def format_letter(name, role, company, content):

    today = date.today().strftime("%d %B %Y")

    letter = f"""
{today}

To  
Hiring Manager  
{company}

Subject: Application for {role} position

Dear Hiring Manager,

I am writing to express my interest in the {role} position at {company}.

{content}

I am eager to contribute my skills and grow within your organization. I would welcome the opportunity to discuss my application further.

Thank you for your time and consideration.

Sincerely,  
{name}
"""

    return letter


# ---------- UI ----------
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.block-container {
    max-width: 800px;
    padding-top: 2rem;
}

.card {
    background: #111827;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
    margin-top: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #38bdf8, #0ea5e9);
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

input, textarea {
    background-color: #1e293b !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1 style='text-align:center;'>✉️ AI Cover Letter Generator</h1>", unsafe_allow_html=True)

# ---------- INPUT ----------
name = st.text_input("👤 Your Name")
role = st.text_input("💼 Job Role")
company = st.text_input("🏢 Company Name")
skills = st.text_area("🧠 Your Skills")

tone = st.selectbox("🎯 Select Tone", ["Formal", "Friendly", "Confident", "Short"])

# ---------- BUTTON ----------
if st.button("Generate Cover Letter"):
    if name and role and company and skills:

        with st.spinner("Generating professional cover letter..."):
            content = generate_content(role, skills, company, tone)
            letter = format_letter(name, role, company, content)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📄 Professional Cover Letter")
        st.text(letter)

        st.download_button(
            "📥 Download Cover Letter",
            letter,
            file_name="cover_letter.txt"
        )

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please fill all fields")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center>Made with ❤️ | AI Cover Letter Generator</center>", unsafe_allow_html=True)