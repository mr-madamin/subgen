import argparse

from .audio import extract_audio, probe_tracks


def cmd_tracks(args):
    for t in probe_tracks(args.video):
        lang = t.language or "und"
        title = f"  {t.title}" if t.title else ""
        print(
            f"[{t.index}] {lang:<4} {t.codec_name} {t.channels}ch {t.sample_rate}Hz{title}"
        )


def cmd_extract(args):
    tracks = probe_tracks(args.video)
    indices = {t.index for t in tracks}
    if args.track not in indices:
        raise SystemExit(
            f"track {args.track} is not an audio stream; available: {sorted(indices)}"
        )
    out = extract_audio(args.video, args.out, args.track)
    print(f"wrote {out}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="subtitle", description="...")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tracks = sub.add_parser("tracks", help="list audio tracks")
    p_tracks.add_argument("video")
    p_tracks.set_defaults(func=cmd_tracks)

    p_extract = sub.add_parser("extract", help="extract 16 kHz mono WAV")
    p_extract.add_argument("video")
    p_extract.add_argument("-o", "--out", required=True)
    p_extract.add_argument("--track", type=int, required=True)
    p_extract.set_defaults(func=cmd_extract)

    args = parser.parse_args()
    args.func(args)
