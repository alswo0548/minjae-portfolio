#!/usr/bin/env python3
"""Improve existing OCTV demonstration recordings without fabricating UI footage.

Original frames remain from the real operational demonstration.
The animated focus cursor and click rings are editorial guidance overlays.
"""
from __future__ import annotations
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "assets" / "01-octv"

# Waypoints are fractional video time, x and y in the actual 1348x926 recording.
# They guide attention toward existing UI areas; no new application behavior is drawn.
PATHS = {
    "demo_cctv": [(0.00, 121, 330), (0.23, 420, 500), (0.43, 720, 560),
                  (0.67, 1070, 625), (0.83, 850, 720), (1.00, 710, 680)],
    "demo_overview": [(0.00, 126, 196), (0.26, 615, 470), (0.52, 580, 595),
                      (0.74, 1100, 475), (1.00, 1135, 725)],
    "demo_analysis": [(0.00, 345, 457), (0.25, 630, 385), (0.47, 1000, 356),
                      (0.70, 1150, 660), (1.00, 510, 785)],
    "demo_routes": [(0.00, 492, 392), (0.20, 805, 394), (0.38, 1145, 324),
                    (0.57, 900, 580), (0.77, 454, 744), (1.00, 1090, 645)],
}
# Subtle editorial click emphasis, never labeled as authentic click telemetry.
CLICKS = {
    "demo_cctv": [.23, .67, .83],
    "demo_overview": [.26, .52, .74],
    "demo_analysis": [.25, .47, .70],
    "demo_routes": [.20, .38, .77],
}

def probe(path: Path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate,nb_frames",
        "-show_entries", "format=duration,size", "-of", "json", str(path)],
        text=True)
    data = json.loads(out)
    return data["streams"][0], data["format"]

def build_sprites(folder: Path):
    pointer = Image.new("RGBA", (76, 76))
    soft = Image.new("RGBA", (76, 76))
    sd = ImageDraw.Draw(soft)
    sd.ellipse((9, 9, 65, 65), fill=(29, 191, 255, 55))
    pointer.alpha_composite(soft.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(pointer)
    d.ellipse((18, 18, 57, 57), fill=(20, 64, 100, 52), outline=(111, 225, 255, 229), width=3)
    d.ellipse((34, 34, 42, 42), fill=(255, 255, 255, 245), outline=(8, 24, 47, 245), width=1)
    cursor = folder / "focus-pointer.png"
    pointer.save(cursor)

    click = Image.new("RGBA", (110, 110))
    c = ImageDraw.Draw(click)
    c.ellipse((15, 15, 95, 95), outline=(255, 208, 85, 212), width=5)
    c.ellipse((27, 27, 83, 83), outline=(255, 231, 142, 120), width=3)
    ring = folder / "focus-click.png"
    click.save(ring)
    return cursor, ring

def movement(points, duration, axis: int, center: int):
    # ffmpeg evaluates this at each output frame (30 fps), independently of old frames.
    expression = f"{points[-1][axis]}"
    for i in range(len(points)-2, -1, -1):
        a, b = points[i], points[i+1]
        t0, t1 = a[0]*duration, b[0]*duration
        delta = t1-t0
        u = f"clip((t-{t0:.5f})/{delta:.5f},0,1)"
        smoothed = f"(3*pow({u},2)-2*pow({u},3))"
        value = f"({a[axis]}+({b[axis]-a[axis]})*{smoothed})"
        expression = f"if(lt(t,{t1:.5f}),{value},{expression})"
    return f"({expression}-{center})"

def improve(key: str, sprites: tuple[Path,Path]):
    src = MEDIA / f"{key}.mp4"
    stream, meta = probe(src)
    duration = float(meta["duration"])
    assert (stream["width"], stream["height"]) == (1348, 926), key
    assert stream["avg_frame_rate"] == "15/1", key
    x = movement(PATHS[key], duration, 1, 38)
    y = movement(PATHS[key], duration, 2, 38)
    rx = movement(PATHS[key], duration, 1, 55)
    ry = movement(PATHS[key], duration, 2, 55)
    pulse = "+".join(f"between(t,{max(0,v*duration-.06):.5f},{min(duration,v*duration+.24):.5f})"
                     for v in CLICKS[key])
    graph = (
        "[0:v]minterpolate=fps=30:mi_mode=blend,"
        "eq=contrast=1.04:brightness=0.012:saturation=1.055,"
        "unsharp=3:3:0.38[base];"
        f"[base][1:v]overlay=x='{x}':y='{y}':eval=frame[pointed];"
        f"[pointed][2:v]overlay=x='{rx}':y='{ry}':eval=frame:"
        f"enable='{pulse}',format=yuv420p[out]"
    )
    target = src.with_name(f"{key}.new.mp4")
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
        "-i", str(src),
        "-loop", "1", "-framerate", "30", "-i", str(sprites[0]),
        "-loop", "1", "-framerate", "30", "-i", str(sprites[1]),
        "-filter_complex", graph, "-map", "[out]", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(duration), str(target)
    ]
    print(f"ENCODING {src.name}: source={stream['avg_frame_rate']} duration={duration:.3f}s, size={meta['size']}", flush=True)
    subprocess.run(command, check=True, timeout=460)
    out_stream, out_meta = probe(target)
    fps = out_stream["avg_frame_rate"]
    output_duration = float(out_meta["duration"])
    if fps != "30/1" or abs(output_duration-duration) > 0.35:
        raise ValueError(f"{key}: invalid output {fps}, {output_duration:.3f}s / {duration:.3f}s")
    if int(out_meta["size"]) > 20_000_000:
        raise ValueError(f"{key}: enhanced video exceeds 20 MB")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(target), "-f", "null", "-"],
                   check=True, timeout=230)
    print(f"VERIFIED {target.name}: 30fps {output_duration:.3f}s, {out_meta['size']} bytes", flush=True)
    os.replace(target, src)

def main():
    with tempfile.TemporaryDirectory() as td:
        sprites = build_sprites(Path(td))
        for key in PATHS:
            improve(key, sprites)
    print("RESULT: enhanced 4 original OCTV videos; no new UI behavior invented.", flush=True)

if __name__ == "__main__":
    main()
