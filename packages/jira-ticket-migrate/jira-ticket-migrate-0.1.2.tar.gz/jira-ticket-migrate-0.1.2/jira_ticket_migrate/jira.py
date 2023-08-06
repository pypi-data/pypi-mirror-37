"""Contains Jira related functionality."""

from typing import List
from jira import JIRA as Jira


class JiraTicket:
    """Representation of a Jira project.

    Attributes:
        description (str): The description of the ticket.
        priority (str): The priority of the ticket. For example, "Medium".
        project (str): The name of the project.
        resolution (str): A string, or None, containing the resolution
            of the ticket (should there be one).
        source_link (str): The URL of the ticket on the source Jira
            server.
        summary (str): The summary of the ticket.
    """

    def __init__(
        self,
        description: str,
        priority: str,
        project: str,
        resolution: str,
        source_link: str,
        summary: str,
    ):
        """Initialize a Jira ticket.

        Args:
            description: The description of the ticket.
            priority: The priority of the ticket. For example, "Medium".
            project: The name of the project.
            resolution: A string, or None, containing the resolution of
                the ticket (should there be one).
            source_link: The URL of the ticket on the source Jira
                server.
            summary: The summary of the ticket.
        """
        self.description = description
        self.priority = priority
        self.project = project
        self.resolution = resolution
        self.source_link = source_link
        self.summary = summary


def create_blank_ticket(project: str) -> JiraTicket:
    """Create a representation of a blank Jira ticket.

    It's not actually blank, but the point it that is contains nothing
    useful.

    Args:
        project: The name of the project.

    Returns:
        A "blank" JiraTicket.
    """
    return JiraTicket(
        description="",
        priority="Medium",
        project=project,
        resolution="Done",
        source_link="null",
        summary="Blank ticket",
    )


def translate_priority(priority: str) -> str:
    """Translate to new Jira priority types.

    Jira changed how their priority names, so some translation is
    necessary if migrating from an older Jira.

    Args:
        priority: A ticket priority.

    Returns:
        A valid Jira priority.
    """
    if priority in ("Blocker", "Critical"):
        return "Highest"
    elif priority == "Major":
        return "High"
    elif priority == "Critical":
        return "High"
    elif priority == "Minor":
        return "Low"
    elif priority == "Trivial":
        return "Lowest"

    return priority


def get_project_tickets(
    jira: Jira,
    project: str,
    insert_blank_tickets: bool = True,
    verbose: bool = True,
) -> List[JiraTicket]:
    """Get all tickets from a project in ascending order.

    This will fill in missing tickets with blank tickets if
    insert_blank_tickets is set to True.

    Args:
        jira: The Jira server to get tickets from.
        project: The project name.
        insert_blank_tickets (optional): If an intermediate ticket is
            not defined, fill in a blank ticket in its place. For
            example, if the project name is PROJ and PROJ-1 and PROJ-3
            exist on the Jira but not PROJ-2, this will fill a blank
            ticket for PROJ-2.  Defaults to True.
        verbose (optional): Whether to log the tickets being processed. Defaults to True.

    Returns:
        A list of JiraTickets from ticket number 1 to ticket N, where N
        is the last ticket number.
    """
    # Offsets for the API
    init = 0
    size = 100

    # Store all the API tickets to sort through later. Keys for this are
    # ticket number. Values are the ticket object we get from the Jira
    # SDK/API library.
    api_tickets_dict = {}

    # Fetch from the API until there's no tickets left
    while True:
        start = init * size

        api_tickets = jira.search_issues("project = %s" % project, start, size)

        # Check if we've reached the end
        if not api_tickets:
            break

        # Add the tickets
        for ticket in api_tickets:
            ticket_num = int(ticket.key.split("-")[-1])
            api_tickets_dict[ticket_num] = ticket

        # Move to next API page for next round
        init += 1

    # Keep track of what a ticket "should" be if we're inserting blank
    # tickets
    ticket_counter = 1

    # Store JiraTicket objects for our tickets in here
    tickets = []

    # Create JiraTicket objects from the tickets collected above
    for ticket_num, ticket in sorted(api_tickets_dict.items()):
        if verbose:
            print("...loading %s" % ticket.key)

        # Insert blank tickets as necessary
        while insert_blank_tickets and ticket_counter < ticket_num:
            tickets.append(create_blank_ticket(project))

            ticket_counter += 1

        ticket_counter += 1

        # Insert *this* ticket. First deal with attributes that we
        # have to be careful with Nones with. Then make the ticket.
        description = ticket.fields.description

        if description is None:
            description = ""

        resolution = ticket.fields.resolution

        if resolution is not None:
            resolution = resolution.name

        tickets.append(
            JiraTicket(
                description=description,
                priority=translate_priority(ticket.fields.priority.name),
                project=project,
                resolution=resolution,
                source_link=ticket.permalink(),
                summary=ticket.fields.summary,
            )
        )

    return tickets


def add_source_link_to_description(description: str, link: str) -> str:
    """Add the source ticket URL to the description.

    Args:
        description: The original ticket's description.
        link: The URL to the source ticket.

    Returns:
        The modified description for the ticket.
    """
    link_message = "<This ticket was migrated from %s>" % link

    if description:
        link_message += "\r\n\r\n"

    return link_message + description


def push_ticket(jira: Jira, ticket: JiraTicket):
    """Push a JiraTicket to a Jira server.

    Args:
        jira: The Jira server to get tickets from.
        ticket: The ticket to push to the Jira server.
    """
    # Create the ticket
    ticket_fields = {
        "description": add_source_link_to_description(
            ticket.description, ticket.source_link
        ),
        "issuetype": {"name": "Task"},
        "priority": {"name": ticket.priority},
        "project": {"id": jira.project(ticket.project).id},
        "summary": ticket.summary,
    }

    new_ticket = jira.create_issue(fields=ticket_fields)

    # Transition the ticket
    if ticket.resolution is not None:
        # List available transitions and search for the one we want (if
        # it exists)
        transitions = jira.transitions(new_ticket)

        id_ = None

        for transition in transitions:
            if transition["name"] == ticket.resolution:
                # Found it
                id_ = transition["id"]
                break

        # Transition not available. That's okay.
        if id_ is None:
            return

        jira.transition_issue(new_ticket, id_)
