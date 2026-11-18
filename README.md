# Root-Relative Line Count

This is a small, original implementation of the behavior described in
[repoScanner issue #72](https://github.com/tecnolgd/repoScanner/issues/72).

The implementation accepts a scan root and counts a file relative to that root,
rather than relative to the process's current working directory.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Usage

```powershell
python -m repo_root_line_count.cli C:\path\to\project --lc file.txt
# 3
```

An absolute `--lc` path is also accepted. Paths outside the scan root are
rejected.

## Verification

```powershell
python -m unittest discover -s tests -v
```

## Source attribution and limitations

The problem context comes from the public, MIT-licensed repoScanner issue
above. This implementation is independent and intentionally minimal; it
does not implement the rest of the repoScanner project.
