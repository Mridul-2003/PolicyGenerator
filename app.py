from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
from fpdf import FPDF
import base64
from eng_to_arabic import EngToArabic
import asyncio
app = Flask(__name__)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Use consistent naming

# Configure the generative AI model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

@app.route("/generate_policy", methods=["POST"])
def generate_policy():
    data = request.get_json()

    # Input validation (important for security and robustness)
    required_fields = [
        "policy_name",
        "company_name",
        "location",
        "industry",
        "description",
        "company_size",
        "key_assets_company"
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    policy_name = data["policy_name"]
    company_name = data["company_name"]
    location = data["location"]
    industry = data["industry"]
    business_activities_description = data["description"]
    company_size = data["company_size"]
    key_information_assets = data["key_assets_company"]
    language = data["language"]

    prompt = f"""
You are an experienced advocate that knows about every policy globally.
Generate policy with policy name={policy_name}, company name = {company_name},
location={location}, industry={industry}, Description of your business activities = {business_activities_description},
CompanySize={company_size} and Key information assests of company = {key_information_assets} by taking following template:
Here's a comprehensive prompt template for generating Information Security policies:

"Please generate a {policy_name} policy that is fully compliant with [STANDARDS_LIST] for a {company_name} operating in {location} with approximately {company_size} employees. The policy should:

Align with:
Primary standards: [e.g., ISO27001, NIST, etc.]
Regional regulations: [e.g., CBUAE, NESA, PDPL]
Industry requirements: [e.g., FinTech, Healthcare]
Include:
Document control information
Purpose and scope
Detailed policy statements
Roles and responsibilities
Specific procedures and controls
Compliance requirements
Review and update procedures
Related documents and references
Consider:
Local business culture and practices
Industry-specific risks and controls
Company size and complexity
Technical environment
Operational requirements
Provide:
Implementation guidelines
Compliance checklists
Supporting templates
Audit requirements
Monitoring procedures
Please ensure the policy incorporates both global best practices and local regulatory requirements while remaining practical for day-to-day operations."

Example Usage: "Please generate a Remote Access Policy that is fully compliant with ISO27001 and NIST for a FinTech company operating in UAE with approximately 75 employees. [Continue with points 1-4 from above]"

Here are specialized prompts for different types of Information Security policies:

Access Control Policy Prompt:

Generate an Access Control Policy for {company_name} that includes:

- User access lifecycle management

- Privileged access requirements

- Password and authentication standards

- Remote access controls

- Third-party access management

- Access review procedures

Key focus areas:

- Role-based access control (RBAC)

- Segregation of duties

- Emergency access procedures

- Access monitoring and logging

Data Protection Policy Prompt:

Generate a Data Protection Policy for {company_name} covering:

- Data classification schema

- Data handling requirements

- Data retention periods

- Data disposal procedures

- Privacy requirements

- Cross-border data transfers

Key focus areas:

- Personal data protection

- Customer data handling

- Data minimization

- Data subject rights

Incident Response Policy Prompt:

Generate an Incident Response Policy for {company_name} including:

- Incident classification

- Response team structure

- Notification procedures

- Escalation matrix

- Recovery procedures

- Lessons learned process

Key focus areas:

- Detection capabilities

- Response timelines

- Communication plans

- Evidence handling

Change Management Policy Prompt:

Generate a Change Management Policy for {company_name} covering:

- Change request procedures

- Risk assessment requirements

- Testing requirements

- Approval workflow

- Emergency change procedures

- Post-implementation review

Key focus areas:

- Change advisory board

- Release management

- Rollback procedures

- Documentation requirements

Business Continuity Policy Prompt:

Generate a Business Continuity Policy for {company_name} including:

- BIA requirements

- Recovery time objectives

- Recovery point objectives

- Testing requirements

- Communication procedures

- Activation triggers

Key focus areas:

- Critical function identification

- Recovery strategies

- Regular testing requirements

- Vendor dependencies

Acceptable Use Policy Prompt:

Generate an Acceptable Use Policy for {company_name} covering:

- Device usage rules

- Internet usage guidelines

- Email usage requirements

- Social media guidelines

- Software installation rules

- Personal use limitations

Key focus areas:

- User responsibilities

- Prohibited activities

- Monitoring notice

- Enforcement measures

Mobile Device Policy Prompt:

Generate a Mobile Device Policy for {company_name} including:

- Device enrollment procedures

- Security requirements

- App management

- Data protection

- Remote wipe capabilities

- BYOD requirements

Key focus areas:

- Device encryption

- Authentication requirements

- Lost device procedures

- App whitelisting/blacklisting

Third-Party Risk Management Policy Prompt:

Generate a Third-Party Risk Management Policy for {company_name} covering:

- Vendor assessment procedures

- Due diligence requirements

- Ongoing monitoring

- Performance metrics

- Exit procedures

- Contract requirements

Key focus areas:

- Risk assessment framework

- Security requirements

- Compliance monitoring

- Service level agreements

For each policy type, remember to include:

Regulatory requirements specific to {location}
Industry standards for {industry}
Company size considerations
Implementation guidelines
Supporting templates
Audit requirements

Example output:

Test Company

Information Security Policy

Field Information
Version Number [Version Number, e.g.,]
Effective Date [Date, e.g., ]
Review Date [Date, e.g., ]
Document Owner [Owner&#39;s Name, e.g., John Doe]
Approved By [Approver&#39;s Name, e.g., Jane Smith]
Document Reference Number [Unique Identifier, e.g., ISP-001]
Associated Documents [Related Policies, Standards, etc.]
Revision History [Changes made &amp; their dates]
Audience [e.g., All Employees, IT Department]

1 - Purpose
The purpose of this Information Security Policy is to establish a comprehensive framework for
managing and protecting the information assets of Test Company.
This policy aims to safeguard the confidentiality, integrity, and availability of all information
handled by the company, ensuring compliance with relevant legal, regulatory, and contractual
obligations.
By implementing this policy, Test Company seeks to mitigate risks associated with information
security threats and vulnerabilities, thereby maintaining the trust of our clients, partners, and
employees.
2 - Scope
2.1. Departments

Information Security Policy Internal Document 2
This policy applies to all departments within Test Company, including Administration, Software
Development, QA Testing, Customer Support, and Sales &amp; Marketing.
2.2. Types of Data
The policy covers all types of data handled by the company, including Customer Personal
Identifiable Information (PII), Employee Records, Financial Data, Project Specifications, Source
Code, and Testing Data.
2.3. Key Information Assets
The scope of this policy extends to all key information assets, including the Customer Database,
Employee Records, Financial System, Project Management Software, Source Code Repository,
Office Network Infrastructure, Mobile and Web Applications, Company Website, and Internal
Documentation.
3 - Information Security Objectives
Test Company is committed to achieving the following information security objectives:
- Protecting the confidentiality of customer and employee information by implementing robust
access control measures.
- Ensuring the integrity of our software solutions and data through rigorous testing and validation
processes.
- Maintaining the availability of our information systems and services to support business
operations and customer needs.
- Complying with GDPR and HIPAA regulations to safeguard personal and health information.
- Continuously improving our information security management system through regular reviews
and updates.
4 - Data Classification
Test Company classifies data to ensure appropriate levels of protection and handling.
Data is categorized into the following classes:
- Public: Information intended for public disclosure, such as marketing materials and press
releases.

Information Security Policy Internal Document 3
- Internal: Information that is not intended for public disclosure but is accessible within the
company, such as internal memos and guidelines.
- Confidential: Sensitive information requiring restricted access, such as Customer PII,
Employee Records, and Financial Data.
- Restricted: Highly sensitive information with the strictest access controls, including Source
Code and Project Specifications.
Each data class is subject to specific handling, storage, and transmission requirements to
ensure its protection.
5 - Roles and Responsibilities
The Chief Information Security Officer (CISO), John Doe, is responsible for overseeing the
development, implementation, and maintenance of the Information Security Management
System (ISMS) at Test Company.
He ensures compliance with relevant legal, regulatory, and contractual requirements, including
GDPR and HIPAA.
The Administration Department is tasked with managing access rights and ensuring that all
employees are aware of their information security responsibilities.
They coordinate with the CISO to implement security policies and procedures.
The Software Development Department is responsible for incorporating security best practices
into the design, development, and maintenance of all software solutions.
They must ensure that source code and project specifications are protected against
unauthorized access and modifications.
The QA Testing Department must ensure that all testing data is handled securely and that
vulnerabilities identified during testing are reported and addressed promptly.
Customer Support is responsible for safeguarding customer PII during interactions and ensuring
that any data shared is protected according to company policies.
Sales &amp; Marketing must ensure that any customer or prospect data collected is handled in
compliance with GDPR and other relevant regulations.
All employees are responsible for adhering to the information security policies and procedures
and reporting any security incidents or vulnerabilities to the CISO or designated security
personnel.

Information Security Policy Internal Document 4
6 - Access Control
Access to Test Company&#39;s systems and data is restricted to authorized personnel only and is
granted based on the principle of least privilege.
Employees must use company-issued devices to access systems, ensuring that these devices
are secured and updated regularly.
Two-factor authentication is mandatory for accessing all systems to enhance security.
When accessing company systems from outside the office, employees are required to use a
Virtual Private Network (VPN) to ensure secure communication.
Access rights are reviewed regularly by the Administration Department in coordination with the
CISO to ensure that they remain appropriate and reflect any changes in roles or responsibilities.
Access to sensitive data, such as Customer PII, Employee Records, and Financial Data, is
further restricted to individuals who require it to perform their job functions.
Any changes to access rights must be documented and approved by the CISO or designated
personnel.
Employees are required to log out of systems when not in use and report any unauthorized
access attempts immediately.
The company employs monitoring tools to detect and respond to unauthorized access attempts
or anomalies in system usage.
7 - Security Measures
Test Company is committed to implementing robust security measures to protect its information
assets and ensure compliance with applicable legal and regulatory requirements.
Our security measures are designed to safeguard the confidentiality, integrity, and availability of
information across all departments and operations.
Physical security at our primary location is maintained through a card-based access control
system.
Security cameras are strategically installed at all entrances and exits to monitor and record
activities.

Information Security Policy Internal Document 5
Visitors are required to sign in upon arrival and are escorted by authorized personnel throughout
their visit to ensure security and accountability.
Our change management process ensures that all system changes are systematically tracked
through a dedicated Change Management System.
Before implementation, changes must receive approval from the Chief Information Security
Officer (CISO) to ensure alignment with security policies and objectives.
All changes undergo rigorous testing in a separate environment to identify and mitigate potential
risks before deployment.
To secure information during transmission, we employ encryption protocols such as SSL/TLS
for all data in transit.
Our email system is fortified with secure email gateways to protect both outbound and inbound
traffic from unauthorized access and threats.
In the event of a security incident, we adhere to a predefined Incident Response Plan.
This plan includes logging and investigating all incidents thoroughly, with lessons learned being
integrated into our security procedures to prevent recurrence.
Our Business Continuity Plan is designed to ensure the resilience of our operations.
It includes regular data backups, a disaster recovery site, and clearly defined roles and
responsibilities for the management team to ensure swift and effective response during
disruptions.
Test Company complies with GDPR and HIPAA regulations, reflecting our commitment to
protecting personal data and health information.
These security measures are continuously reviewed and updated to address emerging threats
and maintain compliance with evolving standards and regulations.
8 - Training and Awareness
Test Company is committed to fostering a culture of information security awareness among all
employees.
To achieve this, we will provide regular training sessions designed to educate staff on the
importance of information security and their roles in maintaining it.

Information Security Policy Internal Document 6
These sessions will cover key topics such as data protection, secure handling of customer PII,
GDPR and HIPAA compliance, and the use of company-issued devices.
Employees will also receive training on the implementation of two-factor authentication and the
correct usage of VPNs for secure remote access.
The training program will be mandatory for all new hires during their onboarding process and
will be refreshed annually for all staff to ensure ongoing awareness and compliance.
The Chief Information Security Officer, John Doe, will oversee the development and delivery of
these training programs, ensuring they are up-to-date with the latest security practices and
regulatory requirements.
Feedback from training sessions will be collected to continuously improve the program and
address any identified gaps in knowledge or practice.
9 - Policy Compliance
Compliance with the Information Security Policy is mandatory for all employees, contractors,
and third-party partners of Test Company.
Failure to comply with the policy may result in disciplinary action, up to and including termination
of employment or contract.
Regular audits and assessments will be conducted to ensure adherence to the policy and
identify any areas of non-compliance.
Employees are encouraged to report any suspected breaches of policy or security incidents to
their supervisor or directly to the Chief Information Security Officer.
Test Company will ensure that all employees are aware of the consequences of non-compliance
and the importance of maintaining the integrity and confidentiality of the data we handle.
10 - Review and Updates
The Information Security Policy will be reviewed at least annually to ensure its continued
relevance and effectiveness in addressing the evolving security landscape.
The review process will be led by the Chief Information Security Officer, with input from relevant
departments such as Software Development, QA Testing, and Customer Support.
Updates to the policy will be made as necessary to reflect changes in legal, regulatory, or
contractual requirements, as well as advancements in technology or changes in the company&#39;s
operational environment.

Information Security Policy Internal Document 7
Any revisions to the policy will be communicated to all employees, and additional training will be
provided if significant changes are made.
Test Company is committed to maintaining a robust information security framework that
supports our business objectives and protects the data entrusted to us by our clients and
partners.
11 - Definitions
Confidentiality: The principle of preventing unauthorized access to information. It ensures that
information is accessible only to those authorized to have access.
Integrity: The assurance that information is trustworthy and accurate. It refers to protecting data
from being altered or tampered with by unauthorized individuals.
Availability: The guarantee that authorized users have access to information and associated
assets when required.
Personal Identifiable Information (PII): Any data that can be used to identify a specific
individual, including names, addresses, phone numbers, and social security numbers.
Protected Health Information (PHI): Any information about health status, provision of health
care, or payment for health care that can be linked to an individual.
Risk Assessment: The process of identifying, evaluating, and analyzing risks associated with
organizational operations, particularly in terms of information security.
Change Management: The systematic approach to dealing with changes, both from the
perspective of an organization and on the individual level.
Incident Management: The process of identifying, managing, and analyzing security breaches
or attacks to prevent future occurrences.
Business Continuity Plan (BCP): A plan that outlines procedures and instructions an
organization must follow in the face of disaster, in order to continue its daily operations.
Two-Factor Authentication (2FA): A security process in which users provide two different
authentication factors to verify themselves.
Virtual Private Network (VPN): A technology that creates a safe and encrypted connection
over a less secure network, such as the internet.
SSL/TLS (Secure Sockets Layer/Transport Layer Security): Protocols for establishing
authenticated and encrypted links between networked computers.

dont write anything like for eg Okay, here's the Data Privacy Policy 
for Example Corp, formatted to match the example output: and just give output like example output and dont make innecessary
tables.
"""

    try:
        # Generate content using the prompt
        response = model.generate_content(prompt)
        print(response.text)
        generated_policy=response.text
        if language == "arabic":
            async def main(policy):
                engtoarabic = EngToArabic()
                return await engtoarabic.translate(policy)
            generated_policy = asyncio.run(main(generated_policy))


        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        try:
            pdf.add_font('Arial Unicode MS', '', 'ARIALUNI.TTF', uni=True)
            pdf.set_font('Arial Unicode MS', size=12)
        except IOError:
            print("Arial Unicode MS font not found. Falling back to default font which may result in character encoding issues.")
            pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, generated_policy)
        pdf_filename = f"{policy_name}.pdf"
        # pdf.output(pdf_filename)
        pdf.output("temp.pdf")

        with open("temp.pdf", "rb") as pdf_file:
            encoded_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")

        os.remove("temp.pdf") #Remove the temporary file

        return jsonify({"generated_policy": generated_policy, "pdf": encoded_pdf})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host=" 0.0.0.0", port=8000,debug=True)
