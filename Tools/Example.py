import wx
import wx.richtext as rt


class RichTextFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create style stylesheet and control
        self._stylesheet = rt.RichTextStyleSheet()
        self._stylesheet.SetName('Stylesheet')

        self._style_control = rt.RichTextStyleListBox(self, 1, size=(140, 60))
        self._style_control.SetApplyOnSelection(True)
        self._style_control.SetStyleType(0)
        self._style_control.SetMargins(-5, -5)

        self.rtc.SetStyleSheet(self._stylesheet)
        self._style_control.SetRichTextCtrl(self.rtc)
        self._style_control.SetStyleSheet(self._stylesheet)

        self.sizer.Add(self.rtc, 1, flag=wx.EXPAND)
        self.sizer.Add(self._style_control)
        self.SetSizer(self.sizer)

        self._create_styles()

    def _create_styles(self) -> None:
        """
        Create styles for rich text control.
        :return: None
        """
        # Paragraph style
        stl_paragraph: rt.RichTextAttr = rt.RichTextAttr()
        stl_paragraph.SetFontSize(Numbers.paragraph_font_size)
        stl_paragraph.SetAlignment(wx.TEXT_ALIGNMENT_LEFT)
        # todo font weight and size is ignored
        stl_paragraph.SetFontWeight(wx.FONTWEIGHT_NORMAL)
        stl_paragraph.SetParagraphSpacingBefore(Numbers.paragraph_spacing)
        stl_paragraph.SetParagraphSpacingAfter(Numbers.paragraph_spacing)
        stl_paragraph.SetBackgroundColour(wx.GREEN)

        style_paragraph: rt.RichTextParagraphStyleDefinition = rt.RichTextParagraphStyleDefinition(
            Strings.style_paragraph)
        style_paragraph.SetStyle(stl_paragraph)
        style_paragraph.SetNextStyle(Strings.style_paragraph)
        self._stylesheet.AddParagraphStyle(style_paragraph)

        # Paragraph style bold
        stl_paragraph_bold: rt.RichTextAttr = rt.RichTextAttr()
        stl_paragraph_bold.SetFontSize(Numbers.paragraph_font_size_1)
        stl_paragraph_bold.SetAlignment(wx.TEXT_ALIGNMENT_LEFT)
        stl_paragraph_bold.SetFontWeight(wx.FONTWEIGHT_BOLD)
        stl_paragraph_bold.SetParagraphSpacingBefore(Numbers.paragraph_spacing_bold)
        stl_paragraph_bold.SetParagraphSpacingAfter(Numbers.paragraph_spacing_bold)
        stl_paragraph_bold.SetBackgroundColour(wx.YELLOW)

        style_paragraph_bold: rt.RichTextParagraphStyleDefinition = rt.RichTextParagraphStyleDefinition(
            Strings.style_paragraph_bold)
        style_paragraph_bold.SetStyle(stl_paragraph_bold)
        style_paragraph_bold.SetNextStyle(Strings.style_paragraph)
        self._stylesheet.AddParagraphStyle(style_paragraph_bold)

        self.rtc.SetStyleSheet(self._stylesheet)
        self._style_control.SetRichTextCtrl(self.rtc)
        self._style_control.SetStyleSheet(self._stylesheet)
        self._style_control.UpdateStyles()

    def insert_sample_text(self) -> None:
        """
        Insert sample text.
        :return: None
        """
        self.rtc.BeginParagraphStyle(Strings.style_paragraph)
        self.rtc.WriteText('Example paragraph')
        self.rtc.Newline()
        self.rtc.EndParagraphStyle()

        self.rtc.BeginParagraphStyle(Strings.style_paragraph_bold)
        self.rtc.WriteText('Example paragraph')
        self.rtc.Newline()
        self.rtc.EndParagraphStyle()

        self.rtc.BeginParagraphStyle(Strings.style_paragraph)
        self.rtc.WriteText('Example paragraph')
        self.rtc.Newline()
        self.rtc.EndParagraphStyle()

        self.rtc.LayoutContent()


class Strings:
    """
    Just constants
    """
    style_paragraph: str = 'paragraph'
    style_paragraph_bold: str = 'boldparagraph'


class Numbers:
    paragraph_font_size: int = 10
    paragraph_font_size_1: int = 20
    paragraph_spacing: int = 20
    paragraph_spacing_bold: int = 35


class MyApp(wx.App):
    """
    Main class for running the gui
    """

    def __init__(self):
        wx.App.__init__(self)
        self.frame = None

    def OnInit(self):
        self.frame = RichTextFrame(None, -1, "RichTextCtrl", size=(900, 700), style=wx.DEFAULT_FRAME_STYLE)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        self.frame.insert_sample_text()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
