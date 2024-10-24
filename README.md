# Wallcrop

![header](assets/github-header.png)

Wallcrop is a simple tool for cropping an image into smaller images for use as individual desktop wallpapers in a multi-monitor setup.

It can either arrange by size in pixels, or by the actual size of the monitors in cm.

## Installation:

The easiest way to install would be using `pip` in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install wallcrop
```

## Usage

In order to crop up some images you need to let wallcrop know about your monitor setup. This is done in a yaml file, here called `monitors.yml`, an example for this file can be found in `examples/monitors.yml`.

The `monitors.yml` contains a list of monitors, each with a `name`, `height` and `width` of the monitor (if your monitor is vertical just swap these) and `x` and `y` position of the top left corner of the monitor in pixels.
If you want to use the `actual-monitor-size` (`-a`) option (arranging not by the size in pixels, but the actual size of the screens in cm) you need to additionally add values for `x_cm`, `y_cm`, `width_cm` and `height_cm` for each monitor, in that case you don't need values for `x` and `y`. Gaps between monitors should be accounted for in `x_cm` and `y_cm`.

In the used coordinate system $x=0$, $y=0$ is the top-left corner, with x increasing to the right, and y increasing down. negative values for these are also fine.

To crop an image use

```bash
wallcrop -m path/to/your/monitors.yml path/to/your/image.png
```

To crop all images in a folder use

```bash
wallcrop -m path/to/your/monitors.yml path/to/your/images/*
```

For more options see

```bash
wallcrop -h
```

## wallswitch

as a treat, there also is wallswitch for setting the wallpapers following the wallcrop structure. this currently only supports `swww` and `hyprpaper` (using preload`hyprctl hyprpaper` for IPC) as wallpaper daemons and only works if the names of the monitors in the `monitors.yml` correspond to the names of the outputs

## creating the monitors file on Hyprland

There is also an experimental tool for automatically creating a `monitors.yml` from your hyprland config, see

```bash
wallcrop_create_monitors -h
```

for more info
