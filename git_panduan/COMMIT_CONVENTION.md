# Commit Message Convention

Based on [Conventional Commits](https://www.conventionalcommits.org/), adapted for solo/small-team AI & data projects.

## Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

| Type       | Use for                                              |
|------------|-------------------------------------------------------|
| `feat`     | A new feature                                        |
| `fix`      | A bug fix                                             |
| `docs`     | Documentation only changes                            |
| `style`    | Formatting, missing semicolons, no logic change       |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                                |
| `test`     | Adding or updating tests                                |
| `chore`    | Maintenance, dependency bumps, tooling, config          |
| `ci`       | CI/CD pipeline changes                                   |

## Rules

1. **One logical change per commit.** If you touched two unrelated things, that's two commits (and ideally two PRs).
2. **Imperative, present tense.** `add`, not `added` or `adds`. Think "this commit will ___".
3. **No period at the end of the subject line.**
4. **Subject line ≤ 72 characters.** Put extra detail in the body.
5. **Scope is optional but recommended** — lowercase, names the affected module (e.g. `dashboard`, `pipeline`, `agent`).
6. **Body explains *what* and *why*, not *how*.** The diff already shows how.

## Footers

- **Breaking change:**
  ```
  BREAKING CHANGE: <description of what breaks and how to migrate>
  ```
- **Pair programming / co-authored commit:**
  ```
  Co-authored-by: Full Name <email@example.com>
  ```
  (Blank line required before this footer.)
- **Linking an issue:**
  ```
  Closes #12
  ```

## Examples

```
feat(dashboard): add isolation forest anomaly detection

fix(pipeline): handle missing values in transaction dataset

docs(readme): add streamlit deployment instructions

refactor(agent): simplify langchain sql query builder

chore(deps): bump streamlit to 1.38.0

test(pipeline): add pytest coverage for null-handling edge cases
```
