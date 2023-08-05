"""
Create a html document and it's components programatically 
with python.

Usage:
>> d = Document("This is an Html Page")
>> d.section()
>> d.div()
>> d.paragraph()
>> d.header()
>> d.table()
>> d.image()
>> d.url()
"""
__tag__ = "</>"
class Document:
    # Document Attributes
    _document = ""
    _title   = ""
    def __init__(self, title, theme='default'):
        _document = self.create_document(title=title)
        return

    def create_document(self, title=""):
        """
        Create the html document with the <head> and <body>
        including the supplied style classes
        """
        self._title = title
        self._document = "<html>\
                            <head>\
                            <title>%s<\title>\
                            </head>\
                            <body>\
                            </body>\
                          <html>" % self._title   

    def add_header(self):
        '''
        Creates the <header> tag for the document
        Meta Information is added.
        '''
        # Ensure single header
        return

    def add_footer(self):
        '''
        Creates the <footer> tag for the document
        Meta Information and copyrights are included here.
        '''
        # Ensure single footer 
        return

    def add_section(self):
        '''
        Creates the <section> tags for grouping content together.
        '''
        return

    def add_heading(self, level=1):
        '''
        Creating the <h1> tag by default. Parse the user supplied
        tag_level to create the tag.
        '''
        return

    def add_paragraph(self, text):
        '''
        Creates the <p> tag using the style classes.
        '''
        content = "<p>\
                     %s\
                   </p>" % text
        self._append(content)
        return 

    def add_img(self, src="."):
        '''
        Creates the <img> tag with the user defined source tag
        '''
        return

    def add_table(self):
        '''
        Creates the <table> block with the column headers
        and the column data info.
        '''

    def add_line(self):
        '''
        Creates the <hr> tag adding a horizontal rule to the document
        '''
        return

    def add_break(self):
        '''
        Creates the <br/> tag adding a ine break in the document
        '''
        return

    def add_url(self, text="", url=""):
        '''
        Creates a hyperlink from and adds to the document.
        '''
        return

    def add_html(self):
        '''
        Allows the user to add some custom html code to the document
        beyond the creativity of this library.
        '''
        return

    def _append(self, content, append=True, insertAtTop=False, split_tag=""):
        '''
        Smart parser for parsing an html text block and inserting
        a block in the document 
        '''
        if split_tag == "":
            split_tag = "</body>"
        if insertAtTop:
            split_tag = "<body>"
        doc_above, doc_before = self._document.split(split_tag)
        self._document = "%s%s%s%s" % (doc_above, content, split_tag, doc_before)
        return

if __name__=="__main__":
    exit
