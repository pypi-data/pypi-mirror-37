'''
Preprocessor for Foliant documentation authoring tool.
Generates image captions using alternative texts for images.
'''


import re
from pathlib import Path

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'stylesheet_path': Path('imgcaptions.css'),
        'targets': [],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('imgcaptions')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._stylesheet = self._get_stylesheet(self.options['stylesheet_path'])

    def _get_stylesheet(self, stylesheet_file_path: Path) -> str:
        self.logger.debug(f'Stylesheet file path: {stylesheet_file_path}')

        if stylesheet_file_path.exists():
            self.logger.debug('Using stylesheet from the file')

            with open(stylesheet_file_path, encoding='utf8') as stylesheet_file:
                return stylesheet_file.read()

        else:
            self.logger.debug('Stylesheet file does not exist; using default stylesheet')

            return '''
.image_caption {
    font-size: .8em;
    font-style: italic;
    text-align: right;
    }
'''

    def process_captions(self, content: str) -> str:
        _image_pattern = re.compile(r'\!\[(?P<caption>.+)\]\((?P<path>.+)\)')

        content = re.sub(
            _image_pattern,
            "![\g<caption>](\g<path>)\n\n" +
            "<p class=\"image_caption\">\g<caption></p>",
            content
        )

        content = f'<style>\n{self._stylesheet}\n</style>\n\n{content}'

        self.logger.debug('Content modified')

        return content

    def apply(self):
        self.logger.info('Applying preprocessor')

        self.logger.debug(f'Allowed targets: {self.options["targets"]}')
        self.logger.debug(f'Current target: {self.context["target"]}')

        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            for markdown_file_path in self.working_dir.rglob('*.md'):
                self.logger.debug(f'Processing Markdown file: {markdown_file_path}')

                with open(markdown_file_path, encoding='utf8') as markdown_file:
                    content = markdown_file.read()

                with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                    markdown_file.write(self.process_captions(content))

        self.logger.info('Preprocessor applied')
