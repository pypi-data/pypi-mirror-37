from ftw.faqblock.contents.interfaces import IFaqBlock
from ftw.simplelayout.contenttypes.contents.textblock import ITextBlockSchema
from ftw.simplelayout.contenttypes.contents.textblock import TextBlock
from ftw.simplelayout.contenttypes.contents.textblock import TextBlockActions
from ftw.simplelayout.contenttypes.contents.textblock import TextBlockModifier
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.interface import implements


class IFaqBlockSchema(ITextBlockSchema):
    """Faq block for simplelayout
    """


alsoProvides(IFaqBlockSchema, IFormFieldProvider)


class FaqBlock(TextBlock):
    implements(IFaqBlock)


class FawBlockModifier(TextBlockModifier):
    pass


class FaqBlockActions(TextBlockActions):
    pass
