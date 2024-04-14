import os
import re
import requests

def update_backlog_issue(issue_key, status):
    api_key = os.environ["BACKLOG_API_KEY"]
    space_name = os.environ["BACKLOG_SPACE_NAME"]
    
    url = f"https://{space_name}.backlog.com/api/v2/issues/{issue_key}?apiKey={api_key}"
    
    data = {
        "statusId": status
    }
    
    response = requests.patch(url, data=data)
    
    if response.status_code == 200:
        print(f"Successfully updated issue {issue_key} to status {status}")
    else:
        print(f"Failed to update issue {issue_key}. Response: {response.text}")

def extract_issue_key(branch_name):
    match = re.search(r"feature/(.*)", branch_name)
    if match:
        return match.group(1)
    else:
        return None

def main():
    branch_name = os.environ["GITHUB_REF_NAME"]
    
    issue_key = extract_issue_key(branch_name)
    
    if issue_key:
        update_backlog_issue(issue_key, 2)  # 2 は "処理中" のステータスID
    else:
        print(f"No issue key found in branch name: {branch_name}")

if __name__ == "__main__":
    main()
