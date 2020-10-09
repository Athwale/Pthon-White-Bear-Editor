import wx

from Constants.Constants import Numbers
from Constants.Constants import Strings


class BaseImage:
    """
    Base class for AsideImage and ImageInText.
    """

    def __init__(self, title: str, image_alt: str, original_image_path: str, thumbnail_path: str, full_filename: str,
                 thumbnail_filename: str):
        """
        Constructor for a base image instance.
        :param title: html title of the link element.
        :param image_alt: html alt description of the img element.
        :param original_image_path: full disk path to the original size image.
        :param thumbnail_path: full path to the thumbnail image.
        :param full_filename: file name of the full image
        :param thumbnail_filename: file name of the thumbnail image
        """
        self._link_title = title
        self._link_title_error_message: str = ''
        self._image_alt = image_alt
        self._image_alt_error_message: str = ''
        self._original_image_path = original_image_path
        self._thumbnail_path = thumbnail_path
        self._full_filename = full_filename
        self._thumbnail_filename = thumbnail_filename
        self._image = None
        self._status_color = None

    def seo_test_self(self) -> bool:
        """
        SEO test self for alt and link title. If the image and thumbnail is not accessible on disk, set a special
        warning image.
        :return: True if test is ok, False otherwise
        """
        # Disk paths have to be checked by the sub classes.
        # Clear all error before each retest
        self._link_title_error_message = ''
        self._image_alt_error_message = ''
        self._status_color = wx.NullColour

        result = True
        # Check article image link title
        if len(self._link_title) < Numbers.article_image_title_min or len(
                self._link_title) > Numbers.article_image_title_max:
            self._link_title_error_message = Strings.seo_error_link_title_length
            result = False

        if self._link_title == Strings.label_article_image_link_title:
            self._link_title_error_message = Strings.seo_error_default_value
            result = False

        # Check article image alt
        if len(self._image_alt) < Numbers.article_image_alt_min or len(
                self._image_alt) > Numbers.article_image_alt_max:
            self._image_alt_error_message = Strings.seo_error_image_alt_length
            result = False

        if self._image_alt == Strings.label_article_image_alt:
            self._image_alt_error_message = Strings.seo_error_default_value
            result = False

        if not result:
            self._status_color = wx.RED
        return result

    def get_link_title(self) -> (str, str):
        """
        Return the link title of the image and error to display in gui if there is one.
        :return: Return the link title of the image item and error to display in gui if there is one.
        """
        return self._link_title, self._link_title_error_message

    def get_image_alt(self) -> (str, str):
        """
        Return the image alt description and error to display in gui if there is one.
        :return: Return the image alt description and error to display in gui if there is one.
        """
        return self._image_alt, self._image_alt_error_message

    def get_original_image_path(self) -> str:
        """
        Return the original image full disk path.
        :return: Return the original image full disk path, None if inaccessible.
        """
        return self._original_image_path

    def get_thumbnail_image_path(self) -> str:
        """
        Return the thumbnail image full disk path.
        :return: Return the thumbnail image full disk path, None if inaccessible.
        """
        return self._thumbnail_path

    def get_thumbnail_filename(self) -> str:
        """
        Return the thumbnail image file name.
        :return: Return the thumbnail image filename.
        """
        return self._thumbnail_filename

    def get_full_filename(self) -> str:
        """
        Return the full image file name.
        :return: Return the full image filename.
        """
        return self._full_filename

    def get_image(self) -> wx.Image:
        """
        Return the image as wx image instance.
        :return: Return the image as wx image instance.
        """
        return self._image

    def get_status_color(self) -> wx.Colour:
        """
        Return the status color of this image. White if ok, Red if SEO check failed.
        :return: Return the status color of this image. White if ok, Red if SEO check failed.
        """
        return self._status_color

    def __str__(self) -> str:
        return "Base image: original: {}, thumbnail: {}, title: {}, alt: {}".format(self._original_image_path,
                                                                                    self._thumbnail_path,
                                                                                    self._link_title,
                                                                                    self._image_alt)