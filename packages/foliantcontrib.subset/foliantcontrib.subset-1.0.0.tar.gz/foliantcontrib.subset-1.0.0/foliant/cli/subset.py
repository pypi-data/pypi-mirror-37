'''CLI extension for the ``subset`` command.'''

import re
from pathlib import Path
from logging import DEBUG, WARNING
from cliar import Cliar, set_arg_map, set_metavars, set_help


class Cli(Cliar):
    def _get_subset_dir_path(self, src_dir_path: Path, user_defined_path_str: str) -> Path:
        self.logger.debug(f'User-defined subset path: {user_defined_path_str}')

        subset_dir_path = Path(user_defined_path_str).expanduser()

        if src_dir_path.resolve() in subset_dir_path.resolve().parents \
            or src_dir_path.resolve() == subset_dir_path.resolve():

            self.logger.debug('The project source directory is included into user-defined subpath')

        else:
            subset_dir_path = src_dir_path / subset_dir_path

            if src_dir_path.resolve() in subset_dir_path.resolve().parents \
                or src_dir_path.resolve() == subset_dir_path.resolve():

                self.logger.debug('The project source directory is not included into user-defined subpath')

            else:
                self.logger.critical('User-defined subpath is outside the project source directory')

                raise RuntimeError('User-defined subpath is outside the project source directory')

        if subset_dir_path.is_dir():
            return subset_dir_path

        else:
            self.logger.critical('User-defined subpath is not an existing directory')

            raise RuntimeError('User-defined subpath is not an existing directory')

    def _rewrite_chapters_paths(self, partial_config: str, src_dir_path: Path, subset_dir_path: Path) -> str:
        chapter_line_pattern = re.compile(
            r'^(\s+\-\s+.+\.md)\s*$',
            flags=re.MULTILINE
        )

        chapter_line_components_pattern = re.compile(
            r'^(?P<indentation>\s+)\-\s+(?P<chapter_title>.+\:\s+)?(?P<chapter_file_path>[^\:]+\.md)\s*$',
            flags=re.MULTILINE
        )

        partial_config_components = chapter_line_pattern.split(partial_config)

        new_partial_config = ''

        for partial_config_component in partial_config_components:
            chapter_line = chapter_line_components_pattern.fullmatch(partial_config_component)

            if chapter_line:
                indentation = chapter_line.group('indentation')
                chapter_title = chapter_line.group('chapter_title')
                chapter_file_path = chapter_line.group('chapter_file_path')

                self.logger.debug(
                    'Processing the line of chapters section; ' +
                    f'indentation: "{indentation}", ' +
                    f'chapter title: {chapter_title}, ' +
                    f'Markdown file path: {chapter_file_path}'
                )

                rewritten_chapter_file_path = (subset_dir_path / chapter_file_path).relative_to(src_dir_path)

                self.logger.debug(f'Rewriting Markdown file path with: {rewritten_chapter_file_path}')

                if chapter_title:
                    new_partial_config += f'{indentation}- {chapter_title}{rewritten_chapter_file_path}'

                else:
                    new_partial_config += f'{indentation}- {rewritten_chapter_file_path}'

            else:
                new_partial_config += partial_config_component

        return new_partial_config

    @set_arg_map(
        {
            'project_dir': 'project-dir',
            'src_dir': 'src-dir',
            'no_rewrite_paths': 'no-rewrite',
            'config_file_name': 'config'
        }
    )
    @set_metavars({'pathstr': 'SUBPATH'})
    @set_help(
        {
            'SUBPATH': "Path to the subset of the Foliant project",
            'project_dir': "Path to the Foliant project root directory, default './'",
            'src_dir': "Path to the Foliant project source directory, default './src/'",
            'no_rewrite_paths': "Do not rewrite the paths of Markdown files in the partial config",
            'config_file_name': "Name of config file of the Foliant project, default 'foliant.yml'",
            'debug': "Log all events during build. If not set, only warnings and errors are logged"
        }
    )
    def subset(
        self,
        pathstr,
        project_dir='./',
        src_dir='./src/',
        no_rewrite_paths=False,
        config_file_name='foliant.yml',
        debug=False
    ):
        '''Generate subset config file using partial data from SUBPATH.'''

        self.logger.setLevel(DEBUG if debug else WARNING)

        self.logger.info('Processing started')

        project_dir_path = Path(project_dir).expanduser()
        src_dir_path = Path(src_dir).expanduser()

        self.logger.debug(f'Project root directory: {project_dir_path}')
        self.logger.debug(f'Project source directory: {src_dir_path}')

        subset_dir_path = self._get_subset_dir_path(src_dir_path, pathstr)

        self.logger.debug(f'Subset directory path: {subset_dir_path}')

        common_config_file_name = config_file_name + '.common'

        self.logger.debug(f'Reading the common config part from the file {common_config_file_name}')

        with open(project_dir_path / common_config_file_name, encoding='utf8') as common_config_file:
            common_config = common_config_file.read()

        partial_config_file_name = config_file_name + '.partial'

        self.logger.debug(f'Reading the partial config from the file {partial_config_file_name}')

        with open(subset_dir_path / partial_config_file_name, encoding='utf8') as partial_config_file:
            partial_config = partial_config_file.read()

        if not no_rewrite_paths:
            partial_config = self._rewrite_chapters_paths(partial_config, src_dir_path, subset_dir_path)

        subset_config = partial_config + '\n\n' + common_config

        self.logger.debug(f'Writing the subset config to the file {config_file_name}')

        with open(project_dir_path / config_file_name, 'w', encoding='utf8') as subset_config_file:
            subset_config_file.write(subset_config)

        self.logger.info('Processing finished')
