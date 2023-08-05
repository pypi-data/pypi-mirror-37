from html.parser import HTMLParser
from pyno import HTML as H, TreeNode


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parent_stack = [H.doc()]

    def handle_starttag(self, tag, attrs):
        self.parent_stack.append(TreeNode(tag,**dict(attrs)))

    def handle_endtag(self, tag):
        self.parent_stack[-2].args.append(self.parent_stack.pop())

    def handle_data(self, data):
        self.parent_stack[-1].args.append(data)


def pyno_parser(text):

    parser = MyHTMLParser()
    parser.feed('<html data><head><title color="blue">Test</title></head><body><h1>Parse me!</h1></body></html>')
    return parser.parent_stack[0]


print(str(pyno_parser('<html data><head><title color="blue">Test</title></head>'
                      '<body><h1>Parse me!</h1></body></html>')))