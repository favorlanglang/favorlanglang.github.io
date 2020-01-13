from jinja2 import Environment, FileSystemLoader, select_autoescape
from construct_dict import getDictItems

env = Environment(
    loader=FileSystemLoader('templates')
)


#------------ Build Web site from templates/*.html -------------#

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
dict_str, toc_str = getDictItems()
template = env.get_template('dict.html')
with open("dict.html", 'w', encoding="utf-8") as f:
    html_str = template.render(dictionary=dict_str, toc=toc_str, sidebar=False)
    f.write(html_str)

# search.html (Vue app)
template = env.get_template('search.html')
with open("search.html", 'w', encoding="utf-8") as f:
    html_str = template.render(sidebar=False)
    f.write(html_str)
    
