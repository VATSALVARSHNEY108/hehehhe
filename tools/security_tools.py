import streamlit as st
import hashlib
import secrets
import ssl
import socket
import subprocess
import platform
import os
import sys
import time
import random
import string
import json
import urllib.parse
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all security and privacy tools"""

    tool_categories = {
        "Authentication & Access Control": [
            "PAM Tools", "SSO Solutions", "MFA Tools", "IAM Platforms", "Access Review"
        ],
        "Antivirus & Endpoint Security": [
            "Antivirus Scanner", "Behavioral Analysis", "EDR Tools", "Mobile Security", "Patch Management"
        ],
        "Network Security": [
            "Firewall Configuration", "IDS/IPS", "NAC", "VPN Testing", "Network Segmentation"
        ],
        "Encryption Tools": [
            "File Encryption", "Email Encryption", "Database Encryption", "Key Management", "Digital Signatures"
        ],
        "Privacy Tools": [
            "VPN Testing", "Privacy Auditing", "Anonymous Browsing", "Data Anonymization", "GDPR Compliance"
        ],
        "Vulnerability Assessment": [
            "Network Scanner", "Web App Testing", "Compliance Reporting", "Penetration Testing", "Risk Assessment"
        ],
        "Web Security": [
            "Website Scanner", "SQL Injection Detector", "XSS Analysis", "SSL/TLS Validator", "HTTPS Checker"
        ],
        "Security Monitoring": [
            "Log Analysis", "SIEM Simulation", "Threat Intelligence", "Anomaly Detection", "Incident Response"
        ],
        "Cloud Security": [
            "CASB Simulation", "Container Security", "Configuration Auditing", "Workload Protection", "Cloud Compliance"
        ],
        "Mobile & IoT Security": [
            "Device Assessment", "App Security Testing", "IoT Vulnerability Scanning", "Mobile Threat Defense",
            "Device Management"
        ],
        "GRC Tools": [
            "Risk Assessment", "Compliance Tracking", "Policy Management", "Audit Trails", "Risk Registers"
        ],
        "Digital Forensics": [
            "Evidence Acquisition", "Incident Response", "Malware Analysis", "Data Recovery", "Chain of Custody"
        ],
        "Password Management": [
            "Password Generation", "Strength Testing", "Breach Checking", "Policy Enforcement", "Credential Vault"
        ],
        "Network Analysis": [
            "Traffic Analysis", "Bandwidth Monitoring", "Protocol Analysis", "Network Mapping", "Performance Testing"
        ],
        "Red Team Operations": [
            "Social Engineering", "Phishing Simulation", "Attack Vector Analysis", "Payload Generation",
            "Exploitation Framework"
        ],
        "Backup & Recovery": [
            "Backup Testing", "Disaster Recovery", "Data Integrity", "Recovery Planning", "Business Continuity"
        ],
        "Security Training": [
            "Awareness Training", "Phishing Simulation", "Security Assessment", "Training Metrics", "Skill Development"
        ]
    }

    selected_category = st.selectbox("Select Security Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Security Tools - {selected_tool}")

    # Display educational disclaimer
    st.warning(
        "🔒 **Educational Purpose Only**: These tools are for educational and authorized testing purposes only. Always obtain proper authorization before testing systems you don't own.")

    # Display selected tool
    if selected_tool == "File Encryption":
        file_encryption()
    elif selected_tool == "Password Generation":
        password_generation()
    elif selected_tool == "Network Scanner":
        network_scanner()
    elif selected_tool == "SSL/TLS Validator":
        ssl_tls_validator()
    elif selected_tool == "Risk Assessment":
        risk_assessment()
    elif selected_tool == "Phishing Simulation":
        phishing_simulation()
    elif selected_tool == "Log Analysis":
        log_analysis()
    elif selected_tool == "Vulnerability Assessment":
        vulnerability_assessment()
    elif selected_tool == "Web App Testing":
        web_app_testing()
    elif selected_tool == "Privacy Auditing":
        privacy_auditing()
    elif selected_tool == "Incident Response":
        incident_response()
    elif selected_tool == "Security Training":
        security_training()
    elif selected_tool == "Compliance Tracking":
        compliance_tracking()
    elif selected_tool == "Threat Intelligence":
        threat_intelligence()
    elif selected_tool == "Digital Signatures":
        digital_signatures()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def file_encryption():
    """File encryption and decryption tool"""
    create_tool_header("File Encryption", "Encrypt and decrypt files securely", "🔐")

    operation = st.radio("Select Operation", ["Encrypt", "Decrypt"])

    if operation == "Encrypt":
        st.subheader("File Encryption")
        uploaded_files = FileHandler.upload_files(['txt', 'pdf', 'docx', 'jpg', 'png'], accept_multiple=True)

        if uploaded_files:
            password = st.text_input("Encryption Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                    return

                if st.button("Encrypt Files"):
                    encrypted_files = {}

                    # Generate key from password
                    key = hashlib.sha256(password.encode()).digest()
                    key_b64 = base64.urlsafe_b64encode(key)
                    fernet = Fernet(key_b64)

                    progress_bar = st.progress(0)

                    for i, uploaded_file in enumerate(uploaded_files):
                        try:
                            # Read file data
                            file_data = uploaded_file.read()

                            # Encrypt data
                            encrypted_data = fernet.encrypt(file_data)

                            # Store encrypted file
                            encrypted_filename = f"{uploaded_file.name}.encrypted"
                            encrypted_files[encrypted_filename] = encrypted_data

                            progress_bar.progress((i + 1) / len(uploaded_files))

                        except Exception as e:
                            st.error(f"Error encrypting {uploaded_file.name}: {str(e)}")

                    if encrypted_files:
                        if len(encrypted_files) == 1:
                            filename, data = next(iter(encrypted_files.items()))
                            FileHandler.create_download_link(data, filename, "application/octet-stream")
                        else:
                            zip_data = FileHandler.create_zip_archive(encrypted_files)
                            FileHandler.create_download_link(zip_data, "encrypted_files.zip", "application/zip")

                        st.success(f"Encrypted {len(encrypted_files)} file(s) successfully!")
                        st.info("🔑 Keep your password safe! You'll need it to decrypt these files.")

    else:  # Decrypt
        st.subheader("File Decryption")
        uploaded_files = FileHandler.upload_files(['encrypted'], accept_multiple=True)

        if uploaded_files:
            password = st.text_input("Decryption Password", type="password")

            if password and st.button("Decrypt Files"):
                decrypted_files = {}

                # Generate key from password
                key = hashlib.sha256(password.encode()).digest()
                key_b64 = base64.urlsafe_b64encode(key)
                fernet = Fernet(key_b64)

                progress_bar = st.progress(0)

                for i, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Read encrypted data
                        encrypted_data = uploaded_file.read()

                        # Decrypt data
                        decrypted_data = fernet.decrypt(encrypted_data)

                        # Remove .encrypted extension
                        original_filename = uploaded_file.name.replace('.encrypted', '')
                        decrypted_files[original_filename] = decrypted_data

                        progress_bar.progress((i + 1) / len(uploaded_files))

                    except Exception as e:
                        st.error(f"Error decrypting {uploaded_file.name}: {str(e)} (Wrong password?)")

                if decrypted_files:
                    if len(decrypted_files) == 1:
                        filename, data = next(iter(decrypted_files.items()))
                        FileHandler.create_download_link(data, filename, "application/octet-stream")
                    else:
                        zip_data = FileHandler.create_zip_archive(decrypted_files)
                        FileHandler.create_download_link(zip_data, "decrypted_files.zip", "application/zip")

                    st.success(f"Decrypted {len(decrypted_files)} file(s) successfully!")


def password_generation():
    """Advanced password generation and testing"""
    create_tool_header("Password Generation", "Generate and test secure passwords", "🔑")

    tab1, tab2, tab3 = st.tabs(["Generate", "Test Strength", "Policy Check"])

    with tab1:
        st.subheader("Password Generator")

        col1, col2 = st.columns(2)
        with col1:
            length = st.slider("Password Length", 8, 128, 16)
            include_uppercase = st.checkbox("Uppercase Letters (A-Z)", True)
            include_lowercase = st.checkbox("Lowercase Letters (a-z)", True)
            include_numbers = st.checkbox("Numbers (0-9)", True)
            include_symbols = st.checkbox("Symbols (!@#$%^&*)", True)

        with col2:
            exclude_ambiguous = st.checkbox("Exclude Ambiguous Characters", True)
            exclude_similar = st.checkbox("Exclude Similar Characters", False)
            must_include_all = st.checkbox("Must Include All Selected Types", True)
            num_passwords = st.slider("Number of Passwords", 1, 50, 5)

        if st.button("Generate Passwords"):
            try:
                passwords = generate_secure_passwords(
                    length, num_passwords, include_uppercase, include_lowercase,
                    include_numbers, include_symbols, exclude_ambiguous,
                    exclude_similar, must_include_all
                )

                if passwords:
                    st.subheader("Generated Passwords")
                    for i, pwd in enumerate(passwords, 1):
                        strength = calculate_password_strength(pwd)
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.code(pwd)
                        with col2:
                            color = "green" if strength >= 80 else "orange" if strength >= 60 else "red"
                            st.markdown(f"<span style='color: {color}'>Strength: {strength}%</span>",
                                        unsafe_allow_html=True)

                    # Download option
                    password_text = '\n'.join(passwords)
                    FileHandler.create_download_link(password_text.encode(), "generated_passwords.txt", "text/plain")
                else:
                    st.error("Could not generate passwords with the specified criteria.")
            except Exception as e:
                st.error(f"Error generating passwords: {str(e)}")

    with tab2:
        st.subheader("Password Strength Tester")

        test_password = st.text_input("Enter password to test", type="password")

        if test_password:
            strength = calculate_password_strength(test_password)

            # Display strength meter
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.progress(strength / 100)
            with col2:
                color = "green" if strength >= 80 else "orange" if strength >= 60 else "red"
                st.markdown(f"<h3 style='color: {color}'>{strength}%</h3>", unsafe_allow_html=True)
            with col3:
                if strength >= 80:
                    st.success("Strong")
                elif strength >= 60:
                    st.warning("Medium")
                else:
                    st.error("Weak")

            # Detailed analysis
            analysis = analyze_password_details(test_password)
            st.subheader("Detailed Analysis")

            for category, result in analysis.items():
                icon = "✅" if result['status'] else "❌"
                st.write(f"{icon} **{category}**: {result['message']}")

    with tab3:
        st.subheader("Password Policy Checker")

        # Policy settings
        st.write("Define Password Policy:")
        col1, col2 = st.columns(2)
        with col1:
            min_length = st.number_input("Minimum Length", 1, 50, 8)
            require_uppercase = st.checkbox("Require Uppercase", True)
            require_lowercase = st.checkbox("Require Lowercase", True)
        with col2:
            require_numbers = st.checkbox("Require Numbers", True)
            require_symbols = st.checkbox("Require Symbols", True)
            max_repeating = st.number_input("Max Repeating Characters", 1, 10, 3)

        test_policy_password = st.text_input("Test password against policy", type="password")

        if test_policy_password and st.button("Check Policy Compliance"):
            compliance = check_password_policy(
                test_policy_password, min_length, require_uppercase,
                require_lowercase, require_numbers, require_symbols, max_repeating
            )

            st.subheader("Policy Compliance Results")
            overall_pass = all(result['status'] for result in compliance.values())

            if overall_pass:
                st.success("✅ Password meets all policy requirements!")
            else:
                st.error("❌ Password does not meet policy requirements.")

            for check, result in compliance.items():
                icon = "✅" if result['status'] else "❌"
                st.write(f"{icon} **{check}**: {result['message']}")


def network_scanner():
    """Network scanning and discovery tool (educational simulation)"""
    create_tool_header("Network Scanner", "Network discovery and port scanning (Educational)", "🌐")

    st.warning(
        "⚠️ **Educational Simulation**: This tool provides educational examples of network scanning concepts. Always obtain authorization before scanning networks.")

    scan_type = st.selectbox("Scan Type", ["Host Discovery", "Port Scan", "Service Detection", "Vulnerability Scan"])

    if scan_type == "Host Discovery":
        st.subheader("Host Discovery Simulation")

        network_range = st.text_input("Network Range (e.g., 192.168.1.0/24)", "192.168.1.0/24")

        if st.button("Simulate Host Discovery"):
            show_progress_bar("Scanning network range", 3)

            # Simulate discovered hosts
            simulated_hosts = generate_simulated_hosts()

            st.subheader("Discovered Hosts (Simulated)")
            for host in simulated_hosts:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**IP**: {host['ip']}")
                with col2:
                    st.write(f"**Status**: {host['status']}")
                with col3:
                    st.write(f"**Response Time**: {host['response_time']}ms")

            # Generate report
            report = generate_host_discovery_report(simulated_hosts)
            FileHandler.create_download_link(report.encode(), "host_discovery_report.txt", "text/plain")

    elif scan_type == "Port Scan":
        st.subheader("Port Scanning Simulation")

        target_ip = st.text_input("Target IP", "192.168.1.1")
        port_range = st.text_input("Port Range", "1-1000")

        if st.button("Simulate Port Scan"):
            show_progress_bar("Scanning ports", 4)

            # Simulate port scan results
            open_ports = generate_simulated_ports()

            st.subheader("Open Ports (Simulated)")
            for port in open_ports:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Port**: {port['port']}")
                with col2:
                    st.write(f"**Service**: {port['service']}")
                with col3:
                    st.write(f"**State**: {port['state']}")

            # Generate report
            report = generate_port_scan_report(target_ip, open_ports)
            FileHandler.create_download_link(report.encode(), "port_scan_report.txt", "text/plain")


def ssl_tls_validator():
    """SSL/TLS certificate validator"""
    create_tool_header("SSL/TLS Validator", "Validate SSL/TLS certificates and configurations", "🔒")

    hostname = st.text_input("Hostname/Domain", placeholder="example.com")
    port = st.number_input("Port", min_value=1, max_value=65535, value=443)

    if hostname and st.button("Validate SSL/TLS"):
        try:
            show_progress_bar("Checking SSL/TLS certificate", 2)

            # Create SSL context
            context = ssl.create_default_context()

            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()

                    st.success("✅ SSL/TLS connection successful!")

                    # Certificate details
                    st.subheader("Certificate Information")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Subject**: {cert.get('subject', 'N/A')}")
                        st.write(f"**Issuer**: {cert.get('issuer', 'N/A')}")
                        st.write(f"**Version**: {cert.get('version', 'N/A')}")

                    with col2:
                        st.write(f"**Not Before**: {cert.get('notBefore', 'N/A')}")
                        st.write(f"**Not After**: {cert.get('notAfter', 'N/A')}")
                        st.write(f"**Serial Number**: {cert.get('serialNumber', 'N/A')}")

                    # Cipher information
                    st.subheader("Cipher Information")
                    if cipher:
                        st.write(f"**Cipher**: {cipher[0]}")
                        st.write(f"**Protocol**: {cipher[1]}")
                        st.write(f"**Key Length**: {cipher[2]} bits")

                    # Security assessment
                    st.subheader("Security Assessment")

                    # Check expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days

                    if days_until_expiry > 30:
                        st.success(f"✅ Certificate valid for {days_until_expiry} days")
                    elif days_until_expiry > 0:
                        st.warning(f"⚠️ Certificate expires in {days_until_expiry} days")
                    else:
                        st.error("❌ Certificate has expired!")

                    # Protocol check
                    if cipher and cipher[1] in ['TLSv1.2', 'TLSv1.3']:
                        st.success(f"✅ Secure protocol: {cipher[1]}")
                    else:
                        st.warning(f"⚠️ Consider upgrading protocol: {cipher[1] if cipher else 'Unknown'}")

                    # Generate detailed report
                    report = generate_ssl_report(hostname, port, cert, cipher, days_until_expiry)
                    FileHandler.create_download_link(report.encode(), f"ssl_report_{hostname}.txt", "text/plain")

        except socket.gaierror:
            st.error("❌ Could not resolve hostname")
        except socket.timeout:
            st.error("❌ Connection timeout")
        except ssl.SSLError as e:
            st.error(f"❌ SSL Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def risk_assessment():
    """Security risk assessment tool"""
    create_tool_header("Risk Assessment", "Assess and calculate security risks", "⚠️")

    st.subheader("Risk Assessment Framework")

    # Risk categories
    risk_categories = {
        "Data Security": ["Data Breach", "Data Loss", "Unauthorized Access", "Data Corruption"],
        "Network Security": ["Network Intrusion", "DDoS Attack", "Man-in-the-Middle", "DNS Poisoning"],
        "Application Security": ["SQL Injection", "XSS", "CSRF", "Authentication Bypass"],
        "Physical Security": ["Unauthorized Access", "Theft", "Natural Disasters", "Equipment Failure"],
        "Human Factors": ["Social Engineering", "Insider Threat", "Human Error", "Lack of Training"]
    }

    selected_category = st.selectbox("Risk Category", list(risk_categories.keys()))
    selected_risk = st.selectbox("Specific Risk", risk_categories[selected_category])

    st.markdown("---")

    # Risk scoring
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Likelihood")
        likelihood = st.slider("Probability of occurrence (1-5)", 1, 5, 3)
        likelihood_desc = ["Very Low", "Low", "Medium", "High", "Very High"]
        st.write(f"**{likelihood_desc[likelihood - 1]}**")

    with col2:
        st.subheader("Impact")
        impact = st.slider("Impact if occurs (1-5)", 1, 5, 3)
        impact_desc = ["Minimal", "Minor", "Moderate", "Major", "Severe"]
        st.write(f"**{impact_desc[impact - 1]}**")

    with col3:
        st.subheader("Current Controls")
        controls = st.slider("Effectiveness of controls (1-5)", 1, 5, 3)
        controls_desc = ["None", "Weak", "Adequate", "Strong", "Excellent"]
        st.write(f"**{controls_desc[controls - 1]}**")

    # Calculate risk score
    raw_risk = likelihood * impact
    residual_risk = raw_risk * (6 - controls) / 5

    st.markdown("---")
    st.subheader("Risk Assessment Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Raw Risk Score", f"{raw_risk}/25")
        if raw_risk >= 20:
            st.error("Critical Risk")
        elif raw_risk >= 15:
            st.warning("High Risk")
        elif raw_risk >= 9:
            st.warning("Medium Risk")
        else:
            st.success("Low Risk")

    with col2:
        st.metric("Residual Risk Score", f"{residual_risk:.1f}/25")
        if residual_risk >= 15:
            st.error("Critical Risk")
        elif residual_risk >= 10:
            st.warning("High Risk")
        elif residual_risk >= 5:
            st.warning("Medium Risk")
        else:
            st.success("Low Risk")

    with col3:
        risk_reduction = ((raw_risk - residual_risk) / raw_risk * 100) if raw_risk > 0 else 0
        st.metric("Risk Reduction", f"{risk_reduction:.1f}%")

    # Recommendations
    st.subheader("Recommendations")
    recommendations = generate_risk_recommendations(selected_risk, residual_risk, controls)
    for rec in recommendations:
        st.write(f"• {rec}")

    # Generate risk report
    if st.button("Generate Risk Report"):
        report_data = {
            "category": selected_category,
            "risk": selected_risk,
            "likelihood": likelihood,
            "impact": impact,
            "controls": controls,
            "raw_risk": raw_risk,
            "residual_risk": residual_risk,
            "recommendations": recommendations,
            "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        report = generate_detailed_risk_report(report_data)
        FileHandler.create_download_link(report.encode(), f"risk_assessment_{selected_risk.replace(' ', '_')}.txt",
                                         "text/plain")


def phishing_simulation():
    """Phishing awareness and simulation tool"""
    create_tool_header("Phishing Simulation", "Educational phishing awareness and testing", "🎣")

    st.warning("📚 **Educational Purpose**: This tool is for awareness training and authorized testing only.")

    tab1, tab2, tab3 = st.tabs(["Phishing Detection", "Email Analysis", "Training Metrics"])

    with tab1:
        st.subheader("Phishing Email Detection Training")

        # Generate sample phishing scenarios
        if st.button("Generate Sample Phishing Email"):
            phishing_sample = generate_phishing_sample()

            st.subheader("Sample Email")
            st.text_area("Email Content", phishing_sample['content'], height=200, disabled=True)

            col1, col2 = st.columns(2)
            with col1:
                user_answer = st.radio("Is this email suspicious?", ["Legitimate", "Phishing"])
            with col2:
                if st.button("Check Answer"):
                    if (user_answer == "Phishing" and phishing_sample['is_phishing']) or \
                            (user_answer == "Legitimate" and not phishing_sample['is_phishing']):
                        st.success("✅ Correct! Good security awareness.")
                    else:
                        st.error("❌ Incorrect. Review the indicators below.")

                    st.subheader("Learning Points")
                    for indicator in phishing_sample['indicators']:
                        st.write(f"• {indicator}")

    with tab2:
        st.subheader("Email Security Analysis")

        email_content = st.text_area("Paste email content for analysis:", height=200)

        if email_content and st.button("Analyze Email"):
            analysis = analyze_email_security(email_content)

            st.subheader("Security Analysis Results")

            # Overall risk score
            risk_score = analysis['risk_score']
            if risk_score >= 80:
                st.error(f"🚨 High Risk: {risk_score}%")
            elif risk_score >= 50:
                st.warning(f"⚠️ Medium Risk: {risk_score}%")
            else:
                st.success(f"✅ Low Risk: {risk_score}%")

            # Detailed findings
            st.subheader("Findings")
            for finding in analysis['findings']:
                severity_color = {"High": "red", "Medium": "orange", "Low": "green"}
                color = severity_color.get(finding['severity'], "black")
                st.markdown(f"<span style='color: {color}'>**{finding['severity']}**: {finding['description']}</span>",
                            unsafe_allow_html=True)

    with tab3:
        st.subheader("Phishing Training Metrics")

        # Simulate training metrics
        metrics = generate_training_metrics()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Detection Rate", f"{metrics['detection_rate']}%")
        with col2:
            st.metric("False Positives", f"{metrics['false_positives']}%")
        with col3:
            st.metric("Training Completed", f"{metrics['training_completed']}%")
        with col4:
            st.metric("Improvement", f"+{metrics['improvement']}%")

        # Training recommendations
        st.subheader("Training Recommendations")
        recommendations = [
            "Focus on URL inspection training",
            "Improve sender verification awareness",
            "Practice attachment safety protocols",
            "Enhance urgency tactic recognition",
            "Regular phishing simulation exercises"
        ]

        for rec in recommendations:
            st.write(f"• {rec}")


def log_analysis():
    """Security log analysis tool"""
    create_tool_header("Log Analysis", "Analyze security logs for threats", "📊")

    # Log file upload
    uploaded_logs = FileHandler.upload_files(['log', 'txt', 'csv'], accept_multiple=True)

    if uploaded_logs:
        for log_file in uploaded_logs:
            st.subheader(f"Analyzing: {log_file.name}")

            try:
                log_content = FileHandler.process_text_file(log_file)

                # Basic log statistics
                lines = log_content.split('\n')
                total_lines = len(lines)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Log Entries", total_lines)
                with col2:
                    unique_ips = len(set(extract_ips_from_logs(log_content)))
                    st.metric("Unique IP Addresses", unique_ips)
                with col3:
                    error_count = sum(
                        1 for line in lines if any(keyword in line.lower() for keyword in ['error', 'fail', 'denied']))
                    st.metric("Error/Failure Events", error_count)

                # Threat detection
                st.subheader("Threat Detection Results")
                threats = detect_log_threats(log_content)

                if threats:
                    for threat in threats:
                        severity_color = {"Critical": "red", "High": "orange", "Medium": "yellow", "Low": "green"}
                        color = severity_color.get(threat['severity'], "black")

                        st.markdown(f"<div style='padding: 10px; border-left: 4px solid {color}; margin: 5px 0;'>"
                                    f"<strong>{threat['type']}</strong> - {threat['severity']}<br>"
                                    f"{threat['description']}<br>"
                                    f"<small>Count: {threat['count']}</small></div>",
                                    unsafe_allow_html=True)
                else:
                    st.success("No obvious threats detected in the logs.")

                # Generate analysis report
                if st.button(f"Generate Report for {log_file.name}"):
                    report = generate_log_analysis_report(log_file.name, total_lines, unique_ips, error_count, threats)
                    FileHandler.create_download_link(report.encode(), f"log_analysis_{log_file.name}.txt", "text/plain")

            except Exception as e:
                st.error(f"Error analyzing {log_file.name}: {str(e)}")

    else:
        # Demo log analysis
        st.subheader("Demo Log Analysis")
        if st.button("Analyze Sample Security Logs"):
            show_progress_bar("Analyzing sample logs", 3)

            # Generate sample analysis results
            sample_results = generate_sample_log_analysis()

            st.subheader("Sample Analysis Results")
            for result in sample_results:
                st.write(f"**{result['timestamp']}** - {result['event']}: {result['description']}")


# Helper functions
def generate_secure_passwords(length, count, upper, lower, numbers, symbols,
                              exclude_ambiguous, exclude_similar, must_include_all):
    """Generate secure passwords with specified criteria"""
    chars = ""
    if lower:
        chars += string.ascii_lowercase
    if upper:
        chars += string.ascii_uppercase
    if numbers:
        chars += string.digits
    if symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if exclude_ambiguous:
        chars = chars.replace('0', '').replace('O', '').replace('l', '').replace('I', '').replace('1', '')

    if exclude_similar:
        chars = chars.replace('i', '').replace('L', '').replace('o', '')

    if not chars:
        return []

    passwords = []
    for _ in range(count):
        password = ""

        if must_include_all:
            # Ensure at least one character from each selected type
            if lower:
                password += secrets.choice(string.ascii_lowercase)
            if upper:
                password += secrets.choice(string.ascii_uppercase)
            if numbers:
                password += secrets.choice(string.digits)
            if symbols:
                password += secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")

        # Fill the rest randomly
        while len(password) < length:
            password += secrets.choice(chars)

        # Shuffle the password
        password_list = list(password)
        random.shuffle(password_list)
        passwords.append(''.join(password_list))

    return passwords


def calculate_password_strength(password):
    """Calculate password strength score"""
    score = 0

    # Length scoring
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    elif len(password) >= 6:
        score += 5

    # Character type scoring
    if any(c.islower() for c in password):
        score += 15
    if any(c.isupper() for c in password):
        score += 15
    if any(c.isdigit() for c in password):
        score += 15
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 20

    # Uniqueness scoring
    unique_chars = len(set(password))
    if unique_chars >= len(password) * 0.8:
        score += 10

    return min(score, 100)


def analyze_password_details(password):
    """Analyze password in detail"""
    analysis = {}

    analysis["Length"] = {
        "status": len(password) >= 8,
        "message": f"Password is {len(password)} characters long"
    }

    analysis["Uppercase Letters"] = {
        "status": any(c.isupper() for c in password),
        "message": "Contains uppercase letters" if any(c.isupper() for c in password) else "No uppercase letters"
    }

    analysis["Lowercase Letters"] = {
        "status": any(c.islower() for c in password),
        "message": "Contains lowercase letters" if any(c.islower() for c in password) else "No lowercase letters"
    }

    analysis["Numbers"] = {
        "status": any(c.isdigit() for c in password),
        "message": "Contains numbers" if any(c.isdigit() for c in password) else "No numbers"
    }

    analysis["Special Characters"] = {
        "status": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
        "message": "Contains special characters" if any(
            c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password) else "No special characters"
    }

    # Check for common patterns
    common_patterns = ["123", "abc", "qwerty", "password", "admin"]
    has_common = any(pattern in password.lower() for pattern in common_patterns)
    analysis["Common Patterns"] = {
        "status": not has_common,
        "message": "No common patterns detected" if not has_common else "Contains common patterns"
    }

    return analysis


def check_password_policy(password, min_length, req_upper, req_lower, req_numbers, req_symbols, max_repeat):
    """Check password against policy"""
    results = {}

    results["Minimum Length"] = {
        "status": len(password) >= min_length,
        "message": f"Password is {len(password)} characters (minimum: {min_length})"
    }

    if req_upper:
        results["Uppercase Required"] = {
            "status": any(c.isupper() for c in password),
            "message": "Contains uppercase letters" if any(
                c.isupper() for c in password) else "Missing uppercase letters"
        }

    if req_lower:
        results["Lowercase Required"] = {
            "status": any(c.islower() for c in password),
            "message": "Contains lowercase letters" if any(
                c.islower() for c in password) else "Missing lowercase letters"
        }

    if req_numbers:
        results["Numbers Required"] = {
            "status": any(c.isdigit() for c in password),
            "message": "Contains numbers" if any(c.isdigit() for c in password) else "Missing numbers"
        }

    if req_symbols:
        results["Symbols Required"] = {
            "status": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "message": "Contains symbols" if any(
                c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password) else "Missing symbols"
        }

    # Check for repeating characters
    max_consecutive = 1
    current_consecutive = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    results["Repeating Characters"] = {
        "status": max_consecutive <= max_repeat,
        "message": f"Max consecutive characters: {max_consecutive} (limit: {max_repeat})"
    }

    return results


def generate_simulated_hosts():
    """Generate simulated host discovery results"""
    hosts = []
    base_ip = "192.168.1."

    for i in range(1, random.randint(5, 15)):
        ip = f"{base_ip}{i}"
        status = random.choice(["Up", "Up", "Up", "Down"])
        response_time = random.randint(1, 100) if status == "Up" else None

        hosts.append({
            "ip": ip,
            "status": status,
            "response_time": response_time
        })

    return hosts


def generate_simulated_ports():
    """Generate simulated port scan results"""
    common_ports = [
        {"port": 22, "service": "SSH", "state": "open"},
        {"port": 80, "service": "HTTP", "state": "open"},
        {"port": 443, "service": "HTTPS", "state": "open"},
        {"port": 25, "service": "SMTP", "state": "closed"},
        {"port": 53, "service": "DNS", "state": "open"},
        {"port": 110, "service": "POP3", "state": "closed"},
        {"port": 143, "service": "IMAP", "state": "filtered"},
        {"port": 993, "service": "IMAPS", "state": "open"},
        {"port": 995, "service": "POP3S", "state": "closed"}
    ]

    return random.sample(common_ports, random.randint(3, 7))


def generate_host_discovery_report(hosts):
    """Generate host discovery report"""
    report = "HOST DISCOVERY REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Total Hosts Scanned: {len(hosts)}\n\n"

    up_hosts = [h for h in hosts if h['status'] == 'Up']
    report += f"Hosts Up: {len(up_hosts)}\n"

    for host in up_hosts:
        report += f"  {host['ip']} - Response: {host['response_time']}ms\n"

    report += f"\nHosts Down: {len(hosts) - len(up_hosts)}\n"
    return report


def generate_port_scan_report(target_ip, ports):
    """Generate port scan report"""
    report = "PORT SCAN REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Target: {target_ip}\n"
    report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for port in ports:
        report += f"Port {port['port']}: {port['state']} - {port['service']}\n"

    return report


def generate_ssl_report(hostname, port, cert, cipher, days_until_expiry):
    """Generate SSL/TLS validation report"""
    report = "SSL/TLS VALIDATION REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Hostname: {hostname}\n"
    report += f"Port: {port}\n"
    report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    report += "CERTIFICATE INFORMATION:\n"
    report += f"Subject: {cert.get('subject', 'N/A')}\n"
    report += f"Issuer: {cert.get('issuer', 'N/A')}\n"
    report += f"Valid Until: {cert.get('notAfter', 'N/A')}\n"
    report += f"Days Until Expiry: {days_until_expiry}\n\n"

    if cipher:
        report += "CIPHER INFORMATION:\n"
        report += f"Cipher: {cipher[0]}\n"
        report += f"Protocol: {cipher[1]}\n"
        report += f"Key Length: {cipher[2]} bits\n\n"

    report += "SECURITY ASSESSMENT:\n"
    if days_until_expiry > 30:
        report += "✓ Certificate validity: Good\n"
    else:
        report += "⚠ Certificate expires soon\n"

    return report


def generate_risk_recommendations(risk_type, residual_risk, controls):
    """Generate risk mitigation recommendations"""
    recommendations = []

    if residual_risk > 15:
        recommendations.append("Immediate action required - implement additional controls")
        recommendations.append("Consider risk transfer options (insurance, outsourcing)")
    elif residual_risk > 10:
        recommendations.append("Enhance existing security controls")
        recommendations.append("Implement monitoring and detection capabilities")

    if controls < 3:
        recommendations.append("Strengthen security controls implementation")
        recommendations.append("Conduct regular security assessments")

    # Risk-specific recommendations
    if "Data Breach" in risk_type:
        recommendations.extend([
            "Implement data encryption at rest and in transit",
            "Deploy data loss prevention (DLP) solutions",
            "Establish incident response procedures"
        ])
    elif "Network" in risk_type:
        recommendations.extend([
            "Deploy network segmentation",
            "Implement intrusion detection systems",
            "Regular penetration testing"
        ])

    return recommendations


def generate_detailed_risk_report(data):
    """Generate detailed risk assessment report"""
    report = "SECURITY RISK ASSESSMENT REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Assessment Date: {data['assessment_date']}\n"
    report += f"Risk Category: {data['category']}\n"
    report += f"Specific Risk: {data['risk']}\n\n"

    report += "RISK SCORING:\n"
    report += f"Likelihood: {data['likelihood']}/5\n"
    report += f"Impact: {data['impact']}/5\n"
    report += f"Current Controls: {data['controls']}/5\n"
    report += f"Raw Risk Score: {data['raw_risk']}/25\n"
    report += f"Residual Risk Score: {data['residual_risk']:.1f}/25\n\n"

    report += "RECOMMENDATIONS:\n"
    for i, rec in enumerate(data['recommendations'], 1):
        report += f"{i}. {rec}\n"

    return report


def generate_phishing_sample():
    """Generate educational phishing email sample"""
    phishing_samples = [
        {
            "content": """From: security@bankofamerica-security.com
