"""Generate README.md (keeps the content of the workflow-managed marker sections).

    python scripts/poster/readme.py
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
REPO = "Anishgoswami-dev/Anishgoswami-dev"


def pic(path: str, alt: str, width: str = "100%", extra: str = "", dark: bool = True) -> str:
    """<picture> with dark/light sources; `path` contains {m} for the mode."""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{path.format(m="dark")}">'
            f'<source media="(prefers-color-scheme: light)" srcset="{path.format(m="light")}">'
            f'<img alt="{alt}" src="{path.format(m="light")}" width="{width}" {extra}></picture>')


_n = [0]


def title(slug: str, alt: str) -> str:
    _n[0] += 1
    div = "divider" if _n[0] % 2 else "divider2"
    return (f'<p align="center">{pic("assets/sections/" + div + "-{m}.svg", "")}</p>\n'
            f'<p align="center">{pic("assets/titles/" + slug + "-{m}.svg", alt)}</p>\n')


def card(key: str, name: str, band_url: str, repo_url: str) -> str:
    """Project card (links to the repo) with an attached action band (download, live demo or the repo)."""
    top = pic("assets/projects/" + key + "-{m}.svg", name + " project card", "100%", 'align="top"')
    band = pic("assets/projects/" + key + "-band-{m}.svg", "Action button for " + name, "100%", 'align="top"')
    return (f'<td width="50%" align="center" valign="top">\n'
            f'<a href="{repo_url}">{top}</a><br>\n'
            f'<a href="{band_url}">{band}</a>\n</td>')


def main() -> None:
    owner = REPO.split("/")[0]
    out = f'''<div align="center">
{pic("assets/banners/header-{m}.svg", "Anish Goswami: hand-drawn signature, animated aurora banner")}
</div>

<a href="scripts/ascii/">{pic("assets/ascii/portrait-{m}.svg", "Animated developer portrait of Anish Goswami", "420", 'align="left" hspace="10"').replace('src="assets/ascii/portrait-light.svg"', 'src="assets/ascii/portrait.gif"')}</a>

{pic("assets/hero/hello-{m}.svg", "Hi, I'm Anish", "360")}<br>
{pic("assets/hero/roles-{m}.svg", "I build AI & deep learning models, full-stack web apps, computer vision systems, intelligent automations, smart developer tools", "360")}<br>
{pic("assets/hero/chips-{m}.svg", "B.Tech CSE at MSIT, Kolkata IST, batch 2025 to 2029, open to internships", "360")}

{pic("assets/hero/welcome-{m}.svg", "Welcome to my space", "360")}<br>
<a href="https://github.com/{owner}">{pic("assets/hero/btn-follow-{m}.svg", "Follow me on GitHub", "172")}</a><a href="https://github.com/{owner}?tab=repositories">{pic("assets/hero/btn-work-{m}.svg", "See my work", "172")}</a>

<br clear="left">

<p align="center">{pic("assets/sections/ticker-{m}.svg", "Python, AI / ML, Computer Vision, Full-stack, Automation, Deep Learning")}</p>

{title("about", "About me")}
<p align="center">{pic("assets/sections/about-{m}.svg", "B.Tech CSE at MSIT, full-stack & AI developer, exploring computer vision and intelligent systems, looking for internships")}</p>

{title("toolbox", "Toolbox")}
<p align="center">{pic("assets/sections/toolbox-{m}.svg", "Toolbox: Python, TypeScript, JavaScript, C, HTML/CSS, React, Vite, Django, Git, GitHub; learning Jupyter, Pandas, Android, Computer Vision, ML, LLM agents and automation")}</p>

<p align="center">{pic("assets/sections/ticker2-{m}.svg", "Build, train, innovate, repeat, code, scale")}</p>

{title("work", "Featured work")}
<!-- FEATURED:START -->
<!-- filled by scripts/featured.py from the pinned repositories -->
<!-- FEATURED:END -->

<p align="center"><a href="https://github.com/{owner}?tab=repositories">{pic("assets/sections/more-{m}.svg", "More from my repositories: open the repositories page")}</a></p>
<p align="center">
<!-- MORE:START -->
<!-- filled by scripts/featured.py -->
<!-- MORE:END -->
</p>

{title("stats", "By the numbers")}
<p align="center">{pic("assets/stats/dashboard-{m}.svg", "GitHub stats: commits, pull requests, stars, followers, top languages and contribution streak")}</p>

{title("city", "Contribution city")}
<p align="center">{pic("assets/3d/contribution-{m}.svg", "3D contribution chart for the last 36 weeks", "100%")}</p>

{title("activity", "Live activity")}
<p align="center">{pic("assets/live/greeting-{m}.svg", "Time-of-day greeting")}</p>

{title("play", "Play a game")}
<p align="center"><a href="https://anishgoswami-dev.github.io/Anishgoswami-dev/">{pic("assets/sections/arcade-{m}.svg", "Bug Hunter, a playable arcade shooter. Click to play.")}</a></p>

{title("connect", "Let's connect")}
<p align="center">
<a href="mailto:anishgoswami20006@gmail.com">{pic("assets/contact/email-{m}.svg", "Email Anish", "250")}</a>
<a href="https://github.com/{owner}">{pic("assets/contact/github-{m}.svg", "Anish on GitHub", "250")}</a>
<a href="https://www.linkedin.com/in/anish-goswami-06a1a1333/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/contact/linkedin-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/contact/linkedin-light.svg"><img alt="LinkedIn" src="assets/contact/linkedin-light.svg" width="250"></picture></a>
<a href="https://www.youtube.com/@Anishgoswami8082"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/contact/youtube-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/contact/youtube-light.svg"><img alt="YouTube" src="assets/contact/youtube-light.svg" width="250"></picture></a>
<a href="https://discord.com/users/anish0331"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/contact/discord-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/contact/discord-light.svg"><img alt="Discord" src="assets/contact/discord-light.svg" width="250"></picture></a>
<a href="https://www.instagram.com/anish_goswami_828"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/contact/instagram-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/contact/instagram-light.svg"><img alt="Instagram" src="assets/contact/instagram-light.svg" width="250"></picture></a>
</p>

<p align="center"><a href="https://github.com/{REPO}">{pic("assets/sections/star-{m}.svg", "Enjoyed the tour? Star this repo")}</a></p>

<div align="center">
{pic("assets/banners/footer-{m}.svg", "Thanks for stopping by")}
</div>
'''
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from bust import carry, carry_blocks
    old = README.read_text(encoding="utf-8") if README.exists() else ""
    README.write_text(carry_blocks(old, carry(old, out)), encoding="utf-8")
    print("README.md written")


if __name__ == "__main__":
    main()
