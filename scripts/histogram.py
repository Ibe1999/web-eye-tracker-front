
import os
import matplotlib.pyplot as plt
from github import Github

def count_labels(repo):
    """Count the number of issues for each label in a repository."""
    labels_count = {}
    print("Fetching issues from the repository...")
    
    # Get all issues (both open and closed)
    for issue in repo.get_issues(state="all"):
        for label in issue.labels:
            labels_count[label.name] = labels_count.get(label.name, 0) + 1
    
    print(f"Found {len(labels_count)} unique labels")
    return labels_count

def generate_histogram(repo_name, labels_count):
    """Generate and save a histogram of issue labels."""
    if not labels_count:
        print(f"No labeled issues found in {repo_name}")
        return None

    print("Generating histogram...")
    
    # Sort labels by count for better visualization
    sorted_labels = sorted(labels_count.items(), key=lambda x: x[1], reverse=True)
    labels, counts = zip(*sorted_labels)

    # Create figure with appropriate size
    plt.figure(figsize=(max(10, len(labels) * 0.5), 8)  # Dynamic width
    
    bars = plt.bar(labels, counts, color='#2ca02c')  # Green color
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    plt.ylabel('Number of Issues')
    plt.xlabel('Labels')
    plt.title(f'Issue Label Distribution - {repo_name}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save to existing artifacts directory
    filename = "artifacts/label_histogram.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Histogram saved to {filename}")
    return filename

def main():
    # Authenticate with GitHub API using GH_PATH token
    token = os.getenv('GH_PATH')  # Changed from GH_PAT to GH_PATH
    if not token:
        raise ValueError("GitHub token not found. Set GH_PATH environment variable.")
    
    repo_name = "Ibe1999/web-eye-tracker-front"
    
    try:
        g = Github(token)
        user = g.get_user()
        print(f"Authenticated as: {user.login}")
        
        repo = g.get_repo(repo_name)
        print(f"Processing repository: {repo_name}")
        
        labels_count = count_labels(repo)
        
        if labels_count:
            generate_histogram(repo_name, labels_count)
        else:
            print("No labeled issues found - nothing to plot")
            
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == '__main__':
    main()
