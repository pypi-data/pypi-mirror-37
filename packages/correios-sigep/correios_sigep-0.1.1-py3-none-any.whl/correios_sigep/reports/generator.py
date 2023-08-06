from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os
import pdfkit
import tempfile

class Generator(object):
    def __init__(self, folder=''):
        if not folder:
            path = os.path.abspath(__file__)
            dir_path = os.path.dirname(path)
            folder = '{}/templates/'.format(dir_path)
        self._env = Environment(
            loader=FileSystemLoader(folder),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, file_name, **params):
        tpl = self._env.get_template(file_name)
        return tpl.render(**params)

    def makePdf(self, paths, out=''):
        if not out:
            file = tempfile.NamedTemporaryFile(delete=False)
            pdfkit.from_file(paths, '{}'.format(file.name))
            file.close()
        else:
            pdfkit.from_file(paths, out)
