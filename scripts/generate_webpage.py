import csv
import hashlib
import os

from common import filename_for

topics_file = os.environ.get('TOPICS_FILE', 'inputs/topics.csv')
styles_file = os.environ.get('STYLES_FILE', 'inputs/styles.csv')
output_path = os.environ.get('OUTPUT_PATH', 'html/index.html')
url_prefix = os.environ.get('URL_PREFIX', 'https://sdgrid.lacop.dev/images/')

IMAGE_COUNT = 4

styles = []
topics = []
with open(styles_file) as f:
    styles = list(csv.DictReader(f))
with open(topics_file) as f:
    topics = list(csv.DictReader(f))

content = """
<!doctype html>
<html>
<head>
    <style>
        table, tr, td {
            border: 1px solid darkgrey;
            border-collapse: collapse;
        }
        td img.large {
            padding: 0 0 2px 0;
        }
        td a:nth-child(4) img {
            padding: 0 1px;
        }
        #sidebar {
            position: fixed;
            top: 3em;
            right: 3em;
            border: 1px solid black;
            padding: 1em;
            background: white;
        }
        #sidebar-content {
            display: none;
        }
        #sidebar img {
            padding: 5px;
        }
        #prompt {
            background: lightgrey;
            padding: 2ex;
            display: inline-block;
            width: 90%;
        }
        #topic {
            background: lightyellow;
            padding: 1ex;
        }
        #images {
            max-width: 1050px;
        }
        #close {
            font-size: 200%;
        }
        p.jump {
            max-width: 70%;
        }
        a.jump {
            padding-left: 1ex;
            display: inline-block;
        }
    </style>
</head>
<body>
"""

content += """
<h1>A collection of Stable Diffusion images</h1>
<p>Contains <em>{}</em> topics across <em>{}</em> styles resulting in <em>{}</em> prompts.
Each prompt has <em>{}</em> variants (seeds) for a total of <strong>{}</strong> images.</p>
""".format(
    len(topics), len(styles),
    len(topics)*len(styles),
    IMAGE_COUNT,
    len(topics)*len(styles)*IMAGE_COUNT
)
content += '<p>All prompts use the same set of seeds which gives an interesting view '
content += 'how the style affects the result. Check out <a href="info.html">more info</a> '
content += 'including source code.</p>'
content += '<p class="jump">Jump to category: '
categories = {}
for style in styles:
    if style['category'] not in categories:
        category = len(categories) + 1
        categories[style['category']] = category
        content += '<a class="jump" href="#category-' + str(category) +'">'
        content += style['category']
        content += '</a>'
content += '</p>'

content += '<table><tr><td></td>'
for topic in topics:
    content += '<td class="topic" data-topic="{0}">{0}</td>'.format(topic['topic'])
content += '</tr>'

last_category = 0
for style in styles:
    category = categories[style['category']]
    if category != last_category:
        assert category == last_category + 1
        last_category = category
        content += '<tr><td colspan="' + str(1 + len(topics)) + '" id="category-' + str(category) +'">'
        content += style['category'] + '</td></tr>'
    content += '<tr><td data-prompt="{}">{}</td>'.format(style['prompt'], style['name'])
    for topic in topics:
        prompt = style['prompt'].replace('$1', topic['topic'])
        content += '<td>'
        for i in [0]:
            filename = filename_for(prompt, i)
            content += '<a href="{}{}{}.jpg"><img width=256 height=256 class="large" loading="lazy" src="{}{}{}.jpg"/></a>'.format(
                url_prefix, '512/', filename,
                url_prefix, '256/', filename)
        content += "<br>"
        for i in range(IMAGE_COUNT)[1:]:
            filename = filename_for(prompt, i)
            content += '<a href="{}{}{}.jpg"><img width=84 height=84 loading="lazy" src="{}{}{}.jpg"/></a>'.format(
                url_prefix, '512/', filename,
                url_prefix, '256/', filename)
        content += '</td>'
content += '</table>'

content += """
<div id="sidebar">
    <p id="sidebar-help">Click any image to show more!</p>
    <div id="sidebar-content">
        <p id="prompt">...</p>
        <input id="close" type="button" value="X">
        <div id="images"></div>
    </div>
</div>
"""

content += """
<script>
document.querySelectorAll('table img').forEach(el => el.onclick = function() {
    var table_cell = el.parentElement.parentElement;
    
    var row_label = table_cell;
    var i = 1;
    while (row_label.previousSibling != null) {
        row_label = row_label.previousSibling;
        i++;
    }
    var column_label = document.querySelector('table tr td:nth-child(' + i + ')');
    
    document.getElementById('prompt').innerHTML = row_label.dataset.prompt.replace(
        '$1', '<span id="topic">' + column_label.dataset.topic + '</span>');
    
    document.getElementById('images').innerHTML = '';
    console.log(table_cell);
    table_cell.querySelectorAll('img').forEach(img => {
        var src = img.src.replace('/256/', '/512/');
        document.getElementById('images').innerHTML += 
            '<a href="' + src + '" target="_blank">' +
            '<img width=512 height=512 src="' + src + '"/></a>';
    });

    document.getElementById('sidebar-help').style.display = 'none';
    document.getElementById('sidebar-content').style.display = 'block';
    return false; // Middle click to open in background still works.
});

document.getElementById('close').onclick = function() {
    document.getElementById('sidebar-content').style.display = 'none';
    document.getElementById('sidebar-help').style.display = 'block';
};

</script>
</body>
</html>
"""

with open(output_path, 'w') as f:
    f.write(content)