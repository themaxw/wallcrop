from pathlib import Path
import click
import yaml


class InvalidResolution(Exception):
    pass


def parse_resolution(res_str: str, rotation: int = 0):
    res_str = res_str.split("@")[0]
    res = res_str.split("x")
    if len(res) != 2:
        raise InvalidResolution

    width, height = int(res[0]), int(res[1])

    # handle rotation
    if rotation % 2 == 1:
        width, height = height, width

    return width, height


@click.command(
    "create_monitors_file",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option("-f", "--format", type=str, default="hyprland", show_default=True)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("~/.config/hypr/hyprland.conf").expanduser(),
    help="your Hyprland config file",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, path_type=Path),
    default="monitors.yml",
    show_default=True,
)
def main(format: str, config: Path, output: Path):
    if format.lower() != "hyprland":
        print("currently only hyprland is supported")
        exit(-1)

    monitors = []
    with open(config) as f:
        for line in f:
            if not line.startswith("monitor="):
                continue

            line = line[len("monitor=") :].strip(" \n")

            name = ""

            # handle name of output as comment
            if len(split_line := line.split("#", 1)) > 1:
                name = split_line[1].strip()
                line = split_line[0]

            monitor_tuple = line.split(",")
            if name == "":
                name = monitor_tuple[0].strip()

            # ignore unnamed monitors
            if name == "":
                continue

            resolution = monitor_tuple[1].strip()
            position = monitor_tuple[2].strip()
            scale = int(monitor_tuple[3].strip())

            rotation = 0
            if len(monitor_tuple) > 4:
                for i, val in enumerate(monitor_tuple[4:]):
                    if val.strip() == "transform":
                        rotation = int(monitor_tuple[4 + i + 1])
                        break
            try:
                width, height = parse_resolution(resolution, rotation)
                x, y = parse_resolution(position)
            except InvalidResolution:
                continue

            monitors.append(
                {"name": name, "width": width, "height": height, "x": x, "y": y}
            )

    if output.exists() and not click.confirm(
        f"the file {output} already exists, do you want to overwrite?", default=False
    ):
        pass
    else:
        with open(output, "w") as f:
            yaml.dump(monitors, f, sort_keys=False)


if __name__ == "__main__":
    main()
