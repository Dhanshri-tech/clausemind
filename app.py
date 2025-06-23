
import streamlit as st
import requests
import uuid
import json
import time

API_BASE_URL = "http://localhost:8000"
APP_NAME = "manager"

# Configure page
st.set_page_config(page_title="ClauseMind - Contract Assistant", layout="wide", initial_sidebar_state="collapsed")

# Initialize session states
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "user_input_value" not in st.session_state:
    st.session_state.user_input_value = ""

if "home_tab" not in st.session_state:
    st.session_state.home_tab = "domains"

if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = None

# Function to create a session (unchanged)
def create_session():
    session_id = f"session-{int(time.time())}"
    try:
        response = requests.post(
            f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions/{session_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({})
        )
        if response.status_code == 200:
            st.session_state.session_id = session_id
            st.session_state.messages = []
            return True
        else:
            st.error(f"❌ Failed to create session: {response.text}")
            return False
    except Exception as e:
        st.error(f"❌ Exception: {e}")
        return False

# Function to send message (unchanged)
def send_message(message):
    if not st.session_state.session_id:
        st.error("❗ No active session. Please create one first.")
        return

    # Append user message
    st.session_state.messages.append({"role": "user", "content": message})

    try:
        response = requests.post(
            f"{API_BASE_URL}/run",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "app_name": APP_NAME,
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}],
                }
            }),
            timeout=30
        )

        if response.status_code != 200:
            st.error(f"❌ Error: {response.text}")
            return

        data = response.json()
        
        # Enhanced Debug Output
        st.write("🔍 **Full API Response Structure:**")
        st.json(data)
        
        # Analyze all events and their roles
        st.write("📋 **Event Analysis:**")
        for i, event in enumerate(data):
            content = event.get("content", {})
            role = content.get("role", "NO_ROLE")
            parts = content.get("parts", [])
            has_text = any("text" in part for part in parts) if parts else False
            
            st.write(f"Event {i}: Role=`{role}`, Has_Text={has_text}")
            if has_text:
                for j, part in enumerate(parts):
                    if "text" in part:
                        preview = part["text"][:100] + "..." if len(part["text"]) > 100 else part["text"]
                        st.write(f"  Part {j} text preview: {preview}")
        
        assistant_message = None

        # Enhanced parsing - try multiple patterns
        patterns_tried = []
        
        # Pattern 1: Original - look for "model" role
        for event in data:
            content = event.get("content", {})
            if content.get("role") == "model":
                parts = content.get("parts", [])
                if parts and "text" in parts[0]:
                    assistant_message = parts[0]["text"].strip()
                    patterns_tried.append("✅ Found via 'model' role")
                    break
        
        # Pattern 2: Look for "assistant" role (common for sub-agents)
        if not assistant_message:
            for event in data:
                content = event.get("content", {})
                if content.get("role") == "assistant":
                    parts = content.get("parts", [])
                    if parts and "text" in parts[0]:
                        assistant_message = parts[0]["text"].strip()
                        patterns_tried.append("✅ Found via 'assistant' role")
                        break
        
        # Pattern 3: Look for any role with text (fallback)
        if not assistant_message:
            for event in data:
                content = event.get("content", {})
                role = content.get("role")
                if role and role != "user":  # Skip user messages
                    parts = content.get("parts", [])
                    if parts and "text" in parts[0]:
                        assistant_message = parts[0]["text"].strip()
                        patterns_tried.append(f"✅ Found via '{role}' role (fallback)")
                        break
        
        # Pattern 4: Check for direct text field (some APIs return differently)
        if not assistant_message:
            for event in data:
                if "text" in event:
                    assistant_message = event["text"].strip()
                    patterns_tried.append("✅ Found via direct 'text' field")
                    break
        
        # Pattern 5: Check for nested response structure
        if not assistant_message:
            for event in data:
                if "response" in event and "text" in event["response"]:
                    assistant_message = event["response"]["text"].strip()
                    patterns_tried.append("✅ Found via nested 'response.text'")
                    break
        
        # Show what patterns were tried
        st.write("🔧 **Parsing Attempts:**")
        for pattern in patterns_tried:
            st.write(pattern)
        
        if not patterns_tried:
            st.write("❌ No patterns matched")

        if assistant_message:
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            # Don't show success message to avoid white blocks
        else:
            st.error("⚠️ Assistant response not found in any expected format.")
            
            # Show available structure for manual inspection
            st.write("🔍 **Available event structures:**")
            for i, event in enumerate(data):
                st.write(f"Event {i} keys: {list(event.keys())}")
                if "content" in event:
                    st.write(f"  Content keys: {list(event['content'].keys())}")

    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
    except Exception as e:
        st.error(f"❌ Exception: {e}")
        import traceback
        st.text(traceback.format_exc())

