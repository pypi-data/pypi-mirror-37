import collections
import jinja2
import os
import re
import shutil

from latex import build_pdf


class ResumeTemplate(object):
    def __init__(self, path, custom_font_paths=None):
        if custom_font_paths is None:
            custom_font_paths = []

        self.path = path
        self.custom_font_paths = custom_font_paths


class ResumeGenerator(object):
    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.')))
    sanitize_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}'}
    sanitize_regex = re.compile('|'.join(
        re.escape(key)
        for key in sorted(sanitize_chars.keys(), key=lambda item: - len(item))))

    def _sanitize(self, obj):
        if isinstance(obj, list):
            return [self._sanitize(x) for x in obj]
        elif isinstance(obj, collections.Mapping):
            for k, v in obj.items():
                if isinstance(v, collections.Mapping):
                    obj[k] = self._sanitize(obj[k])
                elif isinstance(v, list):
                    for i in range(len(v)):
                        obj[k][i] = self._sanitize(obj[k][i])
                else:
                    obj[k] = self.sanitize_regex.sub(lambda match: self.sanitize_chars[match.group()], v)

        return obj

    def _to_pdf(self, latex_file, custom_fonts=None):
        if custom_fonts is None:
            custom_fonts = []

        for custom_font in custom_fonts:
            shutil.copy2(custom_font, self.font_dir)

        return build_pdf(latex_file, builder=self.builder)

    def __init__(self, builder='xelatexmk', font_dir='/usr/share/fonts/'):
        self.builder = builder
        self.font_dir = font_dir

    def generate(self, template, person, save_path):
        latex_cv = self.latex_jinja_env.get_template(template.path).render(self._sanitize(person.to_json()))
        pdf = self._to_pdf(latex_cv, template.custom_font_paths)
        pdf.save_to(save_path)
