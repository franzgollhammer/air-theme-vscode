# Air

A VS Code + Cursor port of JetBrains Air — a calm theme family with lavender keywords, pink strings, amber numbers, and green function params.

![Air theme preview](air-theme.png)

> **Pair with [Air File Icons](https://marketplace.visualstudio.com/items?itemName=franzgollhammer.air-file-icons)** ([Open VSX](https://open-vsx.org/extension/franzgollhammer/air-file-icons) · [repo](https://github.com/franzgollhammer/air-icons-vscode)) — matching JetBrains Air–inspired file icon theme.

## Features

- **Air dark** — near-black `#18191B` editor, soft pastel syntax
- **Air light** — near-white `#FBFBFC` editor, deep-tone syntax
- Matched UI chrome, git decorations, diff colors, and terminal ANSI palette
- Semantic highlighting tuned for JavaScript, TypeScript, Python, Rust, Go, Java, C/C++, PHP, and Ruby

## Install

### VS Code

1. Extensions panel (`Cmd+Shift+X` / `Ctrl+Shift+X`)
2. Search `Air` by `franzgollhammer`
3. Install
4. `Cmd+K Cmd+T` → **Air dark** or **Air light**

Or via CLI:

```sh
code --install-extension franzgollhammer.air-theme
```

### Cursor

Cursor pulls extensions from Open VSX. Same flow: open the Extensions panel, search `Air`, install, then pick it under `Color Theme`.

```sh
cursor --install-extension franzgollhammer.air-theme
```

### Manual (`.vsix`)

Download the latest `.vsix` from [Releases](https://github.com/franzgollhammer/air-theme-vscode/releases), then:

```sh
code --install-extension air-theme-<version>.vsix
# or
cursor --install-extension air-theme-<version>.vsix
```

## Palette

### Air dark

| Color       | Role                                                           |
| ----------- | -------------------------------------------------------------- |
| `#D6D6DD`   | Default fg — variables, punctuation, identifiers               |
| `#A8CC7C`   | Function params (at declaration)                               |
| `#82D2CE`   | Storage/keywords, types, booleans, markdown list markers       |
| `#AAA0FA`   | `const`/`let` declarations, imports, markdown headings         |
| `#F8C762`   | Functions, invocations, bold                                   |
| `#EFB080`   | Classes, type names, namespaces                                |
| `#E394DC`   | Strings, markdown link parens                                  |
| `#87C3FF`   | CSS properties, support classes                                |
| `#EBC88D`   | Numbers                                                        |
| `#CC7C8A`   | `this` / `self`                                                |

Editor background: `#18191B`.

### Air light

| Color       | Role                                                           |
| ----------- | -------------------------------------------------------------- |
| `#1F2024`   | Default fg                                                     |
| `#4E7A2A`   | Function params                                                |
| `#1F7F78`   | Storage/keywords, types, booleans                              |
| `#5A4ECF`   | Declarations, imports, markdown headings                       |
| `#8D6B1F`   | Functions, invocations, bold                                   |
| `#A85A29`   | Classes, type names, namespaces                                |
| `#B03A88`   | Strings, markdown link parens                                  |
| `#0E5FA8`   | CSS properties, support classes                                |
| `#8F6614`   | Numbers                                                        |
| `#A54553`   | `this` / `self`                                                |

Editor background: `#FBFBFC`.

## Development

```sh
npm run dev            # launch VS Code with the extension loaded
npm run dev:insiders   # VS Code Insiders
npm run package        # build .vsix
npm run install:local  # package + install into VS Code
```

See [`scripts/`](scripts) for release automation and [`RELEASING.md`](RELEASING.md) for the publish flow.

## Credits

Inspired by [JetBrains Air](https://www.jetbrains.com/).

## License

[MIT](LICENSE.md)