# Navigation functions
def go_to_chat():
    st.session_state.current_page = "chat"

def go_to_home():
    st.session_state.current_page = "home"

def go_to_domain(domain):
    st.session_state.current_page = "domain"
    st.session_state.selected_domain = domain

# Domain information data
DOMAIN_INFO = {
    "tech": {
        "title": "Technology Contracts",
        "icon": "💻",
        "description": "Specialized contract analysis for technology sector agreements, software licensing, and digital services.",
        "features": [
            "Software License Agreement Analysis",
            "SaaS Contract Review",
            "API Terms and Conditions",
            "Technology Transfer Agreements",
            "Data Processing Agreements",
            "Cloud Service Contracts"
        ],
        "use_cases": [
            "Analyze software licensing terms and restrictions",
            "Review API usage limits and pricing models",
            "Identify data privacy and security clauses",
            "Check intellectual property ownership terms",
            "Validate service level agreements (SLAs)"
        ]
    },
    "finance": {
        "title": "Financial Contracts",
        "icon": "💰",
        "description": "Comprehensive analysis of financial agreements, loan documents, and investment contracts.",
        "features": [
            "Loan Agreement Analysis",
            "Investment Contract Review",
            "Banking Terms Evaluation",
            "Insurance Policy Analysis",
            "Financial Service Agreements",
            "Credit Facility Documentation"
        ],
        "use_cases": [
            "Review interest rates and payment terms",
            "Identify collateral and security provisions",
            "Analyze default and termination clauses",
            "Check regulatory compliance requirements",
            "Validate financial covenants and ratios"
        ]
    },
    "health": {
        "title": "Healthcare Contracts",
        "icon": "🏥",
        "description": "Specialized contract analysis for healthcare providers, medical services, and pharmaceutical agreements.",
        "features": [
            "Medical Service Agreements",
            "Healthcare Provider Contracts",
            "Pharmaceutical Licensing",
            "Medical Device Agreements",
            "Patient Privacy Compliance",
            "Research and Clinical Trial Contracts"
        ],
        "use_cases": [
            "Ensure HIPAA compliance in service agreements",
            "Review medical liability and insurance terms",
            "Analyze pharmaceutical licensing restrictions",
            "Check clinical trial protocols and ethics",
            "Validate patient consent and privacy terms"
        ]
    },
    "procurement": {
        "title": "Procurement Contracts",
        "icon": "📦",
        "description": "Streamlined analysis of procurement agreements, supplier contracts, and vendor management documents.",
        "features": [
            "Supplier Agreement Analysis",
            "Purchase Order Terms",
            "Vendor Management Contracts",
            "Supply Chain Agreements",
            "Distribution Contracts",
            "Manufacturing Agreements"
        ],
        "use_cases": [
            "Review delivery terms and penalties",
            "Analyze quality standards and specifications",
            "Check payment terms and conditions",
            "Identify termination and renewal clauses",
            "Validate compliance and certification requirements"
        ]
    },
    "commercial": {
        "title": "Commercial Contracts",
        "icon": "🤝",
        "description": "General commercial contract analysis covering sales, partnerships, and business agreements.",
        "features": [
            "Sales Agreement Analysis",
            "Partnership Contracts",
            "Joint Venture Agreements",
            "Distribution Agreements",
            "Franchise Contracts",
            "Service Level Agreements"
        ],
        "use_cases": [
            "Review sales terms and conditions",
            "Analyze partnership responsibilities",
            "Check territorial and exclusivity rights",
            "Identify performance metrics and KPIs",
            "Validate dispute resolution mechanisms"
        ]
    }
}

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 4rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .get-started-btn {
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .get-started-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 2rem;
        font-size: 2rem;
        color: white;
        font-weight: bold;
    }
    
    .welcome-message {
        text-align: center;
        font-size: 1.5rem;
        color: #666;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        border: 2px dashed #2E86AB;
    }
    
    .chat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 2px solid #eee;
        margin-bottom: 2rem;
    }
    
    .back-btn {
        background: #f0f0f0;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    .create-session-btn {
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 1rem;
    }
    
    .hero-image {
        width: 100%;
        height: 400px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 1rem;
        background: transparent;
    }
    
    .input-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        background: white;
        padding: 1rem;
        border-radius: 25px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        border: 2px solid #eee;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .input-wrapper {
        position: relative;
        flex: 1;
    }
    
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #2E86AB;
        padding: 12px 50px 12px 20px;
        font-size: 1rem;
        width: 100%;
    }
    
    .send-btn-inside {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        color: white;
        border: none;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        transition: all 0.3s;
    }
    
    .send-btn-inside:hover {
        transform: translateY(-50%) scale(1.1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .clear-chat-btn {
        background: #f44336;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: bold;
        transition: all 0.3s;
        white-space: nowrap;
    }
    
    .clear-chat-btn:hover {
        background: #d32f2f;
        transform: translateY(-1px);
    }
    
    .stButton button {
        border-radius: 20px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
    }
    
    .toggle-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2rem;
        background: white;
        border-radius: 25px;
        padding: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 2px solid #eee;
        gap: 10px;
    }
    
    .toggle-option {
        padding: 10px 25px;
        margin: 0 5px;
        border-radius: 20px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s;
        background: transparent;
        color: #666;
        border: none;
        font-size: 1rem;
    }
    
    .toggle-option.active {
        background: linear-gradient(45deg, #2E86AB, #A23B72);
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .toggle-option:hover:not(.active) {
        background: #f0f0f0;
        color: #333;
    }
    
    .domain-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #eee;
        transition: all 0.3s;
    }
    
    .domain-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .domain-title {
        font-size: 2rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .domain-description {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .feature-list {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .feature-list h4 {
        color: #2E86AB;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .feature-item {
        background: white;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Hide Streamlit elements and unwanted components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide the white block overlay and form elements */
    .stAlert {display: none;}
    .stSuccess {display: none;}
    .stError {display: none;}
    .stWarning {display: none;}
    .stInfo {display: none;}
    
    /* Hide form container white box */
    .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Hide form submit button */
    .stForm button[kind="formSubmit"] {
        display: none !important;
    }
    
    /* Hide extra buttons but keep navigation buttons */
    .stButton {
        display: block;
    }
    
    /* Hide only specific unwanted buttons */
    .stButton button:contains("Send") {
        display: none;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 15px;
        border: 1px solid #eee;
    }

    /* Dropdown styling */
    .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid #2E86AB;
    }
</style>
""", unsafe_allow_html=True)

# HOME PAGE
# 👇 Domain switching logic at the top of your Streamlit app
query_params = st.experimental_get_query_params()
if "domain" in query_params:
    domain_key = query_params["domain"][0]
    if domain_key in DOMAIN_INFO:
        st.session_state.current_page = "domain"
        st.session_state.selected_domain = domain_key

if st.session_state.current_page == "home":
     st.markdown(f"""
     <style>
        .dropdown {{
            position: relative;
            display: inline-block;
        }}

        .dropdown-content {{
            display: none;
            position: absolute;
            background-color: white;
            min-width: 200px;
            box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
            border-radius: 10px;
            z-index: 1000;
            border: 2px solid #2E86AB;
        }}

        .dropdown-content a {{
            color: #333;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            border-radius: 8px;
            margin: 4px;
            font-weight: 500;
            transition: all 0.3s;
        }}

        .dropdown-content a:hover {{
            background: linear-gradient(45deg, #2E86AB, #A23B72);
            color: white;
            transform: translateX(5px);
        }}

        .dropdown:hover .dropdown-content {{
            display: block;
        }}

        .domain-icon {{
            margin-right: 8px;
            font-size: 1.1em;
        }}

        .toggle-bar {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .toggle-option {{
            background: linear-gradient(to right, #2E86AB, #A23B72);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            border: none;
        }}

        .toggle-option.active {{
            background: white !important;
            color: #2E86AB !important;
            border: 2px solid #2E86AB;
        }}
    </style>

    <div class="toggle-bar">
        <div class="dropdown">
            <button class="toggle-option active">Domains ▼</button>
            <div class="dropdown-content" id="domainDropdown">
                <a href="/?domain=tech"><span class="domain-icon">💻</span>Technology</a>
                <a href="/?domain=finance"><span class="domain-icon">💰</span>Finance</a>
                <a href="/?domain=health"><span class="domain-icon">🏥</span>Healthcare</a>
                <a href="/?domain=procurement"><span class="domain-icon">📦</span>Procurement</a>
                <a href="/?domain=commercial"><span class="domain-icon">🤝</span>Commercial</a>
            </div>
        </div>
          <button class="toggle-option {"active" if st.session_state.home_tab == "about" else ""}" onclick="selectTab('about')">About Us</button>
    </div>
    """, unsafe_allow_html=True)

 
     if st.session_state.home_tab == "domains":
        # Create two columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Logo and title section
            # st.markdown("""
            # <div class="logo-container">
            #     <div class="logo">CM</div>
            #     <div>
            #         <h1 class="main-title">CLAUSEMIND</h1>
            #     </div>
            # </div>
            # """, unsafe_allow_html=True)
            st.image("images/banner_left.jpg",use_column_width=True)
            
            st.markdown("""
            <p class="subtitle">
            Your intelligent contract assistant powered by advanced AI. 
            Analyze, review, and manage contracts with unprecedented accuracy and speed. 
            Transform your legal workflow with ClauseMind's cutting-edge technology.
            </p>
            """, unsafe_allow_html=True)
            
            # Get Started button in bottom left
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if st.button("🚀 Get Started", key="get_started", help="Start your contract analysis journey", use_container_width=False):
                st.session_state.current_page = "chat"
                st.rerun()
        
        with col2:
            # Hero image
            # st.markdown("""
            # <div class="hero-image">
            #     📋 Contract AI
            # </div>
            # """, unsafe_allow_html=True)
            st.image("images/banner_right.jpg", use_column_width=True)
    
    
elif st.session_state.home_tab == "about":
        st.markdown("""
        <div class="welcome-message">
            <h3>🏢 About ClauseMind</h3>
            <p>At ClauseMinds, we believe contracts shouldn't be complicated.
We’re building a next-gen AI-powered Contract Lifecycle Management (CLM) system that simplifies how businesses create, review, and manage legal agreements.
Powered by intelligent agents, ClauseMinds automates everything from drafting to clause analysis, compliance checking, approval routing, summarization, and secure storage — all in one seamless workflow.
Whether it’s a startup drafting its first NDA or an enterprise handling procurement workflows, ClauseMinds adapts to every need — fast, reliable, and built for the modern world.
With support for multiple domains like Tech, Healthcare, Finance, Procurement, and Legal, we’re on a mission to turn legal friction into fluid automation.</p>
            <br>
            <p><strong>Our Mission:</strong> To empower businesses with intelligent contract automation that saves time, reduces legal risks, and enhances decision-making — one clause at a time.</p>
        </div>
        """, unsafe_allow_html=True)

# DOMAIN PAGE
elif st.session_state.current_page == "domain":
    # Back button
    if st.button("← Back to Home", key="back_from_domain"):
      st.session_state.current_page = "home"
      st.session_state.home_tab = "domains"  # Ensure we return to domains tab
      st.rerun()

    # Domain information display
    if st.session_state.selected_domain and st.session_state.selected_domain in DOMAIN_INFO:
        domain_data = DOMAIN_INFO[st.session_state.selected_domain]
        
        # Domain card
        st.markdown(f"""
        <div class="domain-card">
            <div class="domain-title">
                <span>{domain_data['icon']}</span>
                <span>{domain_data['title']}</span>
            </div>
            <div class="domain-description">
                {domain_data["description"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Features and Use Cases in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-list">
                <h4>🔧 Key Features</h4>
            """, unsafe_allow_html=True)
            
            for feature in domain_data['features']:
                st.markdown(f'<div class="feature-item">{feature}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-list">
                <h4>💡 Use Cases</h4>
            """, unsafe_allow_html=True)
            
            for use_case in domain_data['use_cases']:
                st.markdown(f'<div class="feature-item">{use_case}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Get Started button for this domain
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"🚀 Start {domain_data['title']} Analysis", key="domain_get_started", use_container_width=True):
         st.session_state.current_page = "chat"
         st.rerun()

# CHAT PAGE
elif st.session_state.current_page == "chat":
    # Chat header with back button and create session
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Home", key="back_home"):
            go_to_home()
            st.rerun()
    
    with col2:
        st.markdown("<h2 style='text-align: center; color: #2E86AB;'>💬 ClauseMind Assistant</h2>", unsafe_allow_html=True)
    
    with col3:
        if not st.session_state.session_id:
            if st.button("🆕 Create Session", key="create_session_top"):
                create_session()
                st.rerun()
    
    # Welcome message (shown when no messages)
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-message">
            <h3>👋 Welcome boss, what can I do for ya?</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat messages container with auto-scroll
    if st.session_state.messages:
        st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-scroll to bottom
        st.markdown("""
        <script>
            setTimeout(function() {
                const chatContainer = document.getElementById('chat-container');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
                // Also scroll the main page
                window.scrollTo(0, document.body.scrollHeight);
            }, 100);
        </script>
        """, unsafe_allow_html=True)
    
    
    # Fixed input at bottom


    input_col, clear_col = st.columns([9, 1])

    with input_col:
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message...",
                key="user_input_value",
                placeholder="Ask me about contracts, clauses, or legal terms...",
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("Send")

        if submitted and user_input.strip():
            send_message(user_input.strip())
            st.rerun()

    with clear_col:
        if st.button("🗑️", key="clear_btn", help="Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


    # Add some space for the fixed input
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
