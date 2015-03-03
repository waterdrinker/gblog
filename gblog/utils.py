
import re
import markdown
from unidecode import unidecode
import MySQLdb

def get_tags(tags):
    """Return a string of tags separated by commas"""
    # Remove the space near commas 
    tags=re.sub(r'\s*[,]+\s*', ',', tags)
    # Remove the space in begining and end
    tags=re.sub(r'(^\s)|(\s$)','', tags)
    # Remove the commas in begining and end
    tags=re.sub(r'(^,)|(,$)','', tags)
    return tags

def get_nice_slug(title):
    """Return slug with hyphen and asscii characters"""
    slug = unidecode(title)
    slug = re.sub(r"[^\w]+", " ", slug)
    return "-".join(slug.lower().strip().split())
    

def get_html_abstract(text, size=150):
    """
    Handler markdown test

    Input: markdown text and abstract size
    Return: html and abstract
    """
    extensions=[
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.smart_strong'
    ]

    html=markdown.markdown(text,extensions)
    if len(text) > size:
        abstract=text[0:size] + " ..."
    else:
        abstract=text

    abstract=markdown.markdown(abstract,extensions)
    return html,abstract

    # Description: Edit html
    #
    # Remove the space between <p> and </p>
    # Remove the beginning space
    # Replace \n with " "
    #html=re.sub("\n", " ", html);
    #html=re.sub(">\s*<", "><", html);
    #html=re.sub("^\s*", "", html);

    # Get the list of html paragrap (between <p> and </p>)
    #line_list = re.findall("<[\w]+>(.*?)</[\w]+>", html);

    # Calculate the filter position of html
    #sum = 0
    #linecount = 0
    #for line in line_list:
        #sum += len(line)
        #linecount += 1
        #if sum > 200 or linecount > 5:
            #break;
    #sum = sum+7*linecount

def format_comment_content(text):
    
    content=re.sub("^\s*", "", text)
    content=re.sub("\r\n", "<br/>", content)
    content=re.sub("\n", "<br/>", content)
    content=re.sub("\r", "<br/>", content)
    content=re.sub("$\s*", "", content)

    return content


def escape_text(text):
    # escape for python braces in string
    text=re.sub("{", "{{", text)
    text=re.sub("}", "}}", text)
    # escape for mysql
    text=MySQLdb.escape_string(text)
    return text





