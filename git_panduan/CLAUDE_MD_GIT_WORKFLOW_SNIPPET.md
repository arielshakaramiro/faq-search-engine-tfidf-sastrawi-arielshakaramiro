<!--
Paste this section into the CLAUDE.md of any repo (or your global
~/.claude/CLAUDE.md if you want it applied everywhere by default).
It tells Claude Code to always branch + PR instead of pushing to main,
and to follow the commit convention automatically.
-->

## Git Workflow

Always follow this workflow when making changes, no matter how small:

1. **Never commit directly to `main`.** Start by creating a branch:
   ```
   git checkout -b <type>/<short-description>
   ```
   Examples: `feat/isolation-forest`, `fix/null-handling`, `docs/setup-guide`

2. **Commit using Conventional Commits format** (see COMMIT_CONVENTION.md):
   ```
   <type>(<scope>): <description>
   ```
   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`.
   One logical change per commit. Imperative mood, no trailing period.

3. **Push the branch and open a PR into `main`**, using the repo's PR template:
   ```
   git push origin <branch-name>
   gh pr create --title "<type>(<scope>): <description>" --fill
   ```

4. **Merge once the change is verified** — for solo work, no need to wait on
   external review:
   ```
   gh pr merge --merge
   ```
   Use `--squash` instead if the branch has messy/WIP commits that should
   collapse into one.

5. **Delete the branch after merge:**
   ```
   git push origin --delete <branch-name>
   ```

If asked to "just push this" or "commit this fix", follow the steps above
by default instead of pushing straight to `main` — ask only if the change
is trivial enough that a full branch/PR cycle seems genuinely unnecessary
(e.g. a one-character typo fix in a personal scratch repo).
