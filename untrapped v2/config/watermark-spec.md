# unTRAPPED watermark specification

**Status: APPROVED.**

The business requirement is to render every upload derivative with the approved unTRAPPED logo watermark while preserving the original source photo unchanged.

## Approved asset

- Repository path: `../branding/untrapped-logo.PNG`
- Format: PNG
- Dimensions: 229 × 60 pixels
- SHA-256: `03d2a1fdeaf5177d9c5bab668bfc56f98a66632b38528569e71d1e5ddd565c1f`

The repository copy is byte-for-byte identical to the approved source supplied by the human.

## Authoritative settings

All adjustable rendering values are stored in [`watermark-settings.json`](watermark-settings.json). Agents and tools must read that file at run time rather than hard-code the values elsewhere.

The currently approved defaults are:

- bottom-right placement;
- 24-pixel margin;
- width equal to 60% of the oriented photo width;
- 50% opacity;
- correct photo orientation before watermarking;
- preserve the logo aspect ratio; and
- no date stamp.

The human may change these settings later by editing the configuration file. A preparation tool must validate the file before processing: `margin_pixels` must be zero or greater, and `width_ratio` and `opacity` must each be greater than zero and no greater than one. An unsupported placement or invalid value blocks preparation without altering source photos.

## Approved file handling

- Never alter source photos in `incoming/`.
- When HEIC is converted to JPG, `synced_photos` records the resulting JPG filename actually uploaded and attached.
- Watermarked derivatives created locally may remain locally.
- Uploaded derivatives remain in Drive.
- Never re-download an uploaded file merely to manufacture a local copy.

Do not reuse the historical text watermark or invent settings when the configuration is missing or invalid.
