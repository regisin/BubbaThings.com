from pathlib import Path
import shutil
import os
import frontmatter
import markdown

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
env.globals['BASE_URL'] = 'https://bubbathings.com'

# build dir
dist = Path('./dist')
# static dir
static = Path('./static')
# content dir
content = Path('./content')

# Remove previous build if it exists
shutil.rmtree(dist, ignore_errors=True)

# Create destination folder/build dir
dist.mkdir()

# copy /static/* to /dist/*
shutil.copytree(static, dist, dirs_exist_ok=True)

# read posts
posts = []
for post in os.listdir(content/"posts"):
    meta = frontmatter.load(content/"posts"/post/"index.md")

    post_dict = {
        'slug': post,
        'title': meta['title'] if 'title' in meta.keys() else "Hello world",
        'description': meta['description'] if 'description' in meta.keys() else "Description of hello world.",
        'categories': meta['categories'] if 'categories' in meta.keys() else [],
        'comments': meta['comments'] if 'comments' in meta.keys() else [],
        'date': meta['date'].strftime("%B %d, %Y"),
        'markdown': meta.content,
        'body': markdown.markdown(meta.content)
    }
    posts.append(post_dict)

# build home page
template = env.get_template("posts.html")
template.stream(posts=posts).dump(str(dist/"index.html"))



# build each post
template = env.get_template("post.html")
for post in posts:
    post_dist = dist / post['slug']
    post_dist.mkdir()
    images_dist = post_dist / 'images'
    images_dist.mkdir()
    try:
        shutil.copytree(content/post['slug']/'images', images_dist, dirs_exist_ok=True)
    except FileNotFoundError as e:
        print("~Exception excepted~", e)
    template.stream(post=post).dump(str(dist / post['slug'] / "index.html"))

