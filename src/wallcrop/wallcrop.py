import os
import yaml
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from math import ceil
import click
from tqdm import tqdm



@click.command("wallcrop")
@click.option(
    "-m",
    "--monitors",
    "monitor_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default="./monitors.yml",
)
@click.option(
    "-n",
    "--no_scale",
    is_flag=True,
    help="Disables Scaling of Input Image. If Image is too small, it will be skipped",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, path_type=Path),
    default="./wallcrop",
)
@click.option(
    "-f", "--format", type=click.STRING, default="png"
)
@click.argument("input_file", nargs=-1, type=click.Path(exists=True, path_type=Path))
def main(monitor_file: Path, output_path: Path, no_scale: bool, input_file: tuple[Path], format: str):
    with open(monitor_file) as f:
        monitors = yaml.safe_load(f)

    min_x = min([m["x"] for m in monitors])
    min_y = min([m["y"] for m in monitors])
    max_x = max([m["x"] + m["width"] for m in monitors])
    max_y = max([m["y"] + m["height"] for m in monitors])

    total_width, total_height = max_x - min_x, max_y - min_y
    tqdm.write(f"total screen area: {total_width}x{total_height}")

    for image_path in tqdm(input_file):
        if not image_path.is_file():
            continue

        try:
            im = Image.open(image_path)
        except UnidentifiedImageError:
            tqdm.write(f"could not open file {image_path}, skipping...")
            continue

        width, height = im.size
        if no_scale and not (width >= total_width and height >= total_height):
            tqdm.write(f"image {image_path} is to small, skipping...")
            continue
        elif not no_scale:
            scale_x = total_width / width
            scale_y = total_height / height
            scale = max(scale_x, scale_y)
            if scale != 1:
                im = im.resize((int(ceil(width * scale)), int(ceil(height * scale))))
                scaling_direcion = "up" if scale >= 1 else "down"
                tqdm.write(f"scaled {image_path.stem} {scaling_direcion} to {im.size}, scaling factor = {scale:.02}")

        width, height = im.size
        offset_x = int(width / 2 - total_width / 2) - min_x
        offset_y = int(height / 2 - total_height / 2) - min_y

        os.makedirs(output_path / image_path.stem, exist_ok=True)

        for m in monitors:
            x_l = offset_x + m["x"]
            x_r = x_l + m["width"]

            y_u = offset_y + m["y"]
            y_l = y_u + m["height"]
            cropped = im.crop((x_l, y_u, x_r, y_l))

            filename = f"{image_path.stem}_{m["name"]}.{format}"
            cropped.save(output_path / image_path.stem / filename)



if __name__ == "__main__":
    main()
