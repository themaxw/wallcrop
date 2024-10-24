from os import path
from pathlib import Path
import subprocess
import random
import sys
from time import sleep
import click


@click.command(
    "wallswitch",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
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
@click.option(
    "-w", "--wallpaper-tool", type=click.Choice(["swww", "hyprpaper"]), default="swww"
)
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
            display = wp.stem[len(wp_name) :].strip(" _")
            if wallpaper_tool == "swww":
                subprocess.run(["swww", "img", "-o", display, str(wp.absolute())])
            elif wallpaper_tool == "hyprpaper":
                subprocess.run(["hyprctl", "hyprpaper", "preload", str(wp.absolute())])
                subprocess.run(
                    [
                        "hyprctl",
                        "hyprpaper",
                        "wallpaper",
                        f"{display},{str(wp.absolute())}",
                    ]
                )
            else:
                print("your tool is currently unsupported")
                sys.exit(-1)
        if wallpaper_tool == "hyprpaper":
            sleep(0.2)
            subprocess.run(["hyprctl", "hyprpaper", "unload", "all"])
        if not daemon:
            break
        sleep(switch_time)
