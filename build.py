import requests
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape


#--------------- Helper functions --------------#
# Get dictionary index (dict items are constructed with Vue)
def getDictToc():
    toc = requests.get("https://favorlanglang.github.io/dict/dict-toc.json").text
    toc = [ "<li><a href='#" + id_ + f"'>{text}</a></li>" for id_, text in json.loads(toc) ]
    return ''.join(toc)


#------------ Build Web site from templates/*.html -------------#
# Setup jinja2 template
env = Environment(
    loader=FileSystemLoader('templates')
)

#  index.html
template = env.get_template('index.html')
with open("index.html", 'w', encoding="utf-8") as f:
    html_str = template.render(sidebar=True)
    f.write(html_str)

# intro.html
template = env.get_template('intro.html')
with open("intro.html", 'w', encoding="utf-8") as f:
    html_str = template.render(sidebar=False, sectionTitle="簡介")
    f.write(html_str)

# render dict.html
toc_str = getDictToc()
template = env.get_template('dict.html')
with open("dict.html", 'w', encoding="utf-8") as f:
    html_str = template.render(toc=toc_str, sidebar=False)  # Note: dict items are constructed with Vue
    f.write(html_str)

# search.html (Vue app)
template = env.get_template('search.html')
with open("search.html", 'w', encoding="utf-8") as f:
    html_str = template.render(sidebar=False)
    f.write(html_str)
    
