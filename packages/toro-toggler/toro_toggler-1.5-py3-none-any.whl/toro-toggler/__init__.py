import re
import logging

from markdown import Extension
from markdown.preprocessors import Preprocessor

Logger = logging.getLogger('toro-toggler')

def makeExtension(config=None):
    return TogglerExtension(config)

class TogglerExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        self._appender = Appender()
        self.heading_processor = TogglerProcessor(md, self._appender)
        md.preprocessors.add('toggler', self.heading_processor, '>html_block')



class Appender(object):
    def process(self, html, safe=False):
        return '\n\n'+html+'\n\n'



class Divider(object):
    def __init__(self, start, md):
        self._start = start
        self._end = -1
        self._name = "Content"
        self._md = md
        self._related_divider = None

    def get_related_divider(self):
        return self._related_divider

    def set_related_divider(self, related_divider):
        if type(related_divider) == unicode or type(related_divider) == str:
            self._related_divider = related_divider
        else:
            raise Exception("Invalid value for related divider")

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        if type(new_name) == unicode or type(new_name) == str:
            self._name = new_name
        else:
            raise Exception("Invalid value for name")

    def get_start(self):
        return self._start

    def set_start(self, new_start):
        if type(new_start) == unicode or type(new_start) == str:
            self._start = new_start
        else:
            raise Exception("Invalid value for start")

    def get_end(self):
        return self._end

    def set_end(self, new_end):
        if type(new_end) == int:
            self._end = new_end
        else:
            raise Exception("Invalid value for end")

    def handle(self, lines):
        start_line = lines.pop(self._start)
        start_divider = "<div" + (
            (" data-related-divider=\"" + self._related_divider + "\"") if self._related_divider else "") + ">"
        if self._start == self._end:
            lines.insert(self._start, self._md.process(start_divider + '</div>'))
        else:
            lines.insert(self._start, self._md.process(start_divider) + '\n' + start_line)
            lines.pop(self._end)
            lines.insert(self._end, self._md.process('</div>'))


class TogglerContainer(object):
    def __init__(self, md):
        self._start = -1
        self._end = -1
        self._parent = None
        self._children = []
        self._dividers = []
        self._md = md


    def get_start(self):
        return self._start

    def set_start(self, new_start):
        if type(new_start) == int:
            self._start = new_start
        else:
            raise Exception("Invalid value for start")

    def get_end(self):
        return self._end

    def set_end(self, new_end):
        if type(new_end) == int:
            self._end = new_end
        else:
            raise Exception("Invalid value for end")

    def get_parent(self):
        return self._parent

    def set_parent(self, new_parent):
        if type(new_parent) == TogglerContainer:
            self._parent = new_parent
        else:
            raise Exception("Invalid value for parent")

    def add_divider(self, divider):
        if type(divider) == Divider:
            self._dividers.append(divider)
        else:
            raise Exception("Invalid value for divider")

    def get_current_divider(self):
        divider_length = len(self._dividers)
        if divider_length != 0:
            current = self._dividers[divider_length - 1]
            if current and current.get_end() == -1:
                return current
        return None

    def add_child(self, child):
        if type(child) == TogglerContainer:
            self._children.append(child)
        else:
            raise Exception("Invalid value for child")

    def is_started(self):
        return self._start != -1

    def handle(self, lines):
        div_names = []
        for div in self._dividers:
            div_names.append(div.get_name())
            div.handle(lines)

        lines.pop(self._start)

        line = self._md.process('<div class=\"toro-toggler\" data-names=\"' + ','.join(map(str, div_names)) +
                                "\">")

        lines.insert(self._start, line)

        lines.pop(self._end)
        lines.insert(self._end, self._md.process('</div>'))

        for child in self._children:
            child.handle(lines)

class TogglerProcessor(Preprocessor):
    def __init__(self, md, appender):
        Preprocessor.__init__(self, md)
        self._appender = appender

    start_toggler_pattern = re.compile('^\[start-toggler\]\s*(?!(.))')
    end_toggler_pattern = re.compile('^\[end-toggler\]\s*(?!(.))')
    divider_pattern = re.compile('^\!\[{1}(?P<name>[^\[\]]+)\]{1}\s*$')
    page_divider_pattern = re.compile('^\!\[{2}(?P<name>[^\[\]]+)\]{2}'
                                      '(?:>\[{1}(?P<related_divider>[^\[\]]+)\]{1}){0,1}\s*$')
    whitespace_pattern = re.compile('[\s]+')
    def run(self, lines):
        containers = self.process_lines(lines)

        for container in containers:
            container.handle(lines)

        newLines = []
        for i, line in enumerate(lines):
            if "\n" in line:
                innerLines = line.split('\n')
                for innerLine in innerLines:
                    newLines.append(innerLine)
            else:
                newLines.append(line)
        return newLines

    def process_lines(self, lines):
        containers = []
        container = TogglerContainer(self._appender)
        for i, line in enumerate(lines):
            if self.start_toggler_pattern.match(line):
                if container.is_started():
                    container = self.create_child(container)
                container.set_start(i)
            elif self.end_toggler_pattern.match(line) and container.is_started():

                container.set_end(i)
                divider = container.get_current_divider()
                if divider:
                    divider.set_end(i-1)

                if container.get_parent():
                    container = container.get_parent()
                else:
                    containers.append(container)
                    container = TogglerContainer(self._appender)
            elif container.is_started():
                if self.whitespace_pattern.match(line) or not line:
                    continue

                divider = container.get_current_divider()
                if not divider:
                    divider = Divider(i, self._appender)
                    container.add_divider(divider)

                divider_match = self.divider_pattern.match(line)
                page_divider_match = self.page_divider_pattern.match(line)
                if divider_match:
                    divider.set_end(i)
                    divider.set_name(divider_match.groupdict().get('name'))
                elif page_divider_match:
                    divider_name = page_divider_match.groupdict().get('name')
                    related_divider = page_divider_match.groupdict().get('related_divider')
                    if not related_divider:
                        related_divider = divider_name
                    divider.set_end(i)
                    divider.set_name(divider_name)
                    divider.set_related_divider(related_divider)

        return containers

    def create_child(self, parent):
        inner_child = TogglerContainer(self._appender)
        inner_child.set_parent(parent)
        parent.add_child(inner_child)
        return inner_child





# md = markdown.Markdown(extensions=["toro-toggler"])
# print("\n")
# print(md.convert("# Architecture\nheheehehe\n[toggler]\nOnce you've completed all those steps, the new file will be opened automatically and a blank canvas is presented. Now \rfor creating the states.\n![1]\nwow\n![2]\n\nhello"))
# print(md.convert("[toggler]\nhello"))