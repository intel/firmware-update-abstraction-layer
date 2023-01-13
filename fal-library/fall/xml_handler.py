"""
    Module that handles parsing of XML files

    Copyright (C) 2022-2023 Intel Corporation
    SPDX-License-Identifier: Apache-2.0
"""
import io
import os.path
import pathlib
import logging
import xmlschema

from typing import Dict, Union, Any
from defusedxml import DefusedXmlException, DTDForbidden, \
    EntitiesForbidden, ExternalReferenceForbidden, \
    NotSupportedError

from defusedxml.ElementTree import XMLParser, parse, ParseError
from concurrent.futures import ThreadPoolExecutor, as_completed

from .utility.file_handler import get_canonical_representation_of_path, check_path


logger = logging.getLogger(__name__)

PARSE_TIME_SECS = 5


class XmlException(Exception):
    """Class exception Module"""
    pass


class XmlHandler:
    """Class for handling XML parsing

    @param xml: XML to be parsed (either as a string or file path)
    @param is_file: False by default, True if XML to be parsed is a file
    @param schema_location: location of schema file
    """

    def __init__(self, xml: str, is_file: bool,
                 schema_location: Union[str, pathlib.Path]) -> None:
        self._is_file = is_file
        self._schema_location = schema_location
        logger.debug(f"SCHEMA LOC : {self._schema_location}")

        self._xml: str = xml
        with ThreadPoolExecutor(max_workers=1) as executor:
            tasks = {executor.submit(self._getroot, x): x for x in [xml]}

            for task in as_completed(tasks, timeout=PARSE_TIME_SECS):
                try:
                    self._root = task.result()
                except TimeoutError:
                    raise XmlException("XML Parser timed out.")

    def _validate(self, xml: str) -> Any:
        """Validates the XML file against the schema for security

        @param xml: XML contents
        @return parsed document
        @raises XmlException
        """
        logger.debug('validating XML file: {}'.format(xml))

        try:
            check_path(self._schema_location)
        except IOError as e:
            raise XmlException(f"Error with Schema file: {e}")

        try:
            parser = XMLParser(forbid_dtd=True,
                               forbid_entities=True, forbid_external=True)

            if self._is_file:
                if not os.path.exists(xml):
                    raise XmlException("XML file not found")
                parsed_doc = parse(xml, parser)
            else:
                parsed_doc = parse(io.StringIO(xml), parser)

            with open(get_canonical_representation_of_path(
                    str(self._schema_location))) as schema_file:
                schema = xmlschema.XMLSchema11(schema_file)
                schema.validate(xml)

            return parsed_doc
        except (xmlschema.XMLSchemaValidationError, ParseError,
                DefusedXmlException, DTDForbidden,
                EntitiesForbidden, ExternalReferenceForbidden,
                NotSupportedError, xmlschema.XMLSchemaParseError) as error:
            raise XmlException(f'XML validation error: {error}')

    def __repr__(self) -> str:
        return "<XmlHandler xml=" + self._xml.__repr__() +\
               ", is_file=" + self._is_file.__repr__() +\
               ", schema_location=" + self._schema_location.__repr__() + ">"

    def get_children(self, xpath: str) -> Dict[str, Any]:
        """Find all elements matching XPath from parsed XML

        @param xpath: Valid XPath expression
        @return: Values of the matched elements as a List
        @raises XmlException
        """
        children = {}
        elements = self._root.find(xpath)

        if elements is None:
            raise XmlException(f'Cannot find children at specified path: {xpath}')
        for each in elements:
            if each.text:
                children[each.tag] = each.text
            else:
                raise XmlException('Empty tag encountered. XML rejected')

        return children

    def find_element(self, xpath: str) -> Any:
        """Finds an attribute for the given key.

        @param xpath: xpath expression to find element
        @return: value of element if path exists, else None
        """
        return self._root.findtext(xpath)

    def get_attribute(self, xpath: str, attribute_name: str) -> str:
        """Get attribute value for the given path and key.

        @param xpath: path to key
        @param attribute_name: name of attribute
        @return: attribute str if found else None
        """
        logger.debug("XML get attr")
        element = self._root.find(xpath)
        if element is not None:
            return element.attrib[attribute_name]
        else:
            raise XmlException("Could not find element in get_attribute")

    def get_root_elements(self, key: str, attr: str) -> list:
        """Retrieves all elements matching the specified element and attribute
        @param key: element name
        @param attr: element's attribute name
        @return: list
        @raises: XmlException when failed to update
        """
        elements = []
        try:
            for ele in self._root.findall(key):
                val = ele.get(attr)
                elements.append(val)
            return elements
        except (XmlException, ValueError, TypeError, KeyError) as e:
            raise XmlException(f"ERROR while fetching elements from root: {e}")

    def _getroot(self, xml: str) -> Any:
        """This function validates and returns the root of the xml
        @param xml: xml contents
        @return: root path
        """
        logger.debug(f"XML : {xml}")
        return self._validate(xml).getroot()
