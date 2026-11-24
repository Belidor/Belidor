<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/header-narrow-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/header-narrow-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Artem Kupratsevich. QA Engineer working remotely from Belgrade, Serbia. A self-test run: automation, releases, people and side work, 4 passed, 0 failed.">
</picture>

Over ten years of test automation for web, mobile and APIs. On the side I build small systems that watch things and report back: a camera that keeps an eye on my dog, a voice assistant for the family smart speaker, a bot that posts the lake temperature every morning.

Most of that code is private, so this page lists what I have built. My site is [belidor.cc](https://belidor.cc); work history is on [LinkedIn](https://www.linkedin.com/in/akupratsevich/).

## Live projects

### [TriSplits](https://triathlon-calculator.online)

<a href="https://triathlon-calculator.online"><img src="assets/trisplits.jpg" width="100%" alt="TriSplits: distance presets at the top, swim and transition pace sliders on the left, the estimated finish time on the right"></a>

Finish-time and split estimator for every triathlon distance, in six languages. A static Next.js site with 30 pre-rendered pages, unit-tested pacing math and a small nginx deploy on a VPS.

`Next.js` `TypeScript` `Vitest`

Site: [triathlon-calculator.online](https://triathlon-calculator.online).

### [GTA VI Countdown for Garmin](https://gta6-garmin.belidor.cc)

<a href="https://gta6-garmin.belidor.cc"><img src="assets/gta6.jpg" width="100%" alt="A Garmin Forerunner 965 showing the GTA VI countdown watch face in front of a Vice City sunset"></a>

A free watch face, glance and app for Garmin watches that tick down to the GTA VI release on 19 November 2026: days, hours, minutes and seconds, with a quiet always-on mode on AMOLED screens. Builds for 123 watch models, a landing page with a per-watch installer, and both apps in the Connect IQ Store.

`Monkey C` `Connect IQ` `GitHub Pages`

Site: [gta6-garmin.belidor.cc](https://gta6-garmin.belidor.cc). Source: [Belidor/gta6-countdown](https://github.com/Belidor/gta6-countdown), MIT.

### [Search on Kupujemprodajem](https://chromewebstore.google.com/detail/search-on-kupujemprodajem/eidkdejdckeneilcfpojkejjnnjnhkgb)

<a href="https://chromewebstore.google.com/detail/search-on-kupujemprodajem/eidkdejdckeneilcfpojkejjnnjnhkgb">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/kupujemprodajem-dark.svg">
  <img src="assets/kupujemprodajem-light.svg" width="100%" alt="A browser context menu over a classified listing. The selected words can be searched on Kupujemprodajem or Halo Oglasi.">
</picture>
</a>

A Chrome extension for life in Serbia: select any text on any page and search it on the country's two big classifieds sites, Kupujemprodajem and Halo Oglasi, straight from the context menu.

`JavaScript` `Chrome Extensions API`

Install: [Chrome Web Store](https://chromewebstore.google.com/detail/search-on-kupujemprodajem/eidkdejdckeneilcfpojkejjnnjnhkgb).

### [pawsight](https://github.com/Belidor/pawsight)

<a href="https://github.com/Belidor/pawsight"><img src="assets/pawsight.jpg" width="100%" alt="The pawsight banner: a dog drinking from its water bowl, with the boxes and zones pawsight draws around the dog and both bowls"></a>

The camera that watches my dog, now open source. An IP camera feeds a YOLO detector, zones anchored to the bowls count every visit to the water and the food, a local vision model tells drinking from eating, and Telegram gets short reports. A pan/tilt camera follows the dog and comes back to the bowls. Runs on one Mac or Linux box, no cloud, no open ports; one install script.

`Python` `YOLO` `Ollama` `go2rtc` `MQTT` `Telegram`

Source: [Belidor/pawsight](https://github.com/Belidor/pawsight), AGPL-3.0.

## More projects

The source of these is private. `live` means working and in use, `beta` means open to a small group of testers, `in progress` means still being built.

| Project | What it does | Status |
| --- | --- | --- |
| Teachy | A workspace for private tutors: a lesson calendar with recurring series, student balances and payments, homework and income analytics. Students get a Telegram Mini App. Tutors join by invite. | `beta` |
| [Cossacks in the browser](https://cossacks.belidor.cc) | The 2002 strategy game in the browser through js-dos. The 610 MB bundle streams from a private Cloudflare R2 bucket behind a hard daily cap, so the bill stays at zero. | `live` |
| [Need for Speed: Underground in the browser](https://nfsu.belidor.cc) | The 2003 street racer in the browser: BottleShip runs the Windows game in WebAssembly with WebGPU, Classic and HD builds, cloud saves behind a personal code. | `live` |
| Belgrade weather bot | A daily Telegram post with the water temperature at Ada Ciganlija, air, wind and UV, cross-checked across several sources. | `live` |
| Homework | A teacher uploads an HTML assignment and gets a link. Students fill it in on the page; the teacher sees each page as it was filled in. | `live` |
| Lotto for Telegram | Classic Russian lotto as a Telegram Mini App, with rooms for seven players and automatic draws. | `live` |
| Photo Cleaner | An iOS app that turns clearing the camera roll into a swipe deck. Nothing is deleted until you confirm. | `beta` |
| Family assistant for Alice | A private skill for the Yandex smart speaker. Answers with Claude, keeps the family calendar and shopping list, says when the next bus leaves. | `in progress` |
| Claude Code mods | Plugins for my own workflow: continue a task after the usage limit resets, check replies against Simplified Technical English, drive Android devices for test runs. | `in progress` |

## Toolbox

**Testing:** Playwright, TypeScript, XCUITest, Appium, CodeceptJS, Selenium, JMeter\
**Pipelines:** Jenkins, GitLab CI, GitHub Actions, Docker, PostgreSQL\
**Side projects:** Python, FastAPI, React, Next.js, Monkey C, YOLO, Ollama, Telegram Bot API, Vercel, Cloudflare, Supabase
