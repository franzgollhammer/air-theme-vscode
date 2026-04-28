# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-04-28

### Added

- README preview screenshots for **Air dark** and **Air light**.

## [1.0.1] - 2026-04-27

### Fixed

- Object property keys (`templateName: ...`, `language: ...`) now render as default foreground instead of purple. Destructured variable declarations (`const { htmlBody } = ...`) keep purple via semantic highlighting. Mirrored across dark + light.

## [1.0.0] - 2026-04-23

### Added

- Initial release
- **Air dark** color theme (`vs-dark`, editor bg `#18191B`)
- **Air light** color theme (`vs`, editor bg `#FBFBFC`)
- Matched UI chrome, git decorations, diff colors, terminal ANSI palette
- Semantic highlighting for JavaScript, TypeScript, Python, Rust, Go, Java, C/C++, PHP, Ruby
- Marketplace metadata (README, icon, banner, keywords)
