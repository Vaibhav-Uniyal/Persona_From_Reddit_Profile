import praw
import json

# Reddit API credentials (replace with your own or use environment variables for security)
CLIENT_ID = 'P4V_kuno9OdjMUF7j01_lg'
CLIENT_SECRET = 'hLBnU2Hivrg6E7T5hMTopf73ul4lKA'
USER_AGENT = 'ClassProfessional517 '

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def fetch_user_data(username):
    user = reddit.redditor(username)
    posts = []
    comments = []
    profile_pic_url = getattr(user, 'icon_img', None)
    for submission in user.submissions.new(limit=None):
        posts.append({
            'title': submission.title,
            'body': submission.selftext,
            'url': submission.url,
            'created_utc': submission.created_utc
        })
    for comment in user.comments.new(limit=None):
        comments.append({
            'body': comment.body,
            'url': f"https://reddit.com{comment.permalink}",
            'created_utc': comment.created_utc
        })
    data = {
        'username': username,
        'profile_photo': profile_pic_url,
        'posts': posts,
        'comments': comments
    }
    with open(f"{username}_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(posts)} posts and {len(comments)} comments to {username}_data.json (profile photo: {profile_pic_url})")

def main():
    username = input("Enter Reddit username (without u/): ")
    fetch_user_data(username)

if __name__ == "__main__":
    main() 