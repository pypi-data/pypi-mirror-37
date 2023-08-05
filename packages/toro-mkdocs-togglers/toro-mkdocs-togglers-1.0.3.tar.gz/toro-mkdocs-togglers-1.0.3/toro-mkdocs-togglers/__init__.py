import re
import markdown

from markdown import Extension
from markdown.preprocessors import Preprocessor


def makeExtension(**kwargs):
    return TogglerExtension(**kwargs)


class TogglerExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        self.heading_processor = TogglerProcessor(md)
        md.preprocessors.add('togglers', self.heading_processor, '>html_block')


class TogglerProcessor(Preprocessor):

    def __init__(self, md):
        Preprocessor.__init__(self, md)

    def run(self, lines):
        content = ""
        lineLen = len(lines)
        count = 0

        for line in lines:
            content += line
            if count < lineLen - 1:
                content += "\n"
            count += 1

        tabs_p = r'(\|{3}[ ]*".*"(?=\n))'

        toggler_p = r'(^\|{3}[\s\S]*?\|{3}[\s\S]*?[ ]{2,}[\S].*?(?=\n\n*.*?(?!\|)^[\S]))|' \
                    r'(^\|{3}[\s\S]*\|{3}[\s\S]*?[ ]{2,}[\S].*?(?=\n\n+))|' \
                    r'(^\|{3}[\s\S]*\|{3}[\s\S]*?[ ]{2,}[\S].*?(?=\n*$))'

        togglers = re.compile(toggler_p, re.MULTILINE).findall(content)

        for toggler in togglers:
            temp = ""
            for t in toggler:
                temp += t
            content = content.replace(temp, self.getTogglerHTML(tabs_p, temp))

        togglers = []
        toggler = ""
        indent = ""
        start_tabbed_toggler = False
        content_lines_num = len(content.split("\n")) -1
        count = 0
        for c in content.split("\n"):
            if not start_tabbed_toggler:
                tabbed_toggler = re.compile(r'^[ ]+\|{3}[ ]*".*"').findall(c)
                if tabbed_toggler:
                    tabbed_toggler = tabbed_toggler[0]
                    toggler += tabbed_toggler + "\n"
                    start_tabbed_toggler = True
                    indent = re.compile(r'^\s*').findall(toggler)[0]
            else:
                if c.startswith(indent + indent) or c.startswith(indent + "|||"):
                    toggler += c + "\n"

                elif c == "\n" or not c:
                    toggler += "\n"

                elif count == content_lines_num:
                    start_tabbed_toggler = False
                    temp = re.compile(r'^[ ]+\|{3}[ ]*".*"[\s\S]*?(?=\n+$)').findall(toggler)
                    if temp:
                        toggler = temp[0]
                    togglers.append(toggler)
                    toggler = ""
                    indent = ""

                elif not c.startswith(indent + indent) and not c.startswith(indent + "|||"):
                    indent_temp = re.compile(r'^\s*').findall(c)
                    if indent_temp:
                        indent_temp = indent_temp[0]
                        if len(indent_temp) > len(indent):
                            toggler += c + "\n"
                            count += 1
                            continue

                    start_tabbed_toggler = False
                    if toggler:
                        temp = re.compile(r'^[ ]+\|{3}[ ]*".*"[\s\S]*?(?=\n+$)').findall(toggler)
                        if temp:
                            toggler = temp[0]
                        togglers.append(toggler)
                        toggler = ""
                        indent = ""
            count += 1
        for toggler in togglers:
            content = content.replace(toggler, "\n" + self.getTogglerHTML(tabs_p, toggler))

        new_lines = []
        for line in content.split("\n"):
            new_lines.append(line)

        return new_lines

    def getTogglerHTML(self, tabs_p, toggler):
        indent = re.compile(r'^\s*').findall(toggler)
        without_indents = self.remove_indents(toggler)

        without_indents = self.getMainDiv(without_indents, tabs_p)

        indent = indent[0]
        if indent:
            with_indents = self.add_indents(without_indents, indent)
            return with_indents
        else:
            return without_indents

    def getMainDiv(self, toggler, tabs_p):

        # Get main tab names
        main_tabs = re.compile(tabs_p).findall(toggler)

        # If no tabs then return empty list
        if not main_tabs:
            return toggler

        number_of_tabs = len(main_tabs)
        data_names = ""
        tab_contents = []

        i = 0

        for tab in main_tabs:
            # Extract tab name
            t = re.search(r'"(.*?)"', tab).group(1)

            data_names += t + ","
            start_index = toggler.index(tab) + len(tab) + 1

            if i < number_of_tabs - 1:
                last_index = toggler.index(main_tabs[i + 1])
            else:
                last_index = len(toggler)

            # Tab contents
            tab_content = toggler[start_index:last_index]

            tab_contents.append(tab_content)
            i += 1

        data_names = data_names[:-1]
        tab_names = data_names.split(",")

        content = ""
        for i in range(len(tab_names)):
            content += self.getSubDiv(tab_names[i], tab_contents[i])

        return "\n<div class=\"toro-toggler\" data-names=\"{}\">\n\n{}\n\n</div>\n\n".format(data_names, content)

    def getSubDiv(self, tab_name, tab_content):
        tab_content = self.remove_indents(tab_content) + "\n\n"
        tab_content = self.getNestedTogglerDiv(tab_content)

        return "\n\n<div data=related-divider=\"{}\">\n\n{}\n\n</div>".format(tab_name, tab_content)

    def getNestedTogglerDiv(self, content):
        tabs_p = r'(/{3}[ ]*".*"(?=\n))'
        toggler_p = r'(^/{3}[\s\S]*?/{3}[\s\S]*?[ ]{2,}[\S].*?(?=\n\n*.*?(?!/)^[\S]))|' \
                    r'(^/{3}[\s\S]*/{3}[\s\S]*?[ ]{2,}[\S].*?(?=\n\n+))|' \
                    r'(^/{3}[\s\S]*/{3}[\s\S]*?[ ]{2,}[\S].*?(?=\n*$))'

        togglers = re.compile(toggler_p, re.MULTILINE).findall(content)
        for toggler in togglers:
            temp = ""
            for t in toggler:
                temp += t
            content = content.replace(temp, self.getTogglerHTML(tabs_p, temp))

        togglers = []
        toggler = ""
        indent = ""
        start_tabbed_toggler = False
        content_lines_num = len(content.split("\n")) - 1
        count = 0

        for c in content.split("\n"):

            if not start_tabbed_toggler:
                tabbed_toggler = re.compile(r'^[ ]+/{3}[ ]*".*"').findall(c)
                if tabbed_toggler:
                    tabbed_toggler = tabbed_toggler[0]
                    toggler += tabbed_toggler + "\n"
                    start_tabbed_toggler = True
                    indent = re.compile(r'^\s*').findall(toggler)[0]
            else:
                if c.startswith(indent + indent) or c.startswith(indent + "///"):
                    toggler += c + "\n"

                elif count == content_lines_num:
                    start_tabbed_toggler = False
                    temp = re.compile(r'^[ ]+/{3}[ ]*".*"[\s\S]*?(?=\n+$)').findall(toggler)
                    if temp:
                        toggler = temp[0]
                    togglers.append(toggler)
                    toggler = ""
                    indent = ""

                elif c == "\n" or not c:
                    toggler += "\n"

                elif not c.startswith(indent + indent) and not c.startswith(indent + "///"):
                    indent_temp = re.compile(r'^\s*').findall(c)
                    if indent_temp:
                        indent_temp = indent_temp[0]
                        if len(indent_temp) > len(indent):
                            toggler += c + "\n"
                            count += 1
                            continue

                    start_tabbed_toggler = False
                    if toggler:
                        temp = re.compile(r'^[ ]+/{3}[ ]*".*"[\s\S]*?(?=\n+$)').findall(toggler)
                        if temp:
                            toggler = temp[0]
                        togglers.append(toggler)
                        toggler = ""
                        indent = ""
            count += 1

        for toggler in togglers:
            content = content.replace(toggler, self.getTogglerHTML(tabs_p, toggler))

        return content

    def remove_indents(self, content):
        content_lines = content.split("\n")

        for line in content_lines:
            if line and line != "\n":
                indent = re.compile(r'^\s*').findall(content)
                if indent:
                    indent = indent[0]
                    indent = indent.replace("\n", "")
                    without_indents = ""

                    for c in content.split("\n"):
                        if c[:len(indent)] == indent:
                            without_indents += c[len(indent):] + "\n"
                        else:
                            without_indents += c + "\n"

                    without_indents = without_indents[:-1]
                    return without_indents

        return content

    def add_indents(self, content, indent):
        with_indent = ""
        for c in content.split("\n"):
            with_indent += indent + c + "\n"

        return with_indent


# md = markdown.Markdown(extensions=["toro-mkdocs-togglers"])
# text = """
# ||| "Tab1"
#     /// "NestedTabName1"
#         Nested Tab1 content.
#     /// "NestedTabName2"
#         Nested Tab2 content.
#
#     Tab1 content.
# ||| "Tab2"
#     Tab2 content.
#
#     dfadf
#
# ||| "Tab3"
#     Tab3 content.
# """
# print(md.convert(text))
