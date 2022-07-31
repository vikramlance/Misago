# `create_markdown_hook`

```python
from misago.richtext.hooks import create_markdown_hook

create_markdown_hook.call_action(
    action: CreateMarkdownAction,
    context: Context,
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
)
```

A synchronous filter for the function used to create `mistune.Markdown` instance to use for parsing markup.

Returns `mistune.Markdown` instance.


## Required arguments

### `action`

```python
def create_markdown_action(
    context: Context,
    block: BlockParser,
    inline: InlineParser,
    plugins: List[MarkdownPlugin],
) -> Markdown:
    ...
```

Next filter or built-in function used to create new post in the database.


### `context`

```python
Optional[Context]
```

A dict with GraphQL query context.


### `block`

```python
BlockParser
```

An instance of `BlockParser` to use. Defaults to `mistune.BlockParser`.

### `inline`

```python
InlineParser
```

An instance of `InlineParser` to use. Defaults to `mistune.InlineParser(mistune.AstRenderer())`.


### `plugins`

```python
List[Callable[[Markdown], None]]
```

List of callables accepting single argument, an instance of `mistune.Markdown`.