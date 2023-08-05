from jinja2 import contextfilter, Markup
import markdown
from pathlib import Path
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor


class Jinja2Processor(BlockProcessor):
    def test(self, parent, block):
        return block.startswith('{%') or block.startswith('{{')

    def run(self, parent, blocks):
        block = blocks.pop(0)
        sibling = self.lastChild(parent)
        if sibling is not None:
            if sibling.tail:
                sibling.tail = sibling.tail + block
            else:
                sibling.tail = block
        else:
            if parent.text:
                parent.text = parent.text + block
            else:
                parent.text = block
        return True


class IgnoreExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
                'jinja2',
                Jinja2Processor(md.parser),
                ">hashheader")


@contextfilter
def markdown2html(context, text, render=True):
    result = markdown.markdown(
            text,
            extensions=[IgnoreExtension(), 'markdown.extensions.extra'],
            output_format='html5',
            tab_length=2)
    if render:
        result = context.environment.from_string(result).render(context)
    if context.eval_ctx.autoescape:
        result = Markup(result)
    return result


def merge_dict(a, b):
    if isinstance(a, list):
        return [merge_dict(i, b) for i in a]
    return {**a, **b}


def fileglob(path, root):
    return [p.relative_to(root) for p in Path(root).glob(path)]
