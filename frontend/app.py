# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000"

# st.set_page_config(page_title="DealMind AI", layout="wide")

# # Title
# st.title("💼 DealMind AI")
# st.markdown("### Memory-Powered Sales Intelligence Agent")

# # Sidebar
# st.sidebar.header("📌 Client Info")
# client_name = st.sidebar.text_input("Client Name", "ABC Corp")

# # Layout split
# col1, col2 = st.columns([2, 1])

# # ---------------- LEFT: CHAT ---------------- #
# with col1:
#     st.subheader("💬 Client Interaction")

#     message = st.text_area("Enter client message")

#     if st.button("🚀 Get AI Suggestion"):

#         if message.strip() == "":
#             st.warning("Please enter a message")
#         else:
#             payload = {
#                 "client_name": client_name,
#                 "message": message
#             }

#             with st.spinner("Thinking..."):
#                 try:
#                     response = requests.post(f"{API_URL}/chat", json=payload)

#                     if response.status_code == 200:
#                         result = response.json()

#                         st.success("✅ AI Suggestion")
#                         st.write(result["response"])

#                     else:
#                         st.error("❌ Backend error")

#                 except:
#                     st.error("❌ Cannot connect to backend")

# # ---------------- RIGHT: MEMORY ---------------- #
# with col2:
#     st.subheader("🧠 Client Memory")

#     try:
#         mem_response = requests.get(f"{API_URL}/memory/{client_name}")

#         if mem_response.status_code == 200:
#             memory = mem_response.json()["memory"]

#             if memory:
#                 for m in reversed(memory[-5:]):
#                     st.markdown(f"""
# 🔹 **Message:** {m['message']}  
# 🔹 **Objection:** `{m['objection']}`  
# 🕒 {m['timestamp']}
# ---
# """)
#             else:
#                 st.info("No memory yet")

#         else:
#             st.error("Error loading memory")

#     except:
#         st.warning("Backend not running")

# # ---------------- FOOTER ---------------- #
# st.markdown("---")
# st.markdown("Built with ❤️ using FastAPI + Groq + Memory")



# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000"

# st.set_page_config(page_title="DealMind AI", layout="wide")

# st.title("🧠 DealMind AI")
# st.markdown("### Memory-Powered Sales Intelligence Agent")

# st.sidebar.header("📌 Client Info")
# client_name = st.sidebar.text_input("Client Name", "Acme Corporation")

# col1, col2 = st.columns([2, 1])

# with col1:
#     st.subheader("💬 Client Interaction")
#     message = st.text_area("Enter client message")

#     if st.button("⚡ Get AI Suggestion"):
#         if message.strip() == "":
#             st.warning("Please enter a message")
#         else:
#             payload = {
#                 "client_name": client_name,
#                 "message": message
#             }

#             with st.spinner("Thinking..."):
#                 try:
#                     response = requests.post(f"{API_URL}/chat", json=payload, timeout=30)

#                     if response.status_code == 200:
#                         result = response.json()

#                         st.success("AI Suggestion")
#                         st.write(result["response"])

#                         st.markdown(f"**Detected Objection:** {result['objection']}")
#                         st.markdown(f"**Suggested Strategy:** {result['strategy']}")
#                         st.markdown(f"**Deal Stage:** {result['deal_stage']}")
#                         st.markdown(f"**Deal Value:** {result['deal_value']}")
#                         st.markdown(f"**Product:** {result['product']}")
#                         st.markdown(f"**Sales Agent:** {result['sales_agent']}")
#                         st.markdown(f"**Next Best Action:** {result['next_action']}")
#                         st.markdown(f"**Risk Flags:** {', '.join(result['risk_flags']) if result['risk_flags'] else 'None'}")
#                     else:
#                         st.error(f"Backend Error: {response.status_code} - {response.text}")

#                 except Exception as e:
#                     st.error(f"Cannot connect to backend: {str(e)}")

# with col2:
#     st.subheader("🧠 Client Memory")
#     try:
#         mem_response = requests.get(f"{API_URL}/memory/{client_name}", timeout=10)