Subject: URGENT: Your account will be suspended

Dear Customer,

We have detected suspicious activity on your account. Please verify your identity immediately by clicking the link below:

http://bankofamerica-verify.suspicious-domain.com/login

Failure to verify within 24 hours will result in account suspension.

Thank you,
Bank of America Security Team""",
            "is_phishing": True,
            "indicators": [
                "Suspicious sender domain (bankofamerica-security.com)",
                "Urgency tactics (24 hour deadline)",
                "Suspicious URL (not official bank domain)",
                "Generic greeting ('Dear Customer')",
                "Requests immediate action"
            ]
        },
        {
            "content": """From: noreply@github.com
Subject: Your security alert settings

Hi there,

This is a reminder that you have security alerts enabled for your repositories. You can manage these settings in your account preferences.

If you have any questions, please visit our help documentation.

Best regards,
GitHub Team""",
            "is_phishing": False,
            "indicators": [
                "Legitimate sender domain",
                "No urgent action requested",
                "Professional tone",
                "No suspicious links",
                "Informational content only"
            ]
        }
    ]

    return random.choice(phishing_samples)


def analyze_email_security(email_content):
    """Analyze email for security threats"""
    risk_score = 0
    findings = []

    # Check for suspicious URLs
    import re
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                      email_content)

    for url in urls:
        if any(suspicious in url.lower() for suspicious in ['bit.ly', 'tinyurl', 'secure-', 'verify-']):
            risk_score += 20
            findings.append({
                "severity": "High",
                "description": f"Suspicious URL detected: {url}"
            })

    # Check for urgency keywords
    urgency_keywords = ['urgent', 'immediate', 'expires', 'suspend', 'verify now', 'act now']
    urgency_count = sum(1 for keyword in urgency_keywords if keyword in email_content.lower())

    if urgency_count > 2:
        risk_score += 25
        findings.append({
            "severity": "Medium",
            "description": "High use of urgency tactics detected"
        })

    # Check for generic greetings
    if any(greeting in email_content.lower() for greeting in ['dear customer', 'dear user', 'dear sir/madam']):
        risk_score += 15
        findings.append({
            "severity": "Medium",
            "description": "Generic greeting suggests mass phishing attempt"
        })

    # Check for credential requests
    if any(term in email_content.lower() for term in ['password', 'username', 'login', 'verify account']):
        risk_score += 20
        findings.append({
            "severity": "High",
            "description": "Email requests sensitive credentials"
        })

    return {
        "risk_score": min(risk_score, 100),
        "findings": findings
    }


def generate_training_metrics():
    """Generate simulated training metrics"""
    return {
        "detection_rate": random.randint(70, 95),
        "false_positives": random.randint(5, 15),
        "training_completed": random.randint(80, 98),
        "improvement": random.randint(10, 25)
    }


def extract_ips_from_logs(log_content):
    """Extract IP addresses from log content"""
    import re
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(ip_pattern, log_content)


def detect_log_threats(log_content):
    """Detect potential threats in log content"""
    threats = []
    lines = log_content.split('\n')

    # Count failed login attempts
    failed_logins = sum(1 for line in lines if
                        any(term in line.lower() for term in ['failed login', 'authentication failed', 'login failed']))

    if failed_logins > 10:
        threats.append({
            "type": "Brute Force Attack",
            "severity": "High",
            "description": "Multiple failed login attempts detected",
            "count": failed_logins
        })

    # Check for SQL injection attempts
    sql_injection = sum(
        1 for line in lines if any(term in line.lower() for term in ['union select', 'drop table', '1=1', 'or 1=1']))

    if sql_injection > 0:
        threats.append({
            "type": "SQL Injection Attempt",
            "severity": "Critical",
            "description": "Potential SQL injection attacks detected",
            "count": sql_injection
        })

    # Check for unusual traffic patterns
    error_count = sum(1 for line in lines if any(term in line for term in ['404', '500', '403']))

    if error_count > len(lines) * 0.1:  # More than 10% errors
        threats.append({
            "type": "Unusual Traffic Pattern",
            "severity": "Medium",
            "description": "High error rate indicates potential scanning or attacks",
            "count": error_count
        })

    return threats


def generate_log_analysis_report(filename, total_lines, unique_ips, error_count, threats):
    """Generate log analysis report"""
    report = "LOG ANALYSIS REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"File: {filename}\n"
    report += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    report += "STATISTICS:\n"
    report += f"Total Log Entries: {total_lines}\n"
    report += f"Unique IP Addresses: {unique_ips}\n"
    report += f"Error/Failure Events: {error_count}\n\n"

    report += "THREAT DETECTION:\n"
    if threats:
        for threat in threats:
            report += f"- {threat['type']} ({threat['severity']}): {threat['description']} (Count: {threat['count']})\n"
    else:
        report += "No obvious threats detected.\n"

    return report


def generate_sample_log_analysis():
    """Generate sample log analysis results"""
    return [
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": "Failed Login Attempt",
            "description": "Multiple failed SSH login attempts from IP 192.168.1.100"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "event": "Suspicious Traffic",
            "description": "High volume of 404 errors from single IP address"
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"),
            "event": "Normal Activity",
            "description": "Standard user authentication and file access"
        }
    ]


# Additional helper functions for other tools...
def vulnerability_assessment():
    """Placeholder for vulnerability assessment tool"""
    st.info("Vulnerability Assessment tool - Coming soon!")


def web_app_testing():
    """Placeholder for web application testing tool"""
    st.info("Web Application Testing tool - Coming soon!")


def privacy_auditing():
    """Placeholder for privacy auditing tool"""
    st.info("Privacy Auditing tool - Coming soon!")


def incident_response():
    """Placeholder for incident response tool"""
    st.info("Incident Response tool - Coming soon!")


def security_training():
    """Placeholder for security training tool"""
    st.info("Security Training tool - Coming soon!")


def compliance_tracking():
    """Placeholder for compliance tracking tool"""
    st.info("Compliance Tracking tool - Coming soon!")


def threat_intelligence():
    """Placeholder for threat intelligence tool"""
    st.info("Threat Intelligence tool - Coming soon!")


def digital_signatures():
    """Placeholder for digital signatures tool"""
    st.info("Digital Signatures tool - Coming soon!")
