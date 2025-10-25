name: Generate Snake Animation

on:
  # Run automatically once a day
  schedule:
    - cron: "0 0 * * *"
  # Allow running manually from the Actions tab
  workflow_dispatch:

jobs:
  build:
    name: Generate GitHub Contribution Snake
    runs-on: ubuntu-latest

    steps:
      # 1️⃣ Checkout your repository
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2️⃣ Generate the snake animation SVG
      - name: Generate snake.svg
        uses: Platane/snk@v3
        with:
          github_user_name: Anishgoswami-dev   # <-- your GitHub username
          outputs: dist/github-contribution-grid-snake.svg

      # 3️⃣ Push the generated file to the "output" branch
      - name: Push to output branch
        uses: crazy-max/ghaction-github-pages@v3
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
