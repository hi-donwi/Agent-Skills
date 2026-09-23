# Motion, 3D, and scroll-synced hero video

Load before adding meaningful animation, a WebGL scene, or a pre-rendered scroll video.
This library ships no dedicated motion or 3D skill; what follows is the whole of its
guidance on both.

## Immersive 3D notes

This library ships no dedicated 3D skill; the notes below are the whole of its
3D guidance. Treat anything deeper as project-owned material.

- Describe spatial intent: camera sweep, lighting (e.g. "clustered lighting as studio softboxes").
- Tie 3D rotation / camera movement to scroll with GSAP ScrollTrigger or Framer Motion 3D.
- Generate `.glb`/`.gltf` assets, then have the agent import and render them.
- Verify the canvas in a real browser; check nonblank pixels, framing, resize behavior,
  interaction, and mobile performance.

## Scroll-synced hero video
- Load `web-development` scroll-video guidance below for pre-rendered scroll MP4 heroes.
- Inspect the project's existing video encoding command before use. If an all-keyframe
  encode is needed, verify the installed ffmpeg options and add a project-owned script;
  this skill does not bundle a video encoder.
- Wire through `SmoothHeroVideo`-style component: scroll layer + optional idle layer, posters,
  `mediaUrl()` for CDN/R2, `heroLayout` object-position per demo.
- On bugs: isolate poster-only vs scroll vs idle using the Scroll-synced hero video steps here,
  then apply `debugging/references/playbook.md` if the failure is outside the video path.

## Motion notes

This library ships no dedicated motion skill; the notes below are the whole of
its motion guidance.

- Apply the frequency gate: repeated productivity actions should be fast or static,
  while rare brand moments can be more expressive.
- Always implement `prefers-reduced-motion` behavior.
