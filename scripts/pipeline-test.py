#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline test script — runs as an IAG5 service via iagctl db import"
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Hello from IAG pipeline test!",
        help="Message to print",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="iag5",
        help="Target label for the test run",
    )
    args = parser.parse_args()

    print(f"[pipeline-test] target={args.target}")
    print(f"[pipeline-test] message={args.message}")
    print("[pipeline-test] v2 — pipeline fired successfully")


if __name__ == "__main__":
    main()
