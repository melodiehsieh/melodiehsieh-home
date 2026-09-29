# melodiehsieh.com homepage

A Windows XP-style desktop homepage for [melodiehsieh.com](https://melodiehsieh.com): draggable windows, a Start menu, a taskbar, and a herd of cows on a green hill. It links to the [Apple Health Dashboard](https://github.com/melodiehsieh/apple-health-dashboard).

The site is one static file, `dist/index.html`, with all images embedded. There is no backend and no JavaScript dependency.

## Build

Needs Python 3 with Pillow (`pip install pillow`).

```bash
python3 make_wallpaper.py   # cut-outs from assets/cows/ placed on assets/hill-base.jpg -> assets/hill-cows.jpg
python3 build_homepage.py   # template.html + assets -> dist/index.html
```

Edit the page text (bio, "Now" list, skills, links) at the top of `build_homepage.py`. Edit the layout and styling in `template.html`. Move a cow by changing its position in `make_wallpaper.py`.

## Still to fill in

- Your portrait: add `dist/me.jpg`. The About window shows a silhouette until it exists.
- Contact email, LinkedIn URL and `/resume.pdf` are placeholders in `template.html`.
- The project card links to `/health/`, so the dashboard needs to be served at that path.

## Credits

Wallpaper: Photo by [Zongnan Bao](https://unsplash.com/@zbao?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/green-grass-field-under-blue-sky-during-daytime-DznqzDPA0WM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Cow photos from Wikimedia Commons, licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/):

- [Diary cow looking at camera](https://commons.wikimedia.org/wiki/File:Diary_cow_looking_at_camera_ylinen_2025.jpg), [Cow looking at camera 2025](https://commons.wikimedia.org/wiki/File:Cow_looking_at_camera_2025.jpg), [Cow resting while looking at camera](https://commons.wikimedia.org/wiki/File:Cow_resting_while_looking_at_camera_ylinen_2025.jpg) and [Resting cow looking at camera 2025](https://commons.wikimedia.org/wiki/File:Resting_cow_looking_at_camera_2025.jpg) by Osmo Lundell
- [Cows in Switzerland looking into the camera](https://commons.wikimedia.org/wiki/File:Cows_in_Switzerland_looking_into_the_camera.jpg) by Jonas Eppler

I cut out the backgrounds, resized the cows, and placed them on the wallpaper. The cut-outs in `assets/cows/`, the cow avatar and the composite wallpaper are adaptations of these photos and are shared under the same CC BY-SA 4.0 license.
