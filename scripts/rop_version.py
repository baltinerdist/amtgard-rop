"""Single source of truth for which rulebook edition the corpus is built from."""
VERSION = "V8.08"
NAME = 'V8.08 "Spongy"'
DATE = "2026-07-25"
PRINT_OFFSET = 2          # printed page = PDF page - 2  (V8.7 was 3)
ABILITY_PAGES = range(62, 78)   # PDF pp 62..77 inclusive
FURNITURE = r'Amtgard 8\b.*|07-2\d-202\d'   # running header + date stamp (page number added by callers)
