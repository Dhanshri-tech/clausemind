# 🧠 Multi-Agent Contract Lifecycle Management (CLM) System

An AI-powered Contract Lifecycle Management platform built with Google Agent Development Kit (ADK), MongoDB, and Streamlit. This system handles automated contract creation, review, approval, and summarization — customized for multiple domains.

---

## 🚀 Features

- 🤖 **Multi-Agent Architecture:** Agents for clause analysis, compliance, approval, summarization, and alerts.
- 🏥 **Multi-Domain Support:** Healthcare, Telecom, Tech/IT, Procurement, Finance, and Legal.
- 💾 **MongoDB Integration:** Robust storage for contracts, logs, and agent actions.
- 💻 **Interactive UI:** Built with Streamlit and styled with TailwindCSS.
- 🧠 **Smart Templates:** Each domain includes customizable contract templates.
- 🔁 **Automated Workflow:** All agents run in a structured pipeline without manual triggering.

---

## 🛠️ Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | Streamlit + TailwindCSS             |
| Backend     | Python + Google ADK (agent toolkit) |
| Database    | MongoDB                             |
| Infra       | Localhost / GitHub (demo)           |

---

## 👩‍💻 Team

We are a passionate team of three who worked collaboratively to build this project:

- **Dhanshri** – 🛢️ MongoDB integration, database schema design, agent logs
- **Anushree** – 📝 Template creation, documentation, domain research
- **Ram** – 🔌 UI-agent connection, Streamlit workflow

---

## 📂 Project Structure

multi-agent-clm/
├── app.py                        # Streamlit entry point
├── manager/                     # Core logic & orchestration
│   ├── Database/                # MongoDB interactions
│   ├── sub_agents/             # All intelligent agents
│   │   ├── approval/           → Approval Agent logic
│   │   ├── audit_versioning_agent/ → Tracks clause versions
│   │   ├── clause_analysis/    → Clause classification logic
│   │   ├── compliance/         → Rule-based compliance agent
│   │   ├── creation/           → Drafts initial contracts
│   │   ├── negotiation/        → Recommends edits
│   │   ├── storage/            → Manages word export / local handling
│   │   └── summary/            → Generates contract summary
│   ├── tools/                  # Utilities (prompt loader, etc.)
│   |
│   └── .env                    # Secrets & configs
|     |-----─ agent.py                # Root orchestrator
├── README.md                   # Project overview
---

## 🧪 How to Run

1. **Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-clm.git
cd multi-agent-clm

2. **Install Requirements**

pip install -r requirements.txt

3. Start MongoDB (it's running locally or via cloud) 
 
4. **Run the Streamlit App**
   streamlit run streamlit_app.py

✨ Future Enhancements
Integration with Vertex AI and LangChain
Dashboard for admin analytics and approval trends
PDF generation of contracts with clause highlights
Alert agent with Slack/Email integration
Signature module and version history tracking

⭐ Give us a star!
If you like the project or found it helpful, consider giving it a ⭐ and sharing feedback!
