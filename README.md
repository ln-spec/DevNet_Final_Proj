---

## `README.md`
```markdown
# San Rafael Disaster Alert GUI & Control Center Simulation

This Streamlit web dashboard serves as the visual Proof of Concept (PoC) presentation layer for **Scenario E (Municipality of San Rafael)** in the CSFE 1 Final Project course suite.

Local Installation & Execution Steps

Follow these steps to run the interactive dashboard prototype directly on your local developer station machine:

1. Install Python Libraries: Ensure you have Python installed on your device, then install required project dependencies via your terminal:
   ```bash
   pip install streamlit pandas
   ```

2. Execute the Application Web App Server: Run the Streamlit initialization script string via command shell context:
   ```bash
   streamlit run app.py
   ```

3. Interact with the Presentation Dashboard: A web browser window will automatically launch at address `http://localhost:8501`. Use the toggle switches on the sidebar panel configuration block to trigger simulated typhoon server downtime and observe automated routing changes.

## Strategic Features

- **Tab 1 (Live System Status):** Demonstrates how the design implements network layer architecture failover resilience. Toggling a disaster state displays how routing adjustments can protect overall service uptime limits dynamically.
- **Tab 2 (Barangay Portal):** Validates REST API outcome compliance (**CO2**). Simulates input authentication checking mechanisms and structured event logging processing.
- **Tab 3 (Terraform View):** Displays the verified infrastructure as code config mapping, confirming full infrastructure generation capabilities offline.
