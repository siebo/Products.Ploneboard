from Products.ATContentTypes.interface import ITextContent
from zope.interface import implements
from Products.PortalTransforms.transforms import markdown

class CommentTextContent(object):
    implements(ITextContent)

    def __init__(self, context):
        self.context = context

    def getText(self, **kwargs):
        body = self.context.getText()
        return markdown.convert(body)

    def setText(self, value, **kwargs):
        self.context.setText(value, **kwargs)

    def CookedBody(self, stx_level='ignored'):
        return self.getText()

    def EditableBody(self):
        return self.getRawText()
