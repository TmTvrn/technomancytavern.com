# Technomancy Tavern

Splash page for [technomancytavern.com](https://technomancytavern.com): a single-file, canvas-rendered pixel-art scene featuring Mancy, the tavern's technomancer barkeep.

- Everything lives in `index.html`; no build step.
- Cloudflare Pages (project `tmtvrn`) deploys every push to `main`. Pushes to other branches get preview URLs on `tmtvrn.pages.dev`.
- `tmtvrn.com` and both `www` hosts redirect here (Cloudflare redirect rules, not this repo).
- Set `STEAM_URL` near the top of the script once the Steam page exists.

Run locally:

```bash
python3 -m http.server 8787
```

Contact: contact@tmtvrn.com
