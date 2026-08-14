# Eigenholm blog instructions

Read and follow [_ARTICLE_WORKFLOW.md](_ARTICLE_WORKFLOW.md) for every request to
write, draft, research, or create an article. In particular, automatically use
the local LLM wiki at `C:\Wiki\wiki` as the research source for article topics.

The blog's design system belongs to this repository. Preserve `_quarto.yml`,
`custom.scss`, `custom-dark.scss`, and `_eigenholm-rules.scss` conventions when
creating posts.

Content lives in four sections, each with its own listing page: `posts/`
(Writing), `projects/`, `notes/`, and `replications/`. Pick the directory that
matches the kind of work before drafting; `_ARTICLE_WORKFLOW.md` defines the bar
for each one. Add the new page to `## Related reading` on the pages it connects
to, and validate with `uv run python tools/check_content.py`.
