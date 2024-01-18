from __future__ import annotations
from html.parser import HTMLParser
from typing import Dict, List, Union

from pathlib import Path
import streamlit as st

from .logger import logger


class HTMLElement:
    element: str
    classes: Union[None, List[str]]
    attributes: Union[None, Dict[str, str]]
    id: Union[None, str]
    content: Union[None, str, List[HTMLElement]]


    def __init__(self
                 , element_type: str
                 , classes: Union[None, List[str]] = None
                 , attributes: Union[None, Dict[str, str]] = None
                 , id: Union[None, str] = None
                 , content: Union[None, str, List[HTMLElement]] = None
                 ) -> None:
        self.element = element_type
        self.classes = classes
        self.attributes = attributes
        self.id = id
        self.content = content


    def __str__(self) -> str:
        element = self.element if self.element else ""
        classes = f' class="{" ".join(self.classes)}"' if self.classes else ''
        id = f' id="{self.id}"' if self.id else ''

        if self.attributes:
            attribute_list = [f'{attribute}="{value}"' for attribute, value in self.attributes.items()]
            attributes = f' {" ".join(attribute_list)}'
        else:
            attributes = f''
        if not self.content:
            content = ''
        else:
            content = ''.join(str(element) for element in self.content)


        return f'<{element}{id}{classes}{attributes}>{content}</{element}>'


    def with_id(self, id: str) -> HTMLElement:
        self.id = id
        return self
    

    def with_class(self, class_name: str) -> HTMLElement:
        self.classes = [class_name]
        return self
    

    def with_classes(self, classes: List[str]) -> HTMLElement:
        self.classes = classes
        return self
    

    def with_attributes(self, attributes: Dict[str, str]) -> HTMLElement:
        self.attributes = attributes
        return self
    

    def with_content(self, content: Union[str, List[HTMLElement]]) -> HTMLElement:
        self.content = content
        return self
    

    @classmethod
    def _from_str(cls, string: str) -> HTMLElement:
        """
        given a valid html string, parse it into an HTMLElement
        """
        _parser.feed(string)
        return _parser.element
    

    @classmethod
    def from_template(cls, template: HTMLTemplate, *args, **kwargs) -> HTMLElement:
        """
        create a new html element from an incomplete template and arbitrary template arguments
        """
        return cls._from_str(template.fill(*args, **kwargs))


class HTMLTemplate:
    """
    store an unfinished html template
    """
    prototype: str
    def __init__(self, prototype: str) -> None:
        self.prototype = prototype


    @classmethod
    @st.cache_data(ttl=3600)
    def load_template(cls, template_path: Union[str, Path]) -> HTMLTemplate:
        """
        load the template stored in a given path and return a new HTMLTemplate
        """
        with open(template_path, "r") as template_file:
            result = HTMLTemplate(template_file.read())

        return result


    def fill(self, *args: str, **kwargs: str) -> HTMLElement:
        """
        fill the template with the given arguments and return a valid html element from it
        """
        return HTMLElement._from_str(self.prototype.format(*args, **kwargs))


class HTMLStackParser(HTMLParser):
    stack: List[HTMLElement] = []
    element: Union[None, HTMLElement] = None

    def __init__(self
                 , *
                 , convert_charrefs: bool = True
                 ) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.stack = []
        self.element = None


    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        logger.debug(f"found tag: {tag}")
        logger.debug(f"attributes found: {attrs}")
        new_element = HTMLElement(tag, content=[], attributes={})
        for html_tag, value in attrs:
            if html_tag == "class":
                new_element.classes = [value]
            elif html_tag == "id":
                new_element.id = value
            else:
                new_element.attributes[html_tag] = value
            
        self.stack.append(new_element)


    def handle_data(self, data: str) -> None:
        if not data == '\n':
            logger.debug(f"found data: {data}")
            self.stack[-1] = self.stack[-1].with_content(data)


    def handle_endtag(self, tag: str) -> None:
        logger.debug(f"found endtag: {tag}")
        last_element = self.stack.pop()
        if not self.stack:
            self.element = last_element
        else:
            self.stack[-1].content.append(last_element)
    

_parser = HTMLStackParser()