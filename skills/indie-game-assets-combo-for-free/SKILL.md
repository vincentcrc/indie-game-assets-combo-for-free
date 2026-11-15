---
name: indie-game-assets-combo-for-free
description: Find, verify, and source free third-party assets for games and prototypes. Use for 找免费游戏素材 or replacing placeholder assets, including sprites and tilesets, UI and fonts, 3D models and character animations, PBR textures and HDRIs, VFX, SFX and music, and engine plugins and templates. Routes requests across ten asset sites and checks specific files, licenses, and engine compatibility before adoption.
---

# indie game assets combo for free

Use this skill when a game task calls for sourcing free assets. Match the asset type, visual or audio direction, engine and version, required format, and intended use. Use project context to fill in those details. If release intent is unclear, prioritize assets suitable for commercial release and flag any material limits. When a user selects a source, start there.

## Find candidates

- Use the [source guide](references/sources.md) for provider-specific access and license rules. Start with Kenney, OpenGameArt, or itch.io for 2D/UI. Use Poly Haven, Kenney, or Fab for 3D, Poly Haven for PBR/HDRI, Mixamo for humanoid motion, and Freesound, Pixabay, or OpenGameArt for audio. Route engine-specific packages to that engine's store.
- From this skill directory, run `python3 scripts/find_assets.py route <type> "<search terms>"` for ranked public entry points. `route all` lists all ten sources. Use public site search, eligible browser tools, or domain-scoped web search to reach specific listings. If a catalog returns few matches, try a category plus one or two simpler keywords or an English variant.
- Use `poly-search` for live Poly Haven matches and `poly-files` for files and dependencies of a selected result. Show the Poly Haven source when presenting live API results. Use `godot-search "<search terms>" --version <version>` for the current Godot Asset Store. Add `--legacy` to query the separate Asset Library. The CLI help and [source guide](references/sources.md) show examples. When an API is unavailable, use the documented browser route or another source.
- Respect the provider's access method. For Unity Asset Store, give the user the manual storefront route and use independently published sources for automated discovery. For an asset behind sign-in, account claims, acceptance, or restricted downloads, give the official steps if the action needs the user. Use public alternate candidates when the user needs an asset immediately. Search only using the asset requirements needed by the provider.

## Verify and use

1. Open each candidate's original listing and inspect the relevant version and file. Confirm zero cost for that file, the license and any bundled exceptions, author, formats, and download method. Free listings can contain paid extras or use different licenses across versions. Mark missing evidence as unverified.
2. Match the intended distribution. CC0 and compatible permissive licenses are useful starting points. For CC BY, retain the required credits and license notices. Review ShareAlike, copyleft, per-seat, engine, or no-redistribution terms against the project. Exclude noncommercial-only assets from commercial releases. Check the game build, public source repository, and raw asset sharing as distinct uses.
3. For a shortlist, provide the specific source page, license and author, what the user can get at zero cost, format and compatibility, and any remaining step. Where the user requests adoption, fetch the authorized original through the official page or API when available. Preserve required license files and record the item and version, license source, attribution, changes, and local path in the project's existing credits or asset inventory. Check that it imports and works in the relevant engine before saying it was integrated.
