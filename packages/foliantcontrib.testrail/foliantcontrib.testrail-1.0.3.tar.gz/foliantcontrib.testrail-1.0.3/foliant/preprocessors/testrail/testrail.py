'''
Preprocessor for Foliant documentation authoring tool.
Collects test cases from TestRail project to markdown file.
'''


from foliant.preprocessors.base import BasePreprocessor
from .testrailapi import *

from jinja2 import Environment, FileSystemLoader
from pkg_resources import resource_filename
import os
from pathlib import Path
from pprint import pprint
from shutil import copytree, copyfile
import re


class Preprocessor(BasePreprocessor):
    defaults = {
        'filename': 'test_cases.md',
        'rewrite_src_file': False,
        'template_folder': 'case_templates',
        'platform_id': 0,
        'platforms': 'smarttv, androidtv, appletv, web',
        'section_header': 'Программа испытаний',
        'std_table_header': 'Таблица прохождения испытаний',
        'std_table_column_headers': '№; ID; Название; Успешно; Комментарий',
        'suite_ids': set(),
        'section_ids': set(),
        'add_cases_without_platform': True,
        'add_unpublished_cases': True,
        'add_case_id_to_case_name': False,
        'add_std_table': True,
        'resolve_urls': False,
        'screenshots_url': '',
        'screenshots_ext': '.png',
        'print_case_structure': False,
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('testrail')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        self._filename = self.options['filename']
        self._rewrite_src_file = self.options['rewrite_src_file']
        self._template_folder = self.options['template_folder']
        self._section_header = self.options['section_header']

        self._std_table_header = self.options['std_table_header']
        self._std_table_column_headers = self.options['std_table_column_headers'].replace(' ', '').split(';')

        self._testrail_url = self.options['testrail_url']
        self._testrail_login = self.options['testrail_login']
        self._testrail_pass = self.options['testrail_pass']

        self._client = testrailapi.APIClient(self._testrail_url)
        self._client.user = self._testrail_login
        self._client.password = self._testrail_pass

        self._project_id = self.options['project_id']

        self._suite_ids = set()
        self._suite_ids = self._parse_ids_options(self._suite_ids, self.options['suite_ids'])

        self._section_ids = set()
        self._section_ids = self._parse_ids_options(self._section_ids, self.options['section_ids'])

        self._platform_id = self.options['platform_id']
        self._platforms = self.options['platforms'].replace(' ', '').split(',')
        if not self._platform_id == self.defaults['platform_id']:
            self._platform_name = self._platforms[self._platform_id-1]
        else:
            self._platform_name = ''

        self._add_cases_without_platform = self.options['add_cases_without_platform']
        self._add_unpublished_cases = self.options['add_unpublished_cases']
        self._add_case_id_to_case_name = self.options['add_case_id_to_case_name']
        self._add_std_table = self.options['add_std_table']

        self._resolve_urls = self.options['resolve_urls']
        if not self._platform_id == self.defaults['platform_id']:
            self._screenshots_url = '/'.join((self.options['screenshots_url'], 'raw/master/images', self._platform_name, ''))
        else:
            self._screenshots_url = '/'.join((self.options['screenshots_url'], 'raw/master/images/'))
        self._screenshots_ext = self.options['screenshots_ext']

        self._print_case_structure = self.options['print_case_structure']

        self._case_counter = 0
        self._test_cases = ['# ' + self._section_header + '\n\n']
        self._std_table = []

        self._env = Environment(loader=FileSystemLoader(str(self.project_path)))

        self._template_folder = self.options['template_folder']
        if self._template_folder == self.defaults['template_folder'] and not os.path.exists(self.project_path / self.defaults['template_folder']):
            copytree(resource_filename(__name__, 'case_templates'), self.project_path / self.defaults['template_folder'])

    def _parse_ids_options(self, variable, option):
        if option:
            for item in str(option).replace(' ', '').split(','):
                variable.add(int(item))
        else:
            variable = option
        return variable


    def _collect_suites_and_sections_ids(self, project_suites):

        if not self._suite_ids:
            if not self._section_ids:
                for suite in project_suites:
                    self._suite_ids.add(suite['id'])
            else:
                for suite in project_suites:
                    suite_sections = self._client.send_get('get_sections/%s&suite_id=%s' % (self._project_id, suite['id']))
                    for section in suite_sections:
                        if section['id'] in self._section_ids:
                            self._suite_ids.add(suite['id'])
                            continue
        if not self._section_ids:
            for suite in project_suites:
                if suite['id'] in self._suite_ids:
                    suite_sections = self._client.send_get('get_sections/%s&suite_id=%s' % (self._project_id, suite['id']))
                    for section in suite_sections:    
                        self._section_ids.add(section['id'])

        next_iteration = True  # collect all child subsections for sections specified
        while next_iteration:
            next_iteration = False
            for suite in project_suites:
                if suite['id'] in self._suite_ids:
                    suite_sections = self._client.send_get('get_sections/%s&suite_id=%s' % (self._project_id, suite['id']))
                    for section in suite_sections:
                        if section['id'] not in self._section_ids and section['parent_id'] in self._section_ids:    
                            self._section_ids.add(section['id'])
                            next_iteration = True


    def _collect_cases(self, project_suites):
        for suite in project_suites:

            if suite['id'] in self._suite_ids:

                if len(self._suite_ids) > 1:  # Add suite names if present and raise next chapters title level
                    self._test_cases.append('## %s\n\n' % suite['name'])
                    suite['name'] = ''.join(('**', suite['name'].upper(), '**'))

                    if self._add_case_id_to_case_name:
                        self._std_table.append((' | '.join(('', ' ', ' ', suite['name'], ' ', ' ', ' '))).strip())
                    else:
                        self._std_table.append((' | '.join(('', ' ', suite['name'], ' ', ' ', ' '))).strip())

                    if suite['description']:
                        self._test_cases.append('%s\n\n' % suite['description'])
                    shift_title_level = 1
                else:
                    shift_title_level = 0

                self._collect_sections(suite['id'], shift_title_level)


    def _collect_sections(self, suite_id, shift_title_level):
        suite_sections = self._client.send_get('get_sections/%s&suite_id=%s' % (self._project_id, suite_id))

        for section in suite_sections:

            title_level_up = ''
            for i in range(section['depth'] + shift_title_level):
                title_level_up += '#'

            section_name = re.sub("[0-9].*\.", "", section['name']).strip()  # Remove numbers in section headers

            if section_name.isupper():  # Remove headers capitalization
                section_name = section_name.lower()
                section_name = section_name[0].upper() + section_name[1:]

            self._test_cases.append('##%s %s\n\n' % (title_level_up,
                            section_name))

            section_name = ''.join(('**', section_name, '**'))
            if self._add_case_id_to_case_name:
                self._std_table.append((' | '.join(('', ' ', ' ', section_name, ' ', ' ', ' '))).strip())
            else:
                self._std_table.append((' | '.join(('', ' ', section_name, ' ', ' ', ' '))).strip())

            if section['id'] in self._section_ids:  # This condition is checked not earlier to save parent chapter headers

                if section['description']:
                    self._test_cases.append('%s\n\n' % section['description'])

                self._collect_case_data(suite_id, section['id'], title_level_up)


    def _collect_case_data(self, suite_id, section_id, title_level_up):
        section_cases = self._client.send_get(
            'get_cases/%s&suite_id=%s&section_id=%s' %
            (self._project_id, suite_id, section_id))

        for case in section_cases:

            if 'custom_prj_type' not in case.keys():  # Collect cases without platform assigned or not
                if self._add_cases_without_platform:
                    case.update({'custom_prj_type': [self._platform_id]})
                else:
                    case.update({'custom_prj_type': [0]})

            if 'custom_tp' not in case.keys():  # If test-case template has no TP field (test-case published), test-cases will be collected on 'add_unpublished_cases' value basis
                case.update({'custom_tp': None})

            if (case['custom_tp'] or self._add_unpublished_cases) and self._platform_id in case['custom_prj_type']:  # Second codition is for test-cases without platform assigned

                self._case_counter += 1

                if self._add_case_id_to_case_name:
                    self._std_table.append((' | '.join(('', str(self._case_counter), str(case['id']), case['title'], ' ', ' ', ' '))).strip())
                    self._test_cases.append('###%s %s (C%s)\n\n' % (title_level_up, case['title'], case['id']))
                else:
                    self._std_table.append((' | '.join(('', str(self._case_counter), case['title'], ' ', ' ', ' '))).strip())
                    self._test_cases.append('###%s %s\n\n' % (title_level_up, case['title']))

# Test-case processing differs depending on the template id. All processors are in case_processing module.
                case_template = '/'.join((str(self.project_path), self._template_folder, ''.join((str(case['template_id']), '.j2'))))

                if not os.path.isfile(case_template):
                    print(f"\n\nhere is no jinja template for test case template_id {case['template_id']} (case_id {case['id']}) in folder {self._template_folder}")
                else:
                    try:
                        template = self._env.get_template(case_template)
                        result = template.render(case=case, platform_name=self._platform_name).split('\r\n')
                    except Exception:
                        print(f"\n\nThere is problem with jinja template for test case template_id {case['template_id']} (case_id {case['id']}) in folder {self._template_folder}")
                        if self._print_case_structure:
                            print('\nCase structure:')
                            pprint(case)
                        result = None

                    if result:
                        for string in result:
                            self._test_cases.append(string)
                            self._test_cases.append('\n')


    def _remove_empty_chapters(self):
        next_iteration = True

        while next_iteration:
            next_iteration = False
            empty_chapter = True
            empty_chapter_title_level = 1
            string_counter = 0
            remove_from_case_list = 0

            for index in range(len(self._test_cases)-1, -1, -1):

                string_counter += 1

                if self._test_cases[index] and not self._test_cases[index].startswith('#'):
                    empty_chapter = False

                elif self._test_cases[index].startswith('#'):
                    remove_from_case_list += 1
                    title_level = len(self._test_cases[index].split(' ')[0])

                    if empty_chapter and title_level >= empty_chapter_title_level:

                        for string in range(string_counter):
                            self._test_cases.pop(index)
                        if len(self._test_cases) > 0:
                            self._std_table.pop(len(self._std_table)-remove_from_case_list)
                        remove_from_case_list -= 1

                        next_iteration = True

                    empty_chapter_title_level = title_level
                    empty_chapter = True
                    string_counter = 0


    def _make_std_table_first_row(self, columns):
        first_row = '| '
        for i, header in enumerate(self._std_table_column_headers):
            if i+1 in columns:
                first_row += self._std_table_column_headers[i] + ' | '
        first_row = first_row.strip()

        return first_row


    def _std_table_aligning(self):

        if self._add_case_id_to_case_name:
            self._std_table_column_headers = self._make_std_table_first_row([1,2,3,4,5])
            self._std_table = [self._std_table_column_headers] + self._std_table
        else:
            self._std_table_column_headers = self._make_std_table_first_row([1,3,4,5])
            self._std_table = [self._std_table_column_headers] + self._std_table

        column_widths = [0 for i in range(self._std_table[0].count('|') - 1)]
        strings = []
        max_width = 60

        for i, line in enumerate(self._std_table):
            line = line.split('|')
            line.pop(0)
            line.pop(len(line) - 1)
            strings.append(line)

            for j in range(len(strings[i])):
                strings[i][j] = strings[i][j].strip(' ')
                if len(strings[i][j]) > column_widths[j]:
                    column_widths[j] = len(strings[i][j])

        for column in range(len(column_widths)):
            if column_widths[column] > max_width:
                column_widths[column] = max_width

        self._std_table = []

        for line in strings:
            new_string = '|'
            for i, item in enumerate(line):
                new_string = ''.join((new_string, ' ', item, ' ' * (column_widths[i] - len(item)), ' ', '|'))
            self._std_table.append(new_string)

        header_separator = '|'
        for i in range(len(strings[0])):
            header_separator = ''.join((header_separator, '-' * (column_widths[i] + 2), '|'))
        self._std_table.insert(1, header_separator)

        self._std_table = ['\n# %s\n' % self._std_table_header] + self._std_table


    def _resolve_url(self):
        for i, string in enumerate(self._test_cases):
            if '![' in string:
                if not self._platform_id == self.defaults['platform_id']:
                    self._test_cases[i] = re.sub("(?<=[\]][\(])(\w*)", self._screenshots_url + "\g<1>" + '_' + self._platform_name + self._screenshots_ext, string)
                else:
                    self._test_cases[i] = re.sub("(?<=[\]][\(])(\w*)", self._screenshots_url + "\g<1>" + self._screenshots_ext, string)


    def apply(self):
        self.logger.info('Applying preprocessor')

        project_name = self._client.send_get('get_project/%s' % self._project_id)['name']

        self.logger.debug(f'Collect data from {self._testrail_url}, project {project_name}')

        project_suites = self._client.send_get('get_suites/%s' % self._project_id)

        self._collect_suites_and_sections_ids(project_suites)

        self._collect_cases(project_suites)

        self._remove_empty_chapters()

        if self._resolve_urls:
            self._resolve_url()

        self._std_table_aligning()

        if self._add_std_table and len(self._std_table) > 3:
            for line in self._std_table:
                self._test_cases.append('\n' + line)
            self._test_cases.append('\n')

        markdown_file_path = '/'.join((str(self.working_dir), self._filename))

        self.logger.debug(f'Processing Markdown file: {markdown_file_path}')

        with open(markdown_file_path, 'w', encoding="utf-8") as file_to_write:
            for string in self._test_cases:
                file_to_write.write(string)

        src_file_path = '/'.join((str(self.config['src_dir']), self._filename))
        if self._rewrite_src_file:
            copyfile(markdown_file_path, src_file_path)

        self.logger.info('Preprocessor applied')
