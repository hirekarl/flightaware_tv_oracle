# python-semantic-release + commitizen

**Versions:** `python-semantic-release>=10.0` (current: 10.5.3), `commitizen>=3.29`
**Role:** semantic-release owns automated CI versioning (version bump + CHANGELOG.md
update + GitHub Release tag on merge to `main`). commitizen provides the `cz commit`
interactive CLI for crafting conventional commits locally.

---

## Key Patterns

### commitizen — interactive commit
```bash
uv run cz commit   # interactive prompt: type → scope → description → body → footer
# aliased as:  uv run cz c
```
Produces correctly formatted `type(scope): description` messages that semantic-release
will parse for version bumps.

### commitizen — preview changelog locally
```bash
uv run cz changelog --dry-run   # preview what the next release entry will look like
uv run cz changelog             # write to CHANGELOG.md
```

### semantic-release — pyproject.toml config (v10 syntax)
```toml
[tool.semantic_release]
version_variables = ["backend/__init__.py:__version__"]   # note: plural in v10
version_toml = ["pyproject.toml:project.version"]
major_on_zero = true
branch = "main"
upload_to_vcs_release = true
parse_squash_commits = true    # REQUIRED for squash-merge workflow
```
`version_variables` (plural with regex) replaces `version_variable` (singular) from v9.
`parse_squash_commits = true` is essential — without it, PSR misses version bump
signals in squashed commit messages.

### Commit → version bump mapping
| Conventional commit type | Bump |
|---|---|
| `feat` | minor |
| `fix`, `perf`, `refactor` | patch |
| `BREAKING CHANGE` footer | major |
| `docs`, `ci`, `chore`, `test`, `style` | no bump |

### CI release pipeline (two-step in v10)
```yaml
- run: uv run semantic-release version   # determine + stamp new version
- run: uv run semantic-release publish   # upload artifacts, create GitHub Release
  env:
    GH_TOKEN: ${{ secrets.GH_TOKEN }}
```
In v10, `publish` does not determine the version — run `version` first.

---

## Gotchas

- **`parse_squash_commits = true` is mandatory** for our squash-merge workflow. Without
  it, PSR reads only the squash commit's subject line, potentially missing all
  conventional commit signals from the feature branch's history.
- **v9 → v10 breaking change**: `version_variable` (singular) was renamed to
  `version_variables` (plural, list). Update any v9 configs.
- **`cz bump` vs `semantic-release version`**: Don't run `cz bump` in CI — that's
  PSR's job. Use `cz bump` only for local testing/preview.
- **`GH_TOKEN` permission**: The `automated-release` job needs `contents: write`.
  Scoped at the job level in our CI config.
- **Squash and Merge is required** (not optional) for PSR to work correctly with
  `parse_squash_commits = true`. Merge commits or rebase merges require different
  PSR configuration.
- **commitizen and PSR both write changelogs** if configured to. In our setup, PSR
  owns `CHANGELOG.md` in CI; use `cz changelog --dry-run` for local preview only.

---

## Resources

- https://python-semantic-release.readthedocs.io/en/latest/ (PSR docs, v10.5.3 — fetched 2026-06-08)
- https://commitizen-tools.github.io/commitizen/ (Commitizen docs — fetched 2026-06-08)
