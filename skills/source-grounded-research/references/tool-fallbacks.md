# Tool Fallbacks

The skill is designed to work across agents with different capabilities.

## Capability order

1. Use a connected search or browser tool to discover and open sources.
2. Use a document or file tool to inspect PDFs, spreadsheets, and local artifacts.
3. Use `fetch_sources.py` for repeatable HTML retrieval and local text capture.
4. Ask the user to provide a URL or file when the agent cannot browse.
5. If no source can be inspected, provide a research plan or clearly limited synthesis instead of pretending to have completed research.

## Degraded modes

- **Search but no page inspection:** use search only for discovery; do not cite snippets as final evidence.
- **Browser but no download:** inspect the online original and cite the online URL; do not link an inaccessible local copy.
- **Local files but no web:** research only the supplied corpus and state that the report is closed-source.
- **No web and no source files:** ask for sources or explain that verification cannot be performed.

## Failure handling

- Record failed URLs and retry only when a transient failure is plausible.
- Preserve redirects and final URLs in the source ledger.
- Treat robots, paywalls, login walls, and missing attachments as limitations.
- Never use a cached snippet, generated summary, or model memory as a substitute for an unavailable original source.

