import os
from math import ceil
from urllib.parse import quote
from PIL import Image
from jinja2 import Template
from shutil import copytree, rmtree

def gengal(inpath, outpath):
    def scandir(basepath):
        def scan(scanpath):
            entries = {
                'dirs': [],
                'files': []
            }
            for entry in os.scandir(scanpath):
                if entry.is_dir():
                    entries['dirs'].append({'name': entry.name, 'abspath': entry.path.replace(basepath, outpath), 'path': './' + quote(entry.name) + '/index.html', 'contents': scan(entry.path)})
                else:
                    image = Image.open(entry.path.replace(basepath, outpath))
                    w, h = image.size
                    size = (700, h)
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(entry.path.replace(basepath, outpath).replace(entry.name, 'thumb' + entry.name))
                    entries['files'].append({'name': entry.name, 'thumbpath': './thumb' + quote(entry.name), 'path': './' + quote(entry.name)})
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
        return scan(basepath)
    def gendirhtml(pages, path):
        for page in pages:
            if page['index'] == 0:
                name = 'index.html'
            else:
                name = 'page' + str(page['index']) + '.html'
            template = Template(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'index.tmpl'), 'r').read())
            rendered = template.render(title='abpig', index=page['index'], prev=page['prev'], next=page['next'], pgcount=page['pgcount'], dirs=page['dirs'], files=page['files'])
            open(os.path.join(path, name), 'w').write(rendered)
            for dirr in page['dirs']:
                gendirhtml(dirr['contents'], dirr['abspath'])
    if os.path.exists(outpath):
        rmtree(outpath)
    copytree(inpath, outpath)
    entries = scandir(inpath)
    gendirhtml(entries, outpath)
