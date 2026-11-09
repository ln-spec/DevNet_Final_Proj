import streamlit as st
import pandas as pd
import datetime
import uuid

# Page Configuration for Client-Ready Delivery
st.set_page_config(
    page_title="San Rafael E-Gov Disaster Dashboard",
    page_icon="⛈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States for Persisting Simulation Data
if "incidents_log" not in st.session_state:
    st.session_state.incidents_log = []
if "typhoon_active" not in st.session_state:
    st.session_state.typhoon_active = False

# Application Header & Project Metadata
st.title("⛈️ Municipality of San Rafael")
st.subheader("E-Government & Disaster Alerts Control Center — DevNet Solution Blueprint")
st.caption("⚠️ DEMO ONLY — Academic Simulation for CSFE 1 Final Project Team Consulting Defense")

st.markdown("---")

# Sidebar Configuration and Infrastructure Control Panel
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    st.markdown("Use these switches to simulate real-world failure events in Western Visayas during a Typhoon.")

    # Critical Disaster Toggle Switch
    if st.checkbox("🚨 Simulate Typhoon Impact", value=st.session_state.typhoon_active,
                   help="Toggling this simulates full power and physical network loss at San Rafael Town Hall."):
        st.session_state.typhoon_active = True
    else:
        st.session_state.typhoon_active = False

    st.markdown("---")
    st.markdown("### 📋 Project Metadata")
    st.markdown(
        "**Client:** Municipality of San Rafael\n\n**Scenario:** E-Government and Disaster Alerts\n\n**SDLC Framework:** GitOps / DevOps CI/CD\n\n**Target Architecture:** Redundant Cloud Failover VPC")

# Main Interface Tab Navigation
tab1, tab2, tab3 = st.tabs(["📊 Live System Status", "📣 Barangay Alert Portal", "🛠️ Terraform Infrastructure IaC"])

# TAB 1: LIVE SYSTEM STATUS & CRITICAL FAILOVER MONITORING
with tab1:
    st.header("📊 Infrastructure Health & Observability Network")

    # Dynamic KPI metric layout based on simulation state
    col1, col2, col3 = st.columns(3)

    with col1:
        if not st.session_state.typhoon_active:
            st.metric(label="Town Hall Core Network", value="ONLINE", delta="Healthy (100% On-Premise)")
        else:
            st.metric(label="Town Hall Core Network", value="CRITICAL OFFLINE", delta="-100% Power/Link Failure",
                      delta_color="inverse")

    with col2:
        if not st.session_state.typhoon_active:
            st.metric(label="AWS Cloud Backup Node", value="STANDBY", delta="Synchronized (0% Active Load)")
        else:
            st.metric(label="AWS Cloud Backup Node", value="ACTIVE FAILOVER",
                      delta="Active Traffic Route (GitOps Executed)", delta_color="normal")

    with col3:
        availability_rate = "99.9%" if not st.session_state.typhoon_active else "99.1% (Rerouted)"
        st.metric(label="Overall Service Availability", value=availability_rate,
                  help="Client SLO target: 99.9% Availability")

    # Visual Architecture Alert Boxes
    if st.session_state.typhoon_active:
        st.error(
            "🚨 **CRITICAL NETWORK EVENT:** Physical link to San Rafael Town Hall Server Room destroyed by heavy wind/flooding. BGP routing metrics broken.")
        st.success(
            "🔄 **AUTOMATED FAILOVER ACTIVE:** Intersight & Cloudflare CDN DNS have successfully migrated active user traffic endpoints away from local hardware to the fallback Cloud environment.")
    else:
        st.info(
            "🟢 **NORMAL STATUS:** All business permit services and municipal APIs are processing requests through the core on-premise town hall servers.")

# TAB 2: BARANGAY EMERGENCY ALERT API PROTOTYPE FORM
with tab2:
    st.header("📣 Secure Barangay Disaster Alert Submission Node")
    st.markdown(
        "This component acts as an interface interacting with the REST API endpoint `/api/v1/alerts` to securely accept barangay emergency data feeds.")

    # Setup Mock API request input layout fields
    with st.form("api_alert_form", clear_on_submit=True):
        col_left, col_right = st.columns(2)

        with col_left:
            barangay_name = st.selectbox("Select Origin Barangay",
                                         ["Poblacion", "San Roque", "Bagumbayan", "Mabini", "Rizal", "Maligaya"])
            incident_type = st.selectbox("Incident Classification Type",
                                         ["Flooding", "Landslide", "Power Outage", "Structural Damage"])

        with col_right:
            alert_level = st.select_slider("Disaster Alert Urgency Level", options=["Info", "Warning", "Critical"])
            api_token = st.text_input("Barangay API Bearer Token Authentication", type="password",
                                      help="Secure JWT/OAuth 2.0 validation value matching client data requirements.")

        details = st.text_area("Situation Details & On-Ground Assessment Description")

        submit_btn = st.form_submit_button("Broadcast Emergency Notification Update")

        if submit_btn:
            # API Form Server-Side Verification Checks
            if not api_token:
                st.error(
                    "⛔ **401 Unauthorized API Exception:** Submit aborted. Missing security token context in Authorization header payload.")
            elif len(details) < 10:
                st.warning(
                    "⚠️ **422 Unprocessable Entity:** Incident report details are too brief. Please provide a clear on-ground statement.")
            else:
                # Add valid alert map dict to local state storage data tracking engine
                new_alert = {
                    "Alert ID": str(uuid.uuid4())[:8].upper(),
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Barangay": barangay_name,
                    "Type": incident_type,
                    "Urgency": alert_level,
                    "Details": details
                }
                st.session_state.incidents_log.insert(0, new_alert)

                # Visual UI notifications representing the automated REST API payload handling sequence
                st.success(
                    "✅ **HTTP Status Code 201 Created:** Alert data accepted successfully by backend server infrastructure.")
                st.toast("⚡ REST API Call Successful: 201 Created", icon="📥")
                st.toast("📱 SMS Gateway Triggered: Broadcasting alerts to citizens...", icon="💬")

    # Live Event Incident History Table Display Pane
    st.markdown("### 📋 Live Broadcasting Alert & Active Incidents Stream Log")
    if st.session_state.incidents_log:
        df_log = pd.DataFrame(st.session_state.incidents_log)
        st.dataframe(df_log, use_container_width=True, hide_index=True)
    else:
        st.info(
            "No active emergency incident alerts registered during the current dashboard session tracker framework.")

# TAB 3: INFRASTRUCTURE AS CODE SYNTAX VISUALIZER
with tab3:
    st.header("🛠️ Infrastructure as Code Automation Engine Verification")
    st.markdown(
        "The following text output displays your static dry-run baseline verification framework generated using `terraform plan`. This explicitly confirms validation compliance for project outcome **CO5**.")

    mock_tf_plan = """
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_vpc.main will be created
  + resource "aws_vpc" "main" {
      + arn                                  = (known after apply)
      + cidr_block                           = "10.0.0.0/16"
      + enable_dns_hostnames                 = true
      + enable_dns_support                   = true
      + id                                   = (known after apply)
      + tags                                 = {
          + "Environment" = "disaster-recovery"
          + "ManagedBy"   = "Terraform"
          + "Project"     = "San-Rafael-E-Government"
          + "Name"        = "san-rafael-vpc"
        }
    }

  # aws_subnet.public[0] will be created
  + resource "aws_subnet" "public" {
      + availability_zone       = "ap-southeast-1a"
      + cidr_block              = "10.0.0.0/24"
      + id                      = (known after apply)
      + map_public_ip_on_launch = true
      + vpc_id                  = (known after apply)
    }

  # aws_subnet.private[0] will be created
  + resource "aws_subnet" "private" {
      + availability_zone       = "ap-southeast-1a"
      + cidr_block              = "10.0.10.0/24"
      + id                      = (known after apply)
      + vpc_id                  = (known after apply)
    }

  # aws_security_group.web will be created
  + resource "aws_security_group" "web" {
      + description = "Public HTTP and HTTPS access to the portal only."
      + id          = (known after apply)
      + name        = "san-rafael-web-sg"
      + vpc_id      = (known after apply)

      + ingress {
          + cidr_blocks = [ "0.0.0.0/0" ]
          + description = "HTTPS"
          + from_port   = 443
          + protocol    = "tcp"
          + to_port     = 443
        }
      + ingress {
          + cidr_blocks = [ "0.0.0.0/0" ]
          + description = "HTTP"
          + from_port   = 80
          + protocol    = "tcp"
          + to_port     = 80
        }
    }

  # aws_instance.portal will be created
  + resource "aws_instance" "portal" {
      + ami                          = "ami-mockid12345678"
      + instance_type                = "t3.micro"
      + id                           = (known after apply)
      + user_data                    = "a01b2c3d4e5f..." # Installs Nginx Disaster Dashboard
      + root_block_device {
          + encrypted   = true
          + volume_size = 8
          + volume_type = "gp3"
        }
    }

Plan: 14 to add, 0 to change, 0 to destroy.
─────────────────────────────────────────────────────────────────────────────────────────────
Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take
these exact actions if you run "terraform apply" now.
    """
