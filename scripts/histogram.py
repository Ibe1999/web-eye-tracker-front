
import os
import matplotlib.pyplot as plt
from github import Github

def count_labels(repo):
    labels_count = {}
    for issue in repo.get_issues(state="all"):
        for label in issue.labels:
            labels_count[label.name] = labels_count.get(label.name, 0) + 1
    return labels_count

def generate_histogram(repo_name, labels_count):
    if not labels_count:
        print("No labeled issues found")
        return None

    sorted_labels = sorted(labels_count.items(), key=lambda x: x[1], reverse=True)
    labels, counts = zip(*sorted_labels)

    plt.figure(figsize=(max(10, len(labels) * 0.5), 8))
    bars = plt.bar(labels, counts, color='#2ca02c')

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

    filename = "artifacts/histogram.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return filename

def main():
    token = os.getenv('GH_PATH')
    if not token:
        raise ValueError("GitHub token not found")

    repo_name = "Ibe1999/web-eye-tracker-front"
    
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        labels_count = count_labels(repo)
        
        if labels_count:
            generate_histogram(repo_name, labels_count)
            
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == '__main__':
    main()
