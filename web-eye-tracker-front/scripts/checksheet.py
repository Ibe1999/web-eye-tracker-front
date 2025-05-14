import os
import requests
from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")  # This env var is set by GitHub Actions

# If not running in Actions, allow fallback for local development
if not GITHUB_REPOSITORY:
    GITHUB_REPOSITORY = "usuario/repositorio"  # Only used if not running in GitHub Actions
    print("Warning: GITHUB_REPOSITORY not found. Using default value for local development.")

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"

# Headers for GitHub API
headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"
    headers["Accept"] = "application/vnd.github.v4+json"
else:
    # We can still make some unauthenticated requests, with lower rate limits
    headers["Accept"] = "application/vnd.github.v4+json"
    print("Warning: No GITHUB_TOKEN provided. Using unauthenticated requests (limited rate).")

def create_devops_labels():
    """Create default DevOps labels if they don't exist"""
    default_labels = [
        {"name": "Plan", "color": "0052cc", "description": "Planning phase tasks"},
        {"name": "Code", "color": "006b75", "description": "Coding phase tasks"},
        {"name": "Build", "color": "ff9f1c", "description": "Build phase tasks"},
        {"name": "Test", "color": "e99695", "description": "Testing phase tasks"},
        {"name": "Release", "color": "bfd4f2", "description": "Release phase tasks"},
        {"name": "Deploy", "color": "7057ff", "description": "Deployment phase tasks"},
        {"name": "Operate", "color": "008672", "description": "Operation phase tasks"},
        {"name": "Monitor", "color": "d73a4a", "description": "Monitoring phase tasks"},
    ]

    for label in default_labels:
        try:
            response = requests.post(
                f"{GITHUB_API_URL}/labels",
                headers=headers,
                json=label
            )
            if response.status_code == 201:
                print(f"Label '{label['name']}' created successfully.")
            elif response.status_code == 422:
                print(f"Label '{label['name']}' already exists.")
            else:
                print(f"Failed to create label '{label['name']}'. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error creating label '{label['name']}': {e}")

def get_devops_phases():
    """Get DevOps phases from GitHub labels"""
    try:
        response = requests.get(f"{GITHUB_API_URL}/labels", headers=headers)
        response.raise_for_status()

        # Filter only DevOps-related labels
        all_labels = response.json()
        devops_labels = [label["name"] for label in all_labels if label["name"] in [
            "Plan", "Code", "Build", "Test", "Release", "Deploy", "Operate", "Monitor"
        ]] 

        # If no specific DevOps labels, use default set
        if not devops_labels:
            devops_labels = [
                "Plan", "Code", "Build", "Test",
                "Release", "Deploy", "Operate", "Monitor"
            ]

        return devops_labels
    except Exception as e:
        print(f"Error fetching GitHub labels: {e}")
        return [
            "Plan", "Code", "Build", "Test",
            "Release", "Deploy", "Operate", "Monitor"
        ]

def get_completed_issues_by_week(phase, start_date, end_date):
    """Get completed issues for a phase in date range"""
    try:
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        query = f"repo:{GITHUB_REPOSITORY} label:\"{phase}\" closed:{start_date_str}..{end_date_str}"
        response = requests.get(
            "https://api.github.com/search/issues",
            headers=headers,
            params={"q": query}
        )
        response.raise_for_status()

        return response.json()["total_count"]
    except Exception as e:
        print(f"Error fetching issues for {phase}: {e}")
        return 0

def generate_month_checklist(year, month):
    """Generate checklist data for a specific month"""
    devops_phases = get_devops_phases()

    first_day = datetime(year, month, 1)
    _, last_day_num = calendar.monthrange(year, month)
    last_day = datetime(year, month, last_day_num)

    month_name = first_day.strftime('%B_%Y')

    days_in_month = (last_day - first_day).days + 1
    days_per_week = days_in_month // 4

    weeks = []
    for i in range(4):
        start = first_day + timedelta(days=(i * days_per_week))
        end = first_day + timedelta(days=((i + 1) * days_per_week) - 1)
        if i == 3:
            end = last_day
        weeks.append((start, end))

    checklist_data = {
        "month": datetime(year, month, 1).strftime('%B %Y'),
        "phases": {}
    }

    for phase in devops_phases:
        phase_data = {
            "week1": {
                "completed": False,
                "issues_count": get_completed_issues_by_week(phase, weeks[0][0], weeks[0][1])
            },
            "week2": {
                "completed": False,
                "issues_count": get_completed_issues_by_week(phase, weeks[1][0], weeks[1][1])
            },
            "week3": {
                "completed": False,
                "issues_count": get_completed_issues_by_week(phase, weeks[2][0], weeks[2][1])
            },
            "week4": {
                "completed": False,
                "issues_count": get_completed_issues_by_week(phase, weeks[3][0], weeks[3][1])
            }
        }

        total_issues = sum([phase_data[f"week{i + 1}"]["issues_count"] for i in range(4)])
        phase_data["total_issues"] = total_issues

        checklist_data["phases"][phase] = phase_data

    return checklist_data, month_name

def generate_check_sheet_png(checklist_data, month_name):
    """Generate PNG visualization of the check sheet data as a table with checkboxes"""
    # Create the artifacts directory if it doesn't exist
    os.makedirs("artifacts", exist_ok=True)

    # Define output path inside the artifacts directory
    output_path = f"artifacts/checksheet_{month_name}.png"

    # Create a pandas DataFrame for visualization
    data = []
    for phase, phase_data in checklist_data["phases"].items():
        row = {
            'Phase': phase,
            'Week 1': phase_data['week1']['issues_count'],
            'Week 2': phase_data['week2']['issues_count'],
            'Week 3': phase_data['week3']['issues_count'],
            'Week 4': phase_data['week4']['issues_count'],
            'Total': phase_data['total_issues']
        }
        data.append(row)

    df = pd.DataFrame(data)

    # Set up the figure with appropriate size
    plt.figure(figsize=(10, 6))

    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Create table
    cell_text = []
    for _, row in df.iterrows():
        cell_row = []
        for col in ['Phase', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Total']:
            if col == 'Phase':
                cell_row.append(row[col])
            elif col == 'Total':
                cell_row.append(str(row[col]))
            else:
                count = row[col]
                cell_row.append(f"{count}")
        cell_text.append(cell_row)

    # Table colors
    colors = []
    for i in range(len(df)):
        row_colors = ['#f8f9fa']
        for week in ['Week 1', 'Week 2', 'Week 3', 'Week 4']:
            row_colors.append('#ffffff')
        row_colors.append('#f2f2f2')
        colors.append(row_colors)

    table = ax.table(
        cellText=cell_text,
        colLabels=['Phase', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Total Issues'],
        loc='center',
        cellLoc='center',
        cellColours=colors
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    # Set title
    plt.title(f'DevOps Check Sheet - {checklist_data["month"]}', fontsize=16, pad=20)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')

    print(f"Check sheet visualization generated: {output_path}")

def main():
    now = datetime.now()
    year = now.year
    month = now.month

    # Create DevOps labels if they don't exist
    create_devops_labels()

    # Generate checklist data
    checklist_data, month_name = generate_month_checklist(year, month)

    # Generate PNG visualization
    generate_check_sheet_png(checklist_data, month_name)

    print("Check sheet generation complete")

if __name__ == "__main__":
    if not GITHUB_TOKEN and not os.environ.get("GITHUB_ACTIONS"):
        print("Warning: GITHUB_TOKEN not set. Some functionality will be limited.")
        print("For full functionality: export GITHUB_TOKEN=ghp_abc123...")

    main()
