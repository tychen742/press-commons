# AGENTS.md - ThinkPress Commons

Shared appendix and tooling pages for ThinkPress books. Read `README.md` first.

- Pages here are canonical; books receive copies through the sync step. Do not edit synced copies inside books.
- Write pages book-neutral; put book-specific commands and cross-references in each book's wrapper.
- Follow the book-authoring skill (`~/ai_shared/skills/book-authoring/`) and the ai_shared style guide for prose and notebook conventions.
- Customize per book only through the book's `commons.yml` (`vars`, `intro`, `slots`); see "Customizing a Page per Book" in `README.md`. When a page needs a new place for book-specific content, add a slot to the page; do not fork it.

## Source Visibility

Keep `tychen742/press-commons` public (confirmed 2026-10-31) so book CI can fetch shared guides anonymously. Never add secrets, learner records, answer keys, or confidential instructor material to files or history. The hosted Commons site retains its staff access policy. Public visibility does not choose a license. Use the approved book titles in Press `docs/PLATFORM_DECISIONS.md` for per-book `commons.yml` values; keep stable repository names, IDs, and domains.
