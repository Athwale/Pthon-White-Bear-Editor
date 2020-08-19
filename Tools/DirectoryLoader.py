import glob
import os
from typing import Dict

from lxml import etree
from lxml import html
from lxml.etree import XMLSyntaxError

from Constants.Strings import Strings
from Exceptions.AccessException import AccessException
from Exceptions.UnrecognizedFileException import UnrecognizedFileException
from Resources.Fetch import Fetch
from Tools.Document.WhitebearDocumentArticle import WhitebearDocument


class DirectoryLoader:
    """
    This class loads and parses white bear web root directory. The output is a dictionary of file names + full path
    to them on the system. If the directory is not readable or writable or the files are not readable or writeable,
    AccessException is raised.
    # TODO parse css
    """

    def __init__(self):
        self._directory_path: str = ''
        self._article_documents: Dict[str, WhitebearDocument] = {}
        self._menu_documents: Dict[str, WhitebearDocument] = {}
        self._index_document = None
        # Prepare xml schemas
        self.xmlschema_index = etree.XMLSchema(etree.parse(Fetch.get_resource_path('schema_index.xsd')))
        self.xmlschema_article = etree.XMLSchema(etree.parse(Fetch.get_resource_path('schema_article.xsd')))
        self.xmlschema_menu = etree.XMLSchema(etree.parse(Fetch.get_resource_path('schema_menu.xsd')))

    def get_directory(self) -> str:
        """
        Returns the directory that is set as the website directory.
        :return: Supposed whitebear directory set in this instance.
        """
        return self._directory_path

    def get_articles(self) -> Dict[str, WhitebearDocument]:
        """
        Returns a dictionary of file names and corresponding WhitebearDocument instances of article pages.
        :return: {file name, WhitebearDocument, ...}
        """
        return self._article_documents

    def get_menus(self) -> Dict[str, WhitebearDocument]:
        """
        Returns a dictionary of file names and corresponding WhitebearDocument instances of menu pages.
        :return: {file name, WhitebearDocument, ...}
        """
        return self._menu_documents

    def get_index_page(self) -> WhitebearDocument:
        """
        Returns a WhitebearDocument instance of the index page.
        :return: a WhitebearDocument instance of the index page.
        """
        return self._index_document

    def load_directory(self, directory_path: str) -> None:
        """
        Return the selected white bear directory as a dictionary of paths to files with file names as keys.
        :param directory_path: Path to the whitebear web root directory.
        :return: None
        """
        self._directory_path = directory_path
        if self._is_white_bear_directory(self._directory_path):
            self._prepare_documents(self._directory_path)

    def _is_white_bear_directory(self, path: str) -> bool:
        """
        Checks whether chosen directory belongs to the whitebear web. The directory must be readable and writable.
        The directory must contain index.html file and this file must be a valid whitebear index file according to
        schema_index.xsd xml schema.
        :raises AccessException if the directory can not be read or written to.
        :raises FileNotFoundError if index.html is not present
        :raises IndexError if the index.html is not a whitebear index page according to xml schema.
        :param path: Path to the root of the whitebear web directory.
        :return: True if path is an accessible white bear directory
        """
        if not os.access(path, os.R_OK) or not os.access(path, os.W_OK):
            raise AccessException(Strings.exception_access)

        if not os.path.exists(os.path.join(path, 'index.html')):
            raise FileNotFoundError(Strings.exception_index + ' ' + path)
        else:
            try:
                xml_doc = html.parse(os.path.join(path, 'index.html'))
                if not self.xmlschema_index.validate(xml_doc):
                    raise IndexError(Strings.exception_not_white_bear + '\n' + str(self.xmlschema_index.error_log))
            except XMLSyntaxError as e:
                raise IndexError(Strings.exception_html_syntax_error + '\n' + str(e))
        return True

    def _prepare_documents(self, path: str) -> None:
        """
        Goes through all supposed whitebear files in a directory. Files have to be readable and writeable. Constructs a
        dictionary {file name:path to the file}.
        :param path: Path to the supposed whitebear root directory.
        :return: None
        :raises AccessException if a file are not readable or not writeable.
        :raises UnrecognizedFileException if the file can not be validated
        """
        # Check all html files in directory are readable and writable
        file: str
        for file in glob.glob(path + '/*.html'):
            file = os.path.join(path, file)
            if os.path.isfile(file):
                if not os.access(file, os.R_OK) or not os.access(file, os.W_OK):
                    raise AccessException(Strings.exception_access_html + " " + file)
                else:
                    filename: str = os.path.basename(file)
                    file_path: str = os.path.realpath(file)
                    try:
                        xml_doc = html.parse(os.path.join(path, file))
                        if self.xmlschema_article.validate(xml_doc):
                            self._article_documents[filename] = WhitebearDocument(filename, file_path,
                                                                                  WhitebearDocument.TYPE_ARTICLE,
                                                                                  self._menu_documents)
                        elif self.xmlschema_menu.validate(xml_doc):
                            self._menu_documents[filename] = WhitebearDocument(filename, file_path,
                                                                               WhitebearDocument.TYPE_MENU, None)
                        elif self.xmlschema_index.validate(xml_doc):
                            self._index_document = WhitebearDocument(filename, file_path,
                                                                     WhitebearDocument.TYPE_INDEX, None)
                        else:
                            # Skip known non editable files
                            if 'google' in filename or '404' in filename:
                                continue
                            else:
                                print(self.xmlschema_article.error_log)
                                raise UnrecognizedFileException(Strings.exception_file_unrecognized + ' ' + filename)
                    except XMLSyntaxError as e:
                        raise UnrecognizedFileException(Strings.exception_html_syntax_error + '\n' + str(e))