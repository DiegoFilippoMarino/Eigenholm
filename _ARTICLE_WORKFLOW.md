# Writing articles from the personal LLM wiki

This repository is the publishing home for Eigenholm, a Quarto technical blog.
The personal LLM wiki at `C:\Wiki\wiki` is the default research source for
articles requested in this repository.

## When asked to create an article

Treat a request such as `Create an article about X` as a request to create a
new draft post, using the wiki as the starting point without requiring the user
to repeat its location.

1. Find the relevant wiki material. Search `C:\Wiki\wiki` with `rg` before
   drafting; begin with `concepts/`, then follow the concept's links into
   `sources/`, `decisions/`, `projects/`, and MOCs as needed. Read the source
   notes that substantiate the article's claims.
2. Synthesize; do not copy the wiki's prose wholesale. Preserve technical
   precision, distinguish established facts from interpretation, and retain
   citations or primary-source links where the wiki supplies them. If the wiki
   does not contain enough material, say so rather than inventing details.
3. Create `posts/<kebab-case-topic>/index.qmd`. Use `posts/_template.qmd` as
   the front-matter and Quarto-markup reference. Set a useful title,
   one-sentence description, current date, and focused categories. Keep
   `draft: true` unless the user explicitly asks to publish.
4. Write for a technically curious reader: start with the motivating problem,
   build intuition before formalism, then add equations, small examples, or
   code only when they clarify the idea. End with limitations, trade-offs, or
   practical takeaways. Do not leave template placeholders in the post.
5. Use standard Quarto features already supported by this site (KaTeX math,
   labelled figures/tables/equations, callouts, and bibliography when needed).
   Add assets next to the post and use descriptive alt text. Do not introduce
   page-level styling, inline CSS, or replacement fonts/colors.
   For numbered equations, put a Quarto label such as `{#eq-attention}` after
   the closing `$$` and reference it as `@eq-attention`. Never put LaTeX
   `\tag{...}` inside an equation: Quarto generates the number, and combining
   both systems produces duplicate equation tags.
6. Run `uv run python tools/check_content.py`, then render the complete site
   with Quarto and fix every validation or rendering error.
   Report the created path, the wiki notes consulted, and anything that needs
   the author's review.

## Site design is owned by this repository

Keep the visual system defined here:

- `_quarto.yml` controls the Quarto website and HTML behavior.
- `custom.scss` and `custom-dark.scss` define the light and dark themes.
- Headings use Source Serif 4; body text uses Inter; code uses the configured
  monospace fallback stack.
- The editorial look is calm, minimal, readable, and research-oriented. Favor
  clear hierarchy, short sections, restrained callouts, and purposeful figures
  over decorative elements.

The wiki provides subject knowledge; this repository provides the article
format, tone, theme, typography, and final published artifact.

## Boundaries

Do not edit `C:\Wiki\wiki` when writing a blog post. It is read-only source
material for this workflow. Do not change global theme/configuration files
unless the user separately requests a site-design change.
