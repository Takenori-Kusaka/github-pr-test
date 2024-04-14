import os
from openai import OpenAI
from github import Github

ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
pr_number = int(os.getenv("PR_NUMBER"))
pr = repo.get_pull(pr_number)

pr_title = pr.title
pr_body = pr.body
pr_author = pr.user.login
merged_by = pr.merged_by.login if pr.merged else ""

reviews = []
for review in pr.get_reviews():
    if review.state == "APPROVED":
        reviews.append(f"- {review.user.login} approved the PR")
review_summary = "\n".join(reviews)

comments = []
for comment in pr.get_issue_comments():
    comments.append(f"- {comment.user.login}: {comment.body}")
comment_summary = "\n".join(comments)

prompt = f"""
以下はGitHubのプルリクエストの情報です。このPRの内容を日本語で400文字程度でまとめてください。
PR作成者、マージ者、レビュー完了者、主なコメント指摘も含めてください。

タイトル:
{pr_title}

説明:
{pr_body}

PR作成者: {pr_author}
マージ者: {merged_by}

レビュー完了者:
{review_summary}

主なコメント:
{comment_summary}
"""

response = ai_client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "あなたはGitHubのプルリクエストを要約するアシスタントです。"},
        {"role": "user", "content": prompt}
    ],
    max_tokens=400,
    n=1,
    stop=None,
    temperature=0.7,
)

summary = response.choices[0].message.content.strip()

report = f"""
# Pull Request Summary

## 概要
- PR #{pr_number} は {pr_author} によって作成されました。
- このPRは {merged_by} によってマージされました。

## 要約
{summary}

## レビュー完了者
{review_summary}

## 主なコメント
{comment_summary}
"""

with open("pr_summary.md", "w") as f:
    f.write(report)
