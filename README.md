## **HR-ASSIST Agentic AI System**
---

**HR-ASSIST** is an Agentic AI-powered system that automates core HR workflows, designed to streamline and modernize human resource operations—starting with employee onboarding. Built on the FastMCP agent framework, this system enables autonomous task completion by integrating domain-specific tools such as employee management, leave tracking, ticketing, and meeting scheduling.

This project showcases a fully modular, extensible MCP server that works seamlessly with the Claude Desktop MCP client to automate HR operations with natural language prompts and custom tools.

---

### ⚙️ **Technical Architecture**

The MCP server—`atliq-hr-assist`—includes:
- Tool interfaces for adding employees, applying leave, managing tickets, scheduling meetings, and sending emails.
- Prompt orchestration for higher-level agent behavior, such as onboarding.
- Integration-ready setup for Claude Desktop as the client.

> The Claude Desktop UI facilitates interaction, while the MCP server handles logic, data flow, and execution through defined tools.

---

### 🛠️ **Setup Instructions**

1. **Update your `claude_desktop_config.json`:**
   
   ```json
   {
     "mcpServers": {
       "hr-assist": {
         "command": "C:\\Users\\senro\\.local\\bin\\uv",
         "args": [
           "--directory",
           "C::\\code\\atliq-hr-assist",
           "run",
           "server.py"
         ],
         "env": {
           "EMAIL": "YOUR_EMAIL",
           "EMAIL_PWD": "YOUR_APP_PASSWORD"
         }
       }
     }
   }
   ```

   - Replace `YOUR_EMAIL` with your actual email.
   - Replace `YOUR_APP_PASSWORD` with your email provider’s app-specific password (e.g., for Gmail).

2. **Install and initialize the environment:**
   ```bash
   uv init
   uv add mcp[cli]
   ```

---

### 🚀 **Features & Usage**

Once configured, you can start using HR-ASSIST through Claude Desktop:

#### ➕ **Add a New Employee**
- Use the "Add from hr-assist" option.
- Enter employee details in the prompt UI.

<img src="Resources\onboard-employee.png" alt="Claude desktop prompt with fields" style="width:auto;height:300px;padding-left:30px">

#### 📅 **Schedule Introductory Meetings**
- Automate calendar scheduling between employee and manager.

<img src="Resources\img-email.png" alt="Claude desktop scheduling meeting with employee and manager" style="width:auto;height:300px;padding-left:30px">

#### 📧 **Email Notification Automation**
- Automatically send onboarding emails from manager to employee.

<img src="Resources\img-sent-email.png" alt="Sent email to employee" style="width:auto;height:auto;padding-left:30px">

#### 🧠 **Onboarding Prompt in Action**
The `onboard_new_employee` prompt automates:
- Employee creation in HRMS
- Welcome email generation
- Ticket generation for IT resources
- Meeting scheduling with manager

Example:
```text
Onboard a new employee with the following details:
- Name: Jane Doe
- Manager Name: John Smith
```

---

### 🧩 **Tool Capabilities Overview**

| Tool | Description |
|------|-------------|
| `add_employee` | Adds a new employee to the system |
| `get_employee_details` | Fetches employee and manager ID |
| `send_email` | Sends welcome emails or notifications |
| `create_ticket` / `list_tickets` / `update_ticket_status` | Manages equipment and onboarding support tickets |
| `schedule_meeting` / `cancel_meeting` / `get_meetings` | Automates meeting coordination |
| `apply_leave` / `get_leave_balance` / `get_leave_history` | Enables leave tracking and history |
