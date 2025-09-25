# teletext-bluesky - creates pages for vbit2 teletext system
# (c) ZXGuesser 2025 (https://https://github.com/ZXGuesser)
# based on https://github.com/mpentler/teletext-twitter

from output import *
import time
import sys
import argparse

# Read config.py for our colour settings etc
config = {}
exec(open("config.py").read(), config)

def parse_args():
    parser = argparse.ArgumentParser(description="Searches Bluesky posts and turns them into teletext pages.")

    parser.add_argument("-q", "--query", type=str, help="a Bluesky search query")
    parser.add_argument("-c", "--count", type=int, default=5, help="number of posts to download (default is 5, capped at 200)")
    parser.add_argument("-d", "--delay", type=int, default=60, help="seconds between timeline scrapes (default is 60 seconds - lower values have no effect)")
    parser.add_argument("-n", "--no-repeat", action="store_true", default=False, help="only download posts once - overrules -d switch")
    parser.add_argument("-Q", "--quiet", action="store_true", default=False, help="suppresses all output to the terminal except warnings and errors")

    args = parser.parse_args()
    args.count = min(args.count, 200)
    args.delay = max(60, args.delay)

    if not args.query:
        print("[!] no query specfied with -q. Exiting...", file=sys.stderr)
        sys.exit(1)

    return args

def main():
    args = parse_args()

    if not args.quiet:
        print("[*] teletext-bluesky - by ZXGuesser", file=sys.stdout)
        print("[*] based on teletext-twitter by Mark Pentler (https://github.com/mpentler)", file=sys.stdout)

    while True:
        try:
            if not args.quiet:
                print("[*] Getting {} most recent posts containing: {}".format(args.count, args.query), file=sys.stdout)
            write_posts(args.count, config, args.query)
            if not args.quiet:
                print("[*] Waiting {} seconds until next scrape".format(args.delay), file=sys.stdout)
        except OSError as e:
            print("[!] Error accessing teletext data file, {}".format(e.strerror), file=sys.stderr)
        if not args.no_repeat:
            time.sleep(args.delay)
        else:
            if not args.quiet:
                print("[*] No repeat mode enabled. Exiting...", file=sys.stdout)
            sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[*] Interrupted by user. Exiting...", file=sys.stdout)
        sys.exit(0)
