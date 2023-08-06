from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.simplelayout.contenttypes.browser.textblock import TextBlockView


class FaqBlockView(TextBlockView):
    template = ViewPageTemplateFile('faqblock.pt')

    def is_reload(self):
        return self.request.URL.endswith('sl-ajax-reload-block-view')

    def show_limit_indicator(self):
        # show_limit_indicator was added in ftw.simplelayout version 1.22. We
        # want to use this feature if it is available, but not throw an error if
        # not.
        if getattr(super(FaqBlockView, self), 'show_limit_indicator', None):
            return super(FaqBlockView, self).show_limit_indicator()
        return False
