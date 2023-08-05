import re
from mistune import Markdown, Renderer, InlineGrammar, InlineLexer
from munch import Munch

def render(content, extensions):
    renderer = KookiRenderer(extensions)
    markdown = KookiMarkdown(renderer=renderer)
    return markdown(content)


class KookiInlineGrammar(InlineGrammar):

    criticmarkup_deletion = re.compile(r'^{--(?=\S)([\s\S]*?\S)--}')
    criticmarkup_substitution = re.compile(r'^{~~(?=\S)([\s\S]*?\S)~>(?=\S)([\s\S]*?\S)~~}')
    criticmarkup_comment = re.compile(r'^{>>(?=\S)([\s\S]*?\S)<<}')
    criticmarkup_highlight = re.compile(r'^{==(?=\S)([\s\S]*?\S)==}{>>(?=\S)([\s\S]*?\S)<<}')
    criticmarkup_addition = re.compile(r'^{\+\+(?=\S)([\s\S]*?\S)\+\+}')
    text = re.compile(r'^[\s\S]+?(?=[\\<!\[_*`~{}]|https?://| {2,}\n|$)')


class KookiInlineLexer(InlineLexer):

    default_rules = [
        'escape', 'inline_html', 'autolink', 'url',
        'footnote', 'link', 'reflink', 'nolink',
        'double_emphasis', 'emphasis', 'code',
        'criticmarkup_addition', 'criticmarkup_deletion',
        'criticmarkup_substitution', 'criticmarkup_comment',
        'criticmarkup_highlight', 'linebreak',
        'strikethrough', 'text',
    ]

    def __init__(self, renderer, **kwargs):
        rules = KookiInlineGrammar()
        super(KookiInlineLexer, self).__init__(renderer, rules, **kwargs)

    def output_criticmarkup_addition(self, m):
        text = m.group(1)
        return self.renderer.criticmarkup_addition(text)

    def output_criticmarkup_deletion(self, m):
        text = m.group(1)
        return self.renderer.criticmarkup_deletion(text)

    def output_criticmarkup_substitution(self, m):
        text = m.group(1)
        substitution = m.group(2)
        return self.renderer.criticmarkup_substitution(text, substitution)

    def output_criticmarkup_comment(self, m):
        text = m.group(1)
        return self.renderer.criticmarkup_comment(text)

    def output_criticmarkup_highlight(self, m):
        text = m.group(1)
        comment = m.group(2)
        return self.renderer.criticmarkup_highlight(text, comment)


class KookiMarkdown(Markdown):

    def __init__(self, renderer, **kwargs):
        if 'inline' not in kwargs:
            kwargs['inline'] = KookiInlineLexer(renderer)
        super(KookiMarkdown, self).__init__(renderer, **kwargs)


def catch_errors(func):
    def callback(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return ''
    return callback


class KookiRenderer(Renderer):
    
    data = Munch()
    
    @classmethod
    def clean(cls):
        cls.data = Munch()

    def __init__(self, extensions, **kwargs):
        self.extensions = extensions
        super(KookiRenderer, self).__init__(**kwargs)

    def block_quote(self, text):
        return self.extensions.__block_quote__(renderer=KookiRenderer.data, text=text)

    def block_html(self, html):
        return self.extensions.__block_html__(renderer=KookiRenderer.data, html=html)

    def inline_html(self, html):
        return self.extensions.__inline_html__(renderer=KookiRenderer.data, html=html)

    def header(self, text, level, raw):
        return self.extensions.__header__(renderer=KookiRenderer.data, text=text, level=level, raw=raw)

    def hrule(self):
        return self.extensions.__hrule__(renderer=KookiRenderer.data)

    def list(self, body, ordered):
        return self.extensions.__list__(renderer=KookiRenderer.data, body=body, ordered=ordered)

    def list_item(self, text):
        return self.extensions.__list_item__(renderer=KookiRenderer.data, text=text)

    def paragraph(self, text):
        return '{}\n\n'.format(self.extensions.__paragraph__(renderer=KookiRenderer.data, text=text))

    def table(self, header, body):
        return self.extensions.__table__(renderer=KookiRenderer.data, header=header, body=body)

    def table_row(self, content):
        return self.extensions.__table_row__(renderer=KookiRenderer.data, content=content, placeholder=False)

    def table_cell(self, content, **flags):
        return self.extensions.__table_cell__(renderer=KookiRenderer.data, content=content, placeholder=False, **flags)

    def link(self, link, title, content):
        return self.extensions.__link__(renderer=KookiRenderer.data, link=link, title=title, content=content)

    def autolink(self, link, is_email=False):
        return self.extensions.__autolink__(renderer=KookiRenderer.data, link=link, is_email=is_email)

    def block_code(self, code, language):
        return self.extensions.__block_code__(renderer=KookiRenderer.data, code=code, language=language)

    def codespan(self, text):
        return self.extensions.__codespan__(renderer=KookiRenderer.data, text=text)

    def double_emphasis(self, text):
        return self.extensions.__double_emphasis__(renderer=KookiRenderer.data, text=text)

    def emphasis(self, text):
        return self.extensions.__emphasis__(renderer=KookiRenderer.data, text=text)

    def image(self, src, title, alt_text):
        return self.extensions.__image__(renderer=KookiRenderer.data, src=src, title=title, alt_text=alt_text)

    def strikethrough(self, text):
        return self.extensions.__strikethrough__(renderer=KookiRenderer.data, text=text)

    def text(self, text):
        return self.extensions.__text__(renderer=KookiRenderer.data, text=text)

    def linebreak(self):
        return self.extensions.__linebreak__(renderer=KookiRenderer.data)

    def newline(self):
        return self.extensions.__newline__(renderer=KookiRenderer.data)

    def footnote_ref(self, key, index):
        return self.extensions.__footnote_ref__(renderer=KookiRenderer.data, key=key, index=index)

    def footnote_item(self, key, text):
        return self.extensions.__footnote_item__(renderer=KookiRenderer.data, key=key, text=text)

    def footnotes(self, text):
        return self.extensions.__footnotes__(renderer=KookiRenderer.data, text=text)

    @catch_errors
    def criticmarkup_addition(self, text):
        return self.extensions.__criticmarkup_addition__(renderer=KookiRenderer.data, text=text)

    @catch_errors
    def criticmarkup_deletion(self, text):
        return self.extensions.__criticmarkup_deletion__(renderer=KookiRenderer.data, text=text)

    @catch_errors
    def criticmarkup_substitution(self, text, substitution):
        return self.extensions.__criticmarkup_substitution__(renderer=KookiRenderer.data, text=text, substitution=substitution)

    @catch_errors
    def criticmarkup_comment(self, text):
        return self.extensions.__criticmarkup_comment__(renderer=KookiRenderer.data, text=text)

    @catch_errors
    def criticmarkup_highlight(self, text, comment):
        return self.extensions.__criticmarkup_highlight__(renderer=KookiRenderer.data, text=text, comment=comment)
