from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional

from emails import EmailSender
from hrms import *
from utils import seed_services
import os
from dotenv import load_dotenv

_ = load_dotenv()

email_sender = EmailSender(
    smtp_server="smtp.gmail.com",
    port=587,
    username=os.getenv("GOOGLE_EMAIL"),
    password=os.getenv("GOOGLE_EMAIL_PWD"),
    use_tls=True
)

mcp = FastMCP("atliq-hr-assist")

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
ticket_manager = TicketManager()
meeting_manager = MeetingManager()

seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

# MCP Server has - tools, resources (knowledge), prompts

@mcp.tool()
def add_employee(emp_name: str, manager_id: str, email: str) -> str:
    """
    Adds an employee to the HRMS database.
    :param emp_name: Employee name
    :param manager_id: Manager ID (optional)
    :param email: Email (optional)
    :return: Confirmation message
    """
    emp = EmployeeCreate(
        emp_id = employee_manager.get_next_emp_id(),
        name = emp_name,
        manager_id = manager_id,
        email = email
    )
    employee_manager.add_employee(emp)
    return f"Employee {emp_name} added successfully"

@mcp.tool()
def get_employee_details(name: str) -> Dict[str, str]:
    """
    Get employee details by name.
    :param name: Name of the Employee
    :return: Employee ID and Manager ID
    """
    matches = employee_manager.search_employee_by_name(name)
    if len(matches) == 0:
        raise ValueError(f"Employee {name} not found")

    emp_id = matches[0]
    return employee_manager.get_employee_details(emp_id)

@mcp.tool()
def send_email(subject: str, body: str, to_emails: List[str]):
    """
    Send Email to the new employee.
    :param subject: Subject line of the email
    :param body: Body of the email
    :param to_emails: To the new employees
    :return: Confirmation message
    """
    email_sender.send_email(
        subject = subject,
        body = body,
        to_emails = to_emails,
        from_email = email_sender.username
    )
    return "Email sent successfully."

@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> str:
    """
    Update the status of a ticket.
    :param ticket_id: Ticket ID
    :param status: New status of the ticket
    :return: Confirmation message
    """
    ticket_status_update = TicketStatusUpdate(status = status)
    return ticket_manager.update_ticket_status(ticket_status_update, ticket_id)

@mcp.tool()
def list_tickets(employee_id: str, status: str) -> List[Dict[str, str]]:
    """
    List tickets for an employee with optional status filter.
    :param employee_id: Employee ID
    :param status: Ticket status (optional)
    :return: List of tickets
    """
    return ticket_manager.list_tickets(employee_id = employee_id, status = status)

@mcp.tool()
def create_ticket(emp_id: str, item:str, reason:str) -> str:
    """
    Creates a new ticket for an employee.
    :param emp_id: Employee ID
    :param item: Item for the ticket (Laptop, ID etc.)
    :param reason: Reason for the ticket (optional)
    :return: Creates ticket
    """
    ticket_req = TicketCreate(
        emp_id = emp_id,
        item = item,
        reason = reason
    )
    return ticket_manager.create_ticket(ticket_req)

@mcp.tool()
def schedule_meeting(emp_id: str, meeting_dt: datetime, topic: str) -> str:
    """
    Schedule an introductory meeting for employee and manager.
    :param emp_id: Employee ID
    :param meeting_dt: Date and time of the meeting in python datetime format
    :param topic: Topic of the meeting
    :return: Schedule meeting
    """
    create_meeting = MeetingCreate(
        emp_id = emp_id,
        meeting_dt = meeting_dt,
        topic = topic
    )
    return meeting_manager.schedule_meeting(create_meeting)

@mcp.tool()
def get_meetings(emp_id: str) -> List[Dict[str, str]]:
    """
    Get the list of meetings scheduled for an employee.
    :param emp_id: Employee ID
    :return: List of meetings
    """
    return meeting_manager.get_meetings(emp_id)

@mcp.tool()
def cancel_meeting(emp_id: str, meeting_dt: datetime, topic) -> str:
    """
    Cancel a meeting scheduled for employee and manager.
    :param emp_id: Employee ID
    :param meeting_dt: Schedule date and time of the meeting in python datetime format
    :param topic: Topic of the meeting
    :return: Cancels the scheduled meeting
    """


@mcp.tool()
def apply_leave(emp_id: str, leave_dates: List) -> str:
    """
    Apply leaves for the employee.
    :param emp_id: Employee ID
    :param leave_dates: Begin and end dates of the leaves
    :return: Apply leaves
    """
    leave = LeaveApplyRequest(
        emp_id = emp_id,
        leave_dates = leave_dates
    )
    return leave_manager.apply_leave(leave)

@mcp.tool()
def get_leave_balance(emp_id: str) -> str:
    """
    Get the number of leaves remaining for the employee.
    :param emp_id: Employee ID
    :return: Leaves remaining for the employee
    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def get_leave_history(emp_id: str) -> str:
    """
    Get the leave history of an employee.
    :param emp_id: Employee ID
    :return: Leave history taken by employee
    """
    return leave_manager.get_leave_history(emp_id)

@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str):
    return f"""
    Onboard a new employee with the following details:
    - Name: {employee_name}
    - Manager Name: {manager_name}
    Steps to follow:
    - Add the employee to the HRMS system.
    - Send a welcome email to the employee with their login credentials. (Format: employee_name@atliq.com)
    - Notify the manager about the new employee's onboarding.
    - Raise tickets for a new laptop, id card, and other necessary equipments.
    - Schedule an introductory meeting between Employee and Manager.
    """

if __name__ == "__main__":
    mcp.run(transport='stdio')