import curses

from .api_key import API_KEY, BASE_URL

from http_client import HttpClient
http_client = HttpClient(API_KEY, BASE_URL)

def fetch_user():
    """Fetch user details and return the user ID."""
    response = http_client.get("/user")
    return response["id"] if response else None


def fetch_workspaces():
    """Fetch all workspaces and return a list of them."""
    response = http_client.get("/workspaces")
    return response if response else []


def choose_workspace(stdscr, workspaces):
    """
    Prompt the user to choose a workspace using arrow keys (without clearing the screen).
    """
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()  # Clear the screen but not the entire terminal

    workspace_names = [ws['name'] for ws in workspaces]
    selected_index = 0  # Start with the first workspace selected

    while True:
        stdscr.clear()  # Clear the screen on each refresh

        # Print instructions for the user
        stdscr.addstr(0, 0, "Select a workspace you want to get the report on:\n", curses.A_BOLD)

        # Display available workspaces with the selected one highlighted
        for idx, name in enumerate(workspace_names):
            if idx == selected_index:
                stdscr.addstr(idx + 2, 0, f"> {name}", curses.A_REVERSE)  # Highlight selected
            else:
                stdscr.addstr(idx + 2, 0, f"  {name}")

        # Refresh the screen to show updates
        stdscr.refresh()

        key = stdscr.getch()  # Get user input

        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1  # Move up in the list
        elif key == curses.KEY_DOWN and selected_index < len(workspace_names) - 1:
            selected_index += 1  # Move down in the list
        elif key == 10:  # Enter key
            # Return the selected workspace's ID
            return workspaces[selected_index]["id"]
        elif key == 27:  # ESC key
            # Exit the program on ESC
            return None



# Fetch the user ID
USER_ID = fetch_user()

# Fetch and choose the workspace
if USER_ID:
    WORKSPACES = fetch_workspaces()
    if WORKSPACES:
        WORKSPACE_ID = curses.wrapper(choose_workspace, WORKSPACES)
        if WORKSPACE_ID:
            print(f"Selected Workspace ID: {WORKSPACE_ID}")
        else:
            print("No workspace selected. Exiting.")
    else:
        print("No workspaces available.")
else:
    print("Failed to fetch user ID.")
