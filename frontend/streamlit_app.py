import streamlit as st
import requests

API_BASE = st.secrets.get("api_base_url", "http://localhost:8000/api")

st.set_page_config(page_title="AgentOps Dashboard", layout="wide")

st.title("AgentOps AI Workflow Orchestration")

col1, col2 = st.columns([2, 1])
with col1:
    st.header("Start a new workflow")
    with st.form("new_workflow"):
        name = st.text_input("Workflow name")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["low", "normal", "high", "urgent"])
        input_document = st.text_area("Input business document")
        approval_required = st.checkbox("Require human approval", value=True)
        submitted = st.form_submit_button("Launch workflow")
        if submitted:
            payload = {
                "name": name,
                "description": description,
                "priority": priority,
                "input_document": input_document,
                "approval_required": approval_required,
            }
            response = requests.post(f"{API_BASE}/workflows/", json=payload)
            if response.ok:
                st.success("Workflow created successfully")
                st.json(response.json())
            else:
                st.error(response.text)

with col2:
    st.header("Metrics")
    metrics = requests.get(f"{API_BASE}/metrics/summary").json()
    st.metric("Total workflows", metrics.get("total_workflows"))
    st.metric("Pending approvals", metrics.get("approvals_pending"))
    st.metric("Completed", metrics.get("completed_workflows"))
    st.metric("Failed", metrics.get("failed_workflows"))

st.markdown("---")

st.header("Recent workflows")
workflows = requests.get(f"{API_BASE}/workflows/").json()
for workflow in workflows:
    with st.expander(f"#{workflow['id']} - {workflow['name']} ({workflow['status']})"):
        st.write(f"**Priority:** {workflow['priority']}")
        st.write(f"**Approval required:** {workflow['approval_required']}")
        st.write(f"**Approved:** {workflow['approved']}")
        st.write("**Summary:**")
        st.write(workflow.get("output_summary", "No summary yet."))
        if workflow['status'] == 'approval_pending':
            approval = st.radio(f"Approve workflow {workflow['id']}?", ["Approve", "Reject"], key=f"approve_{workflow['id']}")
            if st.button("Submit decision", key=f"decision_{workflow['id']}"):
                decision = approval == "Approve"
                decision_payload = {"workflow_id": workflow['id'], "approved": decision}
                result = requests.post(f"{API_BASE}/workflows/approve", json=decision_payload)
                if result.ok:
                    st.success("Decision recorded")
                else:
                    st.error(result.text)

st.markdown("---")
st.header("Agent logs")
workflow_id = st.number_input("Filter logs by workflow ID", min_value=0, value=0)
params = {"workflow_id": workflow_id} if workflow_id else {}
logs = requests.get(f"{API_BASE}/agents/logs", params=params).json()
for log in logs[:20]:
    with st.expander(f"{log['agent_name']} - workflow {log['workflow_id']}"):
        st.write(f"Status: {log['status']}")
        st.write(f"Latency: {log['latency_ms']} ms")
        st.write(f"Retries: {log['retries']}")
        st.write("**Prompt**")
        st.write(log['prompt'])
        st.write("**Response**")
        st.write(log['response'])

st.markdown("---")
st.header("RAG Demo")
with st.form("rag_form"):
    rag_doc = st.text_area("Document for retrieval")
    rag_question = st.text_input("Question")
    rag_submit = st.form_submit_button("Ask")
    if rag_submit:
        payload = {"document": rag_doc, "question": rag_question}
        res = requests.post(f"{API_BASE}/agents/rag/query", json=payload)
        if res.ok:
            st.success("Answer")
            st.write(res.json().get("answer"))
        else:
            st.error(res.text)
