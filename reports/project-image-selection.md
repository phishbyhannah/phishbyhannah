# Project Image Selection

## Grouping method

- Grouped by location keywords in folder and filename.
- Used year tokens in filenames and EXIF content creation date when present.
- Images not confidently mapped were left in `unassigned`.
- Excluded any image already referenced on other site pages.

## Curation method

- Removed exact and near duplicates using SHA-256 and resized-hash buckets.
- Prioritized cinematic frames using filename cues for wildlife, people, wide scenes, and details.
- Kept a mixed rhythm of landscape and portrait frames where available.

## Sri Lanka - 2026

- Layout: `horizontal-snap`
- Selected images: 18
- Variety mix: wide=18

## Raja Ampat - 2024

- Layout: `horizontal-snap`
- Selected images: 18
- Variety mix: detail=1, people=9, wide=7, wildlife=1

## Ningaloo - 2024

- Layout: `horizontal-snap`
- Selected images: 29
- Variety mix: people=11, wildlife=18

## Tonga - 2025

- Layout: `horizontal-snap`
- Selected images: 11
- Variety mix: people=2, wide=6, wildlife=3

## Ningaloo - 2025

- Layout: `horizontal-snap`
- Selected images: 18
- Variety mix: detail=4, people=5, wildlife=9

## Break images

- sri-lanka-2026 -> raja-2024 (fullpage):
  - /images/journey/phish-journey-safari-SriLanka-2025-007.jpg (wide, landscape)
- raja-2024 -> ningaloo-2024 (halfheight):
  - /images/journey/phish-journey-view-raja-2024-009.jpg (wide, landscape)
- ningaloo-2024 -> tonga-2025 (pair):
  - /images/me/phish-Me-whaleshark-ningaloo-2024-001.jpg (wildlife, landscape)
  - /images/journey/phish-journey-view-tonga-2025-005.jpg (wide, portrait)
- tonga-2025 -> ningaloo-2025 (halfheight):
  - /images/peopleinplace/phish-peopleinplace-BWR-tonga-2025-003.jpg (people, landscape)
- endcap (fullpage):
  - /images/waterhabitat/phish-waterhabitat-whaleshark-ningaloo-2025-001.jpg (wildlife, landscape)

## Notes

- Unassigned images: 73
- Excluded as already used elsewhere: 111
- WebP derivatives were not generated in this environment due missing local WebP encoder support.
