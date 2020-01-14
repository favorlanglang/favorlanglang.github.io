import os
import re
import mistune
import requests
import yaml
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape


#--------------- Helper functions --------------#
# Get dictionary index (dict items are constructed with Vue)
def getDictToc():
    toc = requests.get("https://favorlanglang.github.io/dict/dict-toc.json").text
    toc = [ "<li><a href='#" + id_ + f"'>{text}</a></li>" for id_, text in json.loads(toc) ]
    return ''.join(toc)

# Modify `config.yml`
def mdpath2html(dict_):
    for key in dict_:
        if type(dict_[key]) is dict:
            mdpath2html(dict_[key])
        elif type(dict_[key]) is list:
            for item in dict_[key]:
                mdpath2html(item)
        else:
            if re.match("^[a-zA-Z0-9/_-]+\.md$", dict_[key]):
                if not os.path.isfile(dict_[key]):
                    print(f"`{dict_[key]}` is not a markdown file")
                    return
                
                # Replace path with content in dict
                with open(dict_[key], encoding="utf-8") as f:
                    content = ''.join([line for line in f])
                dict_[key] = mistune.markdown(content, escape=False)

# Import `config.yml`
def import_config(fp='config.yml'):
    with open(fp, encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    mdpath2html(config)
    return config




#------------ Build Web site from templates/*.html -------------#
# Setup jinja2 template
env = Environment(
    loader=FileSystemLoader('templates')
)
# Import config.yml
config = import_config()

#  index.html
template = env.get_template('index.html')
with open("index.html", 'w', encoding="utf-8") as f:
    html_str = template.render(config['index'])
    f.write(html_str)

# intro.html
template = env.get_template('intro.html')
with open("intro.html", 'w', encoding="utf-8") as f:
    html_str = template.render(config['intro'])
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
    
