from os import path
from pathlib import Path
import subprocess
import random
import sys
from time import sleep
import click


@click.command("wallswitch")
@click.option(
    "-d",
    "--daemon",
    help="continue running in the background, to change wallpapers regularly",
    is_flag=True,
)
@click.option(
    "-t",
    "--switch-time",
    type=click.FLOAT,
    default=5 * 60,
    help="time in s after which the wallpaper will be changed",
)
@click.option("-w", "--wallpaper-tool", type=click.STRING, default="swww")
@click.argument(
    "wallpaper_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=".",
)
def main(daemon: bool, switch_time: float, wallpaper_dir: Path, wallpaper_tool: str):

    # TODO include checks that a wallpaper dir actually contains wallpapers
    wallpapers = [o for o in wallpaper_dir.iterdir() if o.is_dir()]

    while True:
        # select random wallpaper
        wallpaper_dir = random.choice(wallpapers)
        wp_name = wallpaper_dir.stem
        print(f"seting wallpaper {wp_name}")

        for wp in wallpaper_dir.glob(f"{wp_name}*"):
            display = wp.stem[len(wp_name) :]
            if wallpaper_tool == "swww":
                subprocess.run(["swww", "img", "-o", display, str(wp.absolute())])
            else:
                print("your tool is currently unsupported")
                sys.exit(-1)

        if not daemon:
            break
        sleep(switch_time)
