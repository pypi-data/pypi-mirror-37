import os
from math import ceil
from urllib.parse import quote
from PIL import Image
from jinja2 import Template
from shutil import copytree, rmtree

def gen_gal(in_path, out_path):
    def scan_dir(base_path):
        def scan(scan_path):
            entries = {
                'dirs': [],
                'files': []
            }
            for entry in os.scandir(scan_path):
                if entry.is_dir():
                    entries['dirs'].append({'name': entry.name, 'absolute_path': entry.path.replace(base_path, out_path), 'path': './' + quote(entry.name) + '/index.html', 'contents': scan(entry.path)})
                else:
                    image = Image.open(entry.path.replace(base_path, out_path))
                    w, h = image.size
                    size = (700, h)
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(entry.path.replace(base_path, out_path).replace(entry.name, 'thumbnail_' + entry.name))
                    entries['files'].append({'name': entry.name, 'thumbnail_path': './thumbnail_' + quote(entry.name), 'path': './' + quote(entry.name)})
            entries['dirs'] = sorted(entries['dirs'], key=lambda item: item['name'].lower())
            entries['files'] = sorted(entries['files'], key=lambda item: item['name'].lower())
            pgcount = ceil(len(entries['files']) / 6)
            pages = [{
                'index': 0,
                'prev': -1,
                'next': -1,
                'pgcount': pgcount,
                'dirs': entries['dirs'],
                'files': []
            }]
            if pgcount > 1:
                pages[0]['next'] = 1
            i = 0
            pgi = 0
            for file in entries['files']:
                if i > 5:
                    pgi += 1
                    pages.append({
                        'index': pgi,
                        'prev': -1,
                        'next': -1,
                        'pgcount': pgcount,
                        'dirs': [],
                        'files': []
                    })
                    if pgi > 0:
                        pages[pgi]['prev'] = pgi - 1
                    if pgi < pgcount - 1:
                        pages[pgi]['next'] = pgi + 1
                    i = 0
                pages[pgi]['files'].append(file)
                i += 1
            return pages
        return scan(base_path)
    def gen_dir_html(pages, path):
        for page in pages:
            if page['index'] == 0:
                name = 'index.html'
            else:
                name = 'page' + str(page['index']) + '.html'
            template = Template(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'index.tmpl'), 'r').read())
            rendered = template.render(title='abpig', index=page['index'], prev=page['prev'], next=page['next'], pgcount=page['pgcount'], dirs=page['dirs'], files=page['files'])
            open(os.path.join(path, name), 'w').write(rendered)
            for dirr in page['dirs']:
                gen_dir_html(dirr['contents'], dirr['absolute_path'])
    if os.path.exists(out_path):
        rmtree(out_path)
    copytree(in_path, out_path)
    entries = scan_dir(in_path)
    gen_dir_html(entries, out_path)
