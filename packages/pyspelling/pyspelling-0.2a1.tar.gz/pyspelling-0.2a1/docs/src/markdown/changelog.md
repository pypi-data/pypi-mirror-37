# Changelog

## 0.2.0a1

- **NEW**: Better filters (combine filters and parsers into just filters).
- **NEW**: Drop Python 2 support.
- **NEW**: Better Python encoding detection.
- **NEW**: Better HTML encoding detection.
- **NEW**: Drop `file_extensions` option and `parser` option.
- **NEW**: Filters no longer define file extensions. Sources must specify a wildcard path that matches desired files.
- **NEW**: Drop regular expression support for sources.
- **NEW**: Drop raw filter.

## 0.1.0a3

- **NEW**: Add JavaScript parser.

## 0.1.0a2

- **NEW**: Add option to group consecutive Python comments.
- **FIX**: Properly return error.
- **FIX**: Only retry with default encoding if exception thrown was a `UnicodeDecodeError`.

## 0.1.0a1

- **NEW**: Initial alpha release.
