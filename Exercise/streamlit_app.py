import requests
import streamlit as st

###Run the API first:   ./fastapi-venv/bin/uvicorn model_app:app --reload
####Then run this UI:    ./fastapi-venv/bin/streamlit run streamlit_app.py


# Keep these in sync with model_app.py
TIER_1_CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
TIER_2_CITIES = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri", "Srinagar",
]
KNOWN_CITIES = sorted(TIER_1_CITIES + TIER_2_CITIES)
OCCUPATIONS = [
    "retired", "freelancer", "student", "government_job",
    "business_owner", "unemployed", "private_job",
]

st.set_page_config(page_title="Insurance Premium Predictor", page_icon="🩺")
st.title("🩺 Insurance Premium Category Predictor")
st.caption("A thin UI over the FastAPI `/predict` endpoint in `model_app.py`.")

with st.sidebar:
    st.header("API settings")
    api_url = st.text_input("Predict endpoint", value="http://localhost:8000/predict")
    st.markdown(
        "Start the API with:\n\n"
        "```\n./fastapi-venv/bin/uvicorn model_app:app --reload\n```"
    )

with st.form("user_input"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=119, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.1, value=70.0, step=0.5)
        height = st.number_input("Height (m)", min_value=0.1, value=1.75, step=0.01, format="%.2f")
    with col2:
        income_lpa = st.number_input("Income (LPA)", min_value=0.0, value=12.0, step=0.5)
        occupation = st.selectbox("Occupation", OCCUPATIONS)
        is_smoker = st.checkbox("Smoker?")

    city_choice = st.selectbox("City", KNOWN_CITIES + ["Other (type below)"])
    other_city = st.text_input("Other city", value="", disabled=city_choice != "Other (type below)")
    city = other_city.strip() if city_choice == "Other (type below)" else city_choice

    submitted = st.form_submit_button("Predict", type="primary")

if submitted:
    if not city:
        st.error("Please provide a city.")
        st.stop()

    payload = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "income_lpa": float(income_lpa),
        "is_smoker": bool(is_smoker),
        "city": city,
        "occupation": occupation,
    }

    st.write("**Request payload**")
    st.json(payload)

    try:
        resp = requests.post(api_url, json=payload, timeout=10)
    except requests.exceptions.ConnectionError:
        st.error(f"Could not reach the API at {api_url}. Is uvicorn running?")
        st.stop()
    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")
        st.stop()

    if resp.status_code == 200:
        category = resp.json().get("predicted_category")
        st.success(f"Predicted premium category: **{category}**")
    else:
        st.error(f"API returned HTTP {resp.status_code}")
        try:
            st.json(resp.json())
        except ValueError:
            st.text(resp.text)
