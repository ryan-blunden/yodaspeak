# Coding Workflow

For every coding, debugging, refactoring, or code-review task:

1. Understand the request before editing.
2. Inspect the repository and search for related code, tests, configuration, and conventions.
3. Read only the files needed to understand the existing implementation.
4. Form a short plan, then make the smallest correct change.
5. Follow existing architecture, naming, patterns, and style. Verify APIs and behavior in the codebase; do not invent them.
6. Inspect the diff for mistakes and unintended changes.
7. Run the most relevant available tests, type checks, linters, or build commands.
8. Investigate command failures using their actual output; do not guess.

If the request is ambiguous or materially different approaches exist, ask before making a large or destructive change.

## Context Discipline

- Search first, using targeted queries for symbols, strings, types, imports, tests, and call sites.
- Do not read unrelated files, large directories, or broad context without a specific reason.
- Do not reopen files whose relevant contents are already known.
- For large tasks, work incrementally and validate each step.

## Skills

For coding tasks, load and follow the coding-guidelines skill when it is available.

Repository instructions and existing code conventions take precedence over generic assumptions.

## Working Style

- Work quickly in small, verified steps.
- Keep responses concise, clear, and high-signal.
