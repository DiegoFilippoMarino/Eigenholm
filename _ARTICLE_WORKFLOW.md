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
   Apply the code policy below when deciding what a reader sees inline.
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
- `custom.scss` and `custom-dark.scss` define the light and dark themes; the
  shared rules live in `_eigenholm-rules.scss`.
- Two typographic registers, applied consistently. **Document structure**
  (headings, article titles, listing titles) uses Source Serif 4, mixed case,
  sized above the body text. **Interface chrome** (navbar, hero, section labels,
  listing metadata, table headers, categories) uses Inter, uppercase, letter
  spaced. Body text is Inter; code uses the configured monospace fallback stack.
- Text colors must clear WCAG AA (4.5:1) against the page background. The muted
  token is the tightest one and is already at the edge, so do not lighten it.
- The editorial look is calm, minimal, readable, and research-oriented. Favor
  clear hierarchy, short sections, restrained callouts, and purposeful figures
  over decorative elements.
- `eigenholm.mplstyle` at the project root carries the figure house style: color
  cycle, spine removal, frameless legends, layout, sizes. Adopt it with one line
  in a page's first executable cell, `plt.style.use("../../eigenholm.mplstyle")`,
  and never repeat that formatting inline.

## Code in an article

Code earns inline space by carrying the argument, not by being present. The test:

> A snippet is shown iff removing it would make a claim in the prose
> unverifiable or a mechanism unclear.

Two corollaries do most of the work.

- **An equation beats its numpy restatement.** If the prose already states the
  relation, a cell that re-encodes it line for line adds nothing; fold the cell
  and let the equation carry the meaning.
- **Every number quoted in prose stays traceable.** Folded counts as traceable,
  hidden does not. This is the floor the rule cannot cross.

Mechanics:

1. **One cell, one job.** A cell either makes a claim or draws it, never both.
   Split at the point where computation ends and `plt` begins. Keep imports,
   the style line, and rng seeding in the visible cell so shown code runs top
   to bottom. Put `label` and `fig-cap` on the cell that emits the figure.
2. **Folded is the default**, set once in `_quarto.yml`. Cells that carry an
   argument opt out with `#| code-fold: false`. Give a folded cell a
   `#| code-summary` naming what it is, usually `"Plotting code"`.
3. **Never `echo: false`.** Nothing is hidden outright. A reader who wants the
   axis limits behind a figure gets them in one click, and `code-tools` plus
   `repo-actions` expose the full source of every page.
4. End a plotting cell with `plt.show()`, so a trailing expression cannot leak
   its repr into the output.

## Sections

Four content areas, each with its own listing page and its own bar for entry:

- `posts/` (**Writing**) - long-form articles and attempts at original synthesis.
- `projects/` (**Projects**) - executable artifacts: simulators, implementations,
  things that could be lifted into a repository.
- `notes/` (**Notes**) - narrower derivations and results, shorter than an article.
- `replications/` (**Replications**) - attempts to reproduce published results.
  Every entry opens with a callout naming the target numbers, the method, and the
  outcome. A failed reproduction is reported as a failure, never tuned into
  agreement.

Every page ends with a `## Related reading` section of two to four links to other
pages on the site, placed immediately before `## References`. Use relative paths
such as `../../posts/<slug>/index.qmd`.

The wiki provides subject knowledge; this repository provides the article
format, tone, theme, typography, and final published artifact.

## Boundaries

Do not edit `C:\Wiki\wiki` when writing a blog post. It is read-only source
material for this workflow. Do not change global theme/configuration files
unless the user separately requests a site-design change.
