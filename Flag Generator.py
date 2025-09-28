cat > flaggen.py <<'PY'
#!/usr/bin/env python3
"""
Random Flag Generator - flaggen.py
Generates fake CTF flags like: CTF{a1b2c3}
"""
import argparse
import random
import secrets
import string
from pathlib import Path
from typing import List

COMMON_WORDS = [
    "alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel","india",
    "juliet","kilo","lima","mike","november","oscar","papa","quebec","romeo",
    "sierra","tango","uniform","victor","whiskey","xray","yankee","zulu"
]

def gen_random_token(length: int, charset: str) -> str:
    if charset == "alnum":
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    if charset == "hex":
        chars = string.hexdigits.lower()
        return ''.join(secrets.choice(chars) for _ in range(length))
    if charset == "digits":
        chars = string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))
    if charset == "words":
        out = []
        while len(''.join(out)) < length:
            out.append(random.choice(COMMON_WORDS))
        token = ''.join(out)[:length]
        return token
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_flags(count: int, length: int, charset: str, prefix: str, suffix: str,
                   template: str, unique: bool) -> List[str]:
    flags = []
    seen = set()
    attempts = 0
    max_attempts = count * 10
    while len(flags) < count and attempts < max_attempts:
        token = gen_random_token(length, charset)
        flag = template.replace("{prefix}", prefix).replace("{token}", token).replace("{suffix}", suffix)
        attempts += 1
        if unique:
            if flag in seen:
                continue
            seen.add(flag)
        flags.append(flag)
    if len(flags) < count:
        raise RuntimeError("Could not generate enough unique flags. Try smaller count or larger token size.")
    return flags

def main():
    parser = argparse.ArgumentParser(description="Random Flag Generator for CTFs")
    parser.add_argument("-n", "--number", type=int, default=10, help="Number of flags to generate (default: 10)")
    parser.add_argument("-l", "--length", type=int, default=8, help="Length of token part (default: 8)")
    parser.add_argument("-c", "--charset", choices=["alnum","hex","digits","words"], default="alnum",
                        help="Charset for token (default: alnum)")
    parser.add_argument("--prefix", default="CTF", help="Prefix before braces (default: CTF)")
    parser.add_argument("--suffix", default="", help="Suffix to append after token (default: empty)")
    parser.add_argument("--template", default="{prefix}{{{token}}}{suffix}",
                        help="Template for flag. Use {prefix}, {token}, {suffix}. Default: {prefix}{token}{suffix} wrapped in braces.")
    parser.add_argument("-o", "--output", type=str, help="Write flags to file (one per line)")
    parser.add_argument("--unique", action="store_true", help="Ensure generated flags are unique")
    parser.add_argument("--no-braces", action="store_true", help="Don't automatically add braces around token")
    args = parser.parse_args()

    if args.no_braces and args.template == "{prefix}{{{token}}}{suffix}":
        args.template = "{prefix}{token}{suffix}"
    template = args.template

    try:
        flags = generate_flags(args.number, args.length, args.charset, args.prefix, args.suffix, template, args.unique)
    except RuntimeError as e:
        print("ERROR:", e)
        return

    if args.output:
        out_path = Path(args.output)
        out_path.write_text("\n".join(flags) + "\n", encoding="utf-8")
        print(f"Wrote {len(flags)} flags to {out_path}")
    else:
        for f in flags:
            print(f)

if __name__ == "__main__":
    main()
PY