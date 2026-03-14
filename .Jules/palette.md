## 2025-05-14 - Legibility of HUD Overlays
**Learning:** HUD text rendered directly over dynamic video feeds often suffers from poor contrast, making it difficult to read in varying lighting conditions or busy scenes. A semi-transparent dark background (alpha-blended) provides a consistent high-contrast area for text while maintaining situational awareness of the underlying video.
**Action:** Always implement a dark semi-transparent rectangle using `cv2.addWeighted` behind any diagnostic or informational text overlays in OpenCV-based interfaces.