#         if mem_response.status_code == 200:
#             memory = mem_response.json().get("memory", [])

#             if memory:
#                 for m in reversed(memory):
#                     st.markdown(m["content"])
#                     st.markdown("---")
#             else:
#                 st.info("No memory yet")
#         else:
#             st.error("Error loading memory")
#     except Exception:
#         st.warning("Backend not running")

# st.markdown("---")
# st.markdown("Built with ❤️ using FastAPI + Groq + Hindsight")

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DealMind AI", layout="wide")

st.title("🧠 DealMind AI")
st.markdown("### Memory-Powered Sales Intelligence Agent")

st.sidebar.header("📌 Client Info")
client_name = st.sidebar.text_input("Client Name", "Acme Corporation")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Client Interaction")
    message = st.text_area("Enter client message")

    if st.button("⚡ Get AI Suggestion"):
        if message.strip() == "":
            st.warning("Please enter a message")
        else:
            payload = {
                "client_name": client_name,
                "message": message
            }

            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{API_URL}/chat", json=payload, timeout=30)

                    if response.status_code == 200:
                        result = response.json()

                        st.success("AI Suggestion")
                        st.write(result["response"])

                        st.markdown("### Deal Intelligence Output")
                        st.markdown(f"**Detected Objection:** {result.get('objection', 'Unknown')}")
                        st.markdown(f"**Suggested Strategy:** {result.get('strategy', 'Unknown')}")
                        st.markdown(f"**Deal Stage:** {result.get('deal_stage', 'Unknown')}")
                        st.markdown(f"**Deal Value:** {result.get('deal_value', 'Unknown')}")
                        st.markdown(f"**Product:** {result.get('product', 'Unknown')}")
                        st.markdown(f"**Sales Agent:** {result.get('sales_agent', 'Unknown')}")
                        st.markdown(f"**Next Best Action:** {result.get('next_action', 'Unknown')}")

                        risk_flags = result.get("risk_flags", [])
                        st.markdown(
                            f"**Risk Flags:** {', '.join(risk_flags) if risk_flags else 'None'}"
                        )

                    else:
                        st.error(f"Backend Error: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"Cannot connect to backend: {str(e)}")

with col2:
    st.subheader("📌 Client Brief")
    try:
        preview_response = requests.post(
            f"{API_URL}/chat",
            json={"client_name": client_name, "message": "summary"},
            timeout=20
        )

        if preview_response.status_code == 200:
            preview = preview_response.json()
            profile = preview.get("client_profile", {})

            st.markdown(f"**Account:** {profile.get('account', 'Unknown')}")
            st.markdown(f"**Sector:** {profile.get('sector', 'Unknown')}")
            st.markdown(f"**Office Location:** {profile.get('office_location', 'Unknown')}")
            st.markdown(f"**Revenue:** {profile.get('revenue', 'Unknown')}")
            st.markdown(f"**Employees:** {profile.get('employees', 'Unknown')}")
            st.markdown("---")
            st.markdown(f"**Stage:** {preview.get('deal_stage', 'Unknown')}")
            st.markdown(f"**Product:** {preview.get('product', 'Unknown')}")
            st.markdown(f"**Value:** {preview.get('deal_value', 'Unknown')}")
            st.markdown(f"**Owner:** {preview.get('sales_agent', 'Unknown')}")
        else:
            st.info("No client brief available")
    except Exception:
        st.warning("Client brief unavailable")

    st.subheader("🧠 Client Memory")
    try:
        mem_response = requests.get(f"{API_URL}/memory/{client_name}", timeout=10)

        if mem_response.status_code == 200:
            memory = mem_response.json().get("memory", [])

            if memory:
                for m in reversed(memory):
                    st.markdown(m["content"])
                    st.markdown("---")
            else:
                st.info("No memory yet")
        else:
            st.error("Error loading memory")
    except Exception:
        st.warning("Backend not running")

st.markdown("---")
st.markdown("Built with ❤️ using FastAPI + Groq + Hindsight")