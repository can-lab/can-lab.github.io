import os
import fnmatch
import codecs
import glob

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup


def _render_template(template_filename, context):
    TEMPLATE_ENVIRONMENT = Environment(autoescape=False,
                                       loader=FileSystemLoader('source'),
                                       trim_blocks=False)

    return TEMPLATE_ENVIRONMENT.get_template(template_filename.replace("\\", "/")).render(context)

def delete_html_files():
    files = glob.glob("*.html")
    for file_ in files:
        os.remove(file_)

def create_html_files():
    members = []
    files = []
    for root, dirnames, filenames in os.walk('source'):
            for filename in fnmatch.filter(filenames, '*.html'):
                        files.append(os.path.join(root, filename))
                        if "lab_members" in root:
                            with codecs.open(os.path.join(root, filename), 'r', "utf-8") as f:
                                source_code = f.read()
                            soup = BeautifulSoup(source_code, features="html.parser")
                            members.append({"name": soup.h1.text,
                                            "function": soup.p.text.lower(), # ** .lower() added by Laura de Nooij, 24-09-2020
                                            "url": "_".join(soup.h1.text.lower().split()) + ".html",
                                            "image": soup.span.img['src']})

#   # Sort first by length of function (PI < Postdoc < PhD student < Master student), then by LAST name ** commented out by Laura de Nooij, 24-09-2020
#    members.sort(key=lambda x: (len(x["function"]), x["name"].split(" ")[-1]))

    # Sort functions ** added by Laura de Nooij, 24-09-2020
    members_pi = [d for d in members if d['function'] == 'pi']
    members_pi.sort(key=lambda x: x["name"].split(" ")[-1])
    members_sr = [d for d in members if d['function'] == 'senior researcher']
    members_sr.sort(key=lambda x: x["name"].split(" ")[-1])
    members_postdoc = [d for d in members if d['function'] == 'postdoc']
    members_postdoc.sort(key=lambda x: x["name"].split(" ")[-1])
    members_phd = [d for d in members if d['function'] == 'phd candidate']
    members_phd.sort(key=lambda x: x["name"].split(" ")[-1])
    members_extphd = [d for d in members if d['function'] == 'external phd candidate']
    members_extphd.sort(key=lambda x: x["name"].split(" ")[-1])
    members_ra = [d for d in members if d['function'] == 'research assistant']
    members_ra.sort(key=lambda x: x["name"].split(" ")[-1])
    members_tr = [d for d in members if d['function'] == 'trainee']
    members_tr.sort(key=lambda x: x["name"].split(" ")[-1]) 
    members = members_pi + members_sr + members_postdoc + members_phd + members_extphd + members_ra + members_tr
    
    context = {
            'members': members
        }
    for file_ in files:
        file_ = file_.replace("source" + os.path.sep, "")
        if file_ == "base.html":
            continue
        with codecs.open(os.path.split(file_)[1], 'w', encoding='utf-8') as f:
            print(file_)
            html = _render_template(file_, context)
            f.write(html)


def main():
    delete_html_files()
    create_html_files()

if __name__ == "__main__":
    main()
