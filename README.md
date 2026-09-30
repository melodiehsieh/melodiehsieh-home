# melodiehsieh.com homepage

A homepage for [melodiehsieh.com](https://melodiehsieh.com) where the cows are the navigation: click a cow on the hill (it hops, says MOO! and moos out loud) to read About, Lately, the Personal Project, or how to say hi. A slider at the bottom moves the sky from day to sunset to night. It links to the [Apple Health Dashboard](https://github.com/melodiehsieh/apple-health-dashboard).

The site is one static file, `dist/index.html`, with all images embedded. There is no backend and no JavaScript dependency. Earlier design directions (Windows XP desktop, clouds and others) are kept as standalone pages in `mockups/`, which is local only.

## Build

Needs Python 3 with Pillow (`pip install pillow`).

```bash
python3 src/make_wallpaper.py   # hill, one sprite per cow, and a sky mask -> assets/
python3 src/build_homepage.py   # src/template.html + assets -> dist/index.html
```

Edit the page text (bio, "Now" list, skills, links) at the top of `src/build_homepage.py`. Edit the layout and styling in `src/template.html`. Move a cow by changing its position in `src/make_wallpaper.py`; its clickable label follows automatically.

## Still to fill in

- Your portrait lives in `assets/me.jpg` (4:5 crop). Replace it to change the photo in the About window.
- Contact email, LinkedIn, GitHub and the project links are set at the top of `src/build_homepage.py`.
- The Résumé button opens `dist/Hsieh_Melodie.pdf`. Replace that file to update it.
- The project card links to `https://melodiehsieh.com/health/`, so the dashboard needs to be served at that path.

## Credits

Wallpaper: Photo by [Zongnan Bao](https://unsplash.com/@zbao?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/green-grass-field-under-blue-sky-during-daytime-DznqzDPA0WM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Cow photos from Wikimedia Commons, licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):

- [Diary cow looking at camera](https://commons.wikimedia.org/wiki/File:Diary_cow_looking_at_camera_ylinen_2025.jpg), [Cow looking at camera 2025](https://commons.wikimedia.org/wiki/File:Cow_looking_at_camera_2025.jpg), [Cow resting while looking at camera](https://commons.wikimedia.org/wiki/File:Cow_resting_while_looking_at_camera_ylinen_2025.jpg) and [Resting cow looking at camera 2025](https://commons.wikimedia.org/wiki/File:Resting_cow_looking_at_camera_2025.jpg) by Osmo Lundell
- [Cows in Switzerland looking into the camera](https://commons.wikimedia.org/wiki/File:Cows_in_Switzerland_looking_into_the_camera.jpg) by Jonas Eppler

I cut out the backgrounds, resized the cows, and placed them on the wallpaper. The cut-outs in `assets/cows/`, the cow avatar and the composite wallpaper are adaptations of these photos and are shared under the same CC BY-SA 4.0 license.

Cow sounds: [Cow moos #2](https://bigsoundbank.com/cow-moos-2-s2382.html), [#3](https://bigsoundbank.com/cow-moos-3-s2383.html), [#5](https://bigsoundbank.com/cow-moos-5-s2385.html) and [#6](https://bigsoundbank.com/cow-moos-6-s2386.html) by Joseph Sardin, from [BigSoundBank](https://bigsoundbank.com), released under CC0 (public domain). I faded the edges, evened out the volume and compressed them (`assets/sounds/`).
