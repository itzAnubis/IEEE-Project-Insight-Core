# Palette's UX Journal

This journal tracks critical UX and accessibility learnings for the Project Insight-IEEE repository.

## 2025-05-14 - Legibility and Glanceability in OpenCV HUD
**Learning:** Text overlays in OpenCV can be difficult to read when the background video has high variance or similar colors to the text. Green text on a classroom background often lacks sufficient contrast.
**Action:** Always use a semi-transparent dark rectangle (alpha-blended) behind text overlays to ensure legibility. Implement color-coding for status indicators (e.g., Red for alerts, Green for normal) to allow users to grasp the system state at a glance without reading.
