# Releasing

## Prerequisites (one-time)

### VS Code Marketplace

1. Create a publisher at <https://marketplace.visualstudio.com/manage>
2. Generate a PAT: <https://dev.azure.com> → User Settings → Personal Access Tokens
   - Organization: **All accessible organizations**
   - Scope: **Marketplace → Manage**
3. Store it:
   ```sh
   export VSCE_PAT=<token>
   # or: npx @vscode/vsce login franzgollhammer
   ```

### Open VSX (Cursor / VSCodium / Gitpod)

1. Sign in at <https://open-vsx.org>, agree to the publisher agreement
2. Create a token: <https://open-vsx.org/user-settings/tokens>
3. Create the namespace (once per publisher):
   ```sh
   npx ovsx create-namespace franzgollhammer -p $OVSX_PAT
   ```
4. Store the token:
   ```sh
   export OVSX_PAT=<token>
   ```

## Release flow

```sh
git checkout -b release/vX.Y.Z
npm run verify                   # sanity check vsix contents
bash scripts/release.sh patch    # or minor | major | X.Y.Z
git push origin HEAD --follow-tags
```

`release.sh` does:
1. Refuses to run on `main`/`master` or with a dirty tree
2. Bumps `package.json` version
3. Packages the `.vsix`
4. Verifies vsix contents (no junk, required assets present)
5. Publishes to VS Code Marketplace
6. Publishes to Open VSX
7. Commits `chore(release): vX.Y.Z` and tags `vX.Y.Z`

## Manual flow

```sh
npm run package            # build vsix only
npm run verify             # inspect vsix
npm run publish:vscode     # VS Code Marketplace
npm run publish:openvsx    # Open VSX (Cursor)
npm run publish            # both
```

## Local install

```sh
npm run install:local                # into VS Code
bash scripts/install-local.sh cursor # into Cursor
bash scripts/install-local.sh code-insiders
```

## Regenerating the light variant

The light theme is generated from the dark one by `scripts/make-light.py`:

```sh
npm run build:light
```

Edit the color map in `scripts/make-light.py`, re-run, and commit both the script and `themes/air-light-color-theme.json`.

## After release

- Create a GitHub Release with the `.vsix` attached:
  ```sh
  gh release create vX.Y.Z *.vsix --generate-notes
  ```
- Update `CHANGELOG.md` Unreleased → new version section
