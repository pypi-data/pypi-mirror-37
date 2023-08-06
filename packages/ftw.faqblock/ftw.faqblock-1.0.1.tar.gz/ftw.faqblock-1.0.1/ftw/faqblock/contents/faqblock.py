from ftw.faqblock.contents.interfaces import IFaqBlock
from ftw.simplelayout.contenttypes.contents.textblock import ITextBlockSchema
from ftw.simplelayout.contenttypes.contents.textblock import TextBlock
from ftw.simplelayout.contenttypes.contents.textblock import TextBlockActions
from ftw.simplelayout.contenttypes.contents.textblock import TextBlockModifier
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from zope import schema
from zope.i18nmessageid import Message
from zope.interface import alsoProvides
from zope.interface import implements


class IFaqBlockSchema(ITextBlockSchema):
    """Faq block for simplelayout
    """

    title = schema.TextLine(
        title=Message(u'label_title',
                      domain='ftw.simplelayout',
                      default=u'Title'),
        required=True)

    form.omitted('show_title')
    form.order_before(title='*')


alsoProvides(IFaqBlockSchema, IFormFieldProvider)


class FaqBlock(TextBlock):
    implements(IFaqBlock)


class FawBlockModifier(TextBlockModifier):
    pass


class FaqBlockActions(TextBlockActions):
    pass
