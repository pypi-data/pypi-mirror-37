'''$title preprocessor for Foliant.'''

from typing import Dict
OptionValue = int or float or bool or str

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'option': 'value'
    }
    tags = '$slug',

    def _process_tag(self, tag: str, options: Dict[str, OptionValue], body: str) -> str:
        '''Process tag invokation.

        :param tag: Tag name
        :param options: Options extracted from the tag definition
        :param body: Tag body

        :returns: Whatever you want
        '''

        self.logger.debug(f'Processing tag: {tag}, {options}, {body}')

        result = f'Processed {tag}, possibly using {self._private_attr} in the process'

        self.logger.debug(f'Replacing tag with "{result}"')

        return result

    def process_tags(self, content: str) -> str:
        '''Find tags and replace them with whatever you want.

        :param content: Markdown content

        :returns: Markdown content with tags definitions replaced with other things
        '''

        def _sub(diagram) -> str:
            return self._process_tag(
                diagram.group('tag'),
                self.get_options(diagram.group('options')),
                diagram.group('body')
            )

        return self.pattern.sub(_sub, content)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._private_attr = self.options['option']

        self.logger = self.logger.getChild('$slug')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def apply(self):
        self.logger.info('Applying preprocessor.')

        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()
            with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                markdown_file.write(self.process_tags(content))

        self.logger.info('Preprocessor applied.')
