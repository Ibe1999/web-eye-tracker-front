import os
import matplotlib.pyplot as plt
from github import Github

# Authenticate with GitHub API using the token
token = os.getenv('GH_PAT')

if not token:
    raise ValueError("GitHub token not found. Ensure GH_PAT is set as an environment variable.")

# Define repository name
repo_name = "Ibe1999/web-eye-tracker-front"

# Authenticate with GitHub API
g = Github(token)
try:
    user = g.get_user()
    print(f"Authenticated as: {user.login}")
except Exception as auth_error:
    raise ValueError(f"GitHub authentication failed: {auth_error}")

repo = g.get_repo(repo_name)

def count_labels(repo):
    """Count the number of issues for each label in a repository."""
    labels_count = {}
    print("Fetching issues from the repository...")
    for issue in repo.get_issues(state="all"):
        for label in issue.labels:
            labels_count[label.name] = labels_count.get(label.name, 0) + 1

    print(f"Labels count: {labels_count}")
    return labels_count

def generate_histogram(repo_name, labels_count):
    """Generate and save a histogram of issue labels."""
    if not labels_count:
        print(f"No labeled issues found in {repo_name}. Skipping histogram generation.")
        return None  

    print("Generating histogram...")

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(labels_count.keys(), labels_count.values(), color='skyblue')
    plt.ylabel('Number of Issues')
    plt.xlabel('Labels')
    plt.title(f'Histogram of Issues by Label - {repo_name}')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    # Ensure directory exists
    artifacts_dir = "artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)
    filename = os.path.join(artifacts_dir, "histogram.png")
    plt.savefig(filename)
    plt.close()

    print(f"Histogram saved as: {filename}")
    return filename

def main():
    try:
        print(f"Processing repository: {repo_name}")
        labels_count = count_labels(repo)

        if not labels_count:
            # Optional: Uncomment this to test plotting even if no labels
            # labels_count = {'example': 1, 'placeholder': 2}

            print("⚠️ No labeled issues. Nothing to plot.")
            return

        generate_histogram(repo_name, labels_count)
    except Exception as e:
        print(f"Error processing {repo_name}: {e}")

if __name__ == '__main__':
    main()
