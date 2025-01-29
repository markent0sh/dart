#!/usr/bin/env python3
"""
Create a fake Git commit history based on a 52x7 contribution matrix.

Usage:
    python generate_git_art.py <year> [<matrix_file>]

- <year> (required): e.g., 2022
- <matrix_file> (optional): path to a text file containing the 52x7 matrix.
  If omitted, a demo matrix will be used.

Matrix Format:
- 52 lines, each line has 7 symbols (no spaces), e.g.:
    #$&*...
    #$&*...
    ... (total of 52 lines)
- Each symbol in {#, $, &, *, .}

Symbol → Commits:
- '#' → 0 commits
- '$' → random(1 to 9)   commits
- '&' → random(10 to 19) commits
- '*' → random(20 to 29) commits
- '.' → random(30 to 50) commits
"""

import sys
import os
import random
import datetime
from git import Repo, exc

def load_matrix_from_file(filename):
    """
    Loads a 52x7 matrix from a text file.
    Each line must have exactly 7 characters (no spaces).
    Returns a list of strings, each of length 7.
    """
    matrix = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if len(line) != 7:
                raise ValueError("Each line in the matrix file must have exactly 7 symbols.")
            matrix.append(line)
    if len(matrix) != 52:
        raise ValueError("The matrix file must contain exactly 52 lines.")
    return matrix

def load_demo_matrix():
    """
    Returns a hard-coded 52x7 matrix as an example/demonstration.
    Modify this as desired.
    """
    # For brevity, here's a small repeating pattern that sums to 52 lines.
    # Adjust or replace as you like:
    pattern = [
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
        "#$&*...",
    ]
    # We need 52 lines total. Let's just repeat the 10-line pattern enough times:
    matrix = (pattern * 6)[:52] + [pattern[0]]  # quick hack to reach 52 lines
    matrix = matrix[:52]  # ensure exactly 52
    return matrix

def symbol_to_commit_count(symbol):
    """
    Convert a single symbol into a random commit count based on the specification:
      '#' → 0
      '$' → random(1–9)
      '&' → random(10–19)
      '*' → random(20–29)
      '.' → random(30–50)
    """
    if symbol == '#':
        return 0
    elif symbol == '$':
        return random.randint(1, 9)
    elif symbol == '&':
        return random.randint(10, 19)
    elif symbol == '*':
        return random.randint(20, 29)
    elif symbol == '.':
        return random.randint(30, 50)
    else:
        raise ValueError(f"Invalid symbol '{symbol}'. Must be one of '#', '$', '&', '*', '.'.")

def find_first_sunday(year):
    """
    Find the first Sunday on or after January 1 of the given year.
    Python's weekday() returns:
        Monday=0, Tuesday=1, ... Sunday=6
    So we want a date whose weekday() == 6.
    """
    d = datetime.date(year, 1, 1)
    # If it's not Sunday, move forward until it's Sunday
    while d.weekday() != 6:
        d += datetime.timedelta(days=1)
    return d

def initialize_repo_if_needed(path="."):
    """
    Check if there's a Git repository at the given path.
    If not, initialize one.
    Returns a Repo object.
    """
    try:
        repo = Repo(path)
    except exc.InvalidGitRepositoryError:
        # Not a valid git repo; initialize
        print("[INFO] Initializing new Git repository...")
        repo = Repo.init(path)
    return repo

def make_commits_for_day(repo, day_date, num_commits):
    """
    Make 'num_commits' commits on the specified historical date.
    Modifies (and stages) a dummy file, then commits.
    """
    if num_commits <= 0:
        return  # No commits needed

    # We can fix a specific time (e.g., 12:00) or any time of day:
    # Add a time component (hours, minutes, seconds) for the commit
    commit_datetime = datetime.datetime(
        day_date.year, day_date.month, day_date.day, 12, 0, 0
    )

    # Use an ISO8601-like string for the environment date
    # (GitPython accepts a string for author_date / commit_date)
    commit_date_str = commit_datetime.isoformat()

    dummy_file = os.path.join(repo.working_dir, "dummy_file.txt")

    for i in range(num_commits):
        # Write something to the dummy file
        with open(dummy_file, "a", encoding="utf-8") as f:
            f.write(f"Commit {i+1} on {day_date.isoformat()}\n")

        # Stage changes
        repo.index.add([dummy_file])

        # Make the commit
        repo.index.commit(
            f"Auto commit {i+1}/{num_commits} on {day_date.isoformat()}",
            author_date=commit_date_str,
            commit_date=commit_date_str
        )

def generate_git_art(matrix, year):
    """
    Given a 52x7 matrix of symbols and a year,
    generate commits that reflect the 'heatmap' pattern.
    """
    # Initialize or open the Git repository
    repo = initialize_repo_if_needed(".")

    # Find the first Sunday in the given year
    first_sunday = find_first_sunday(year)

    # We have matrix[0..51], each is a string of length 7
    # matrix[w][d], where w = week index, d = day index (0=Sunday,1=Monday,...6=Saturday)
    for week_idx in range(52):
        week_str = matrix[week_idx]
        if len(week_str) != 7:
            raise ValueError("Invalid row length in matrix; each row must have 7 symbols.")

        for day_idx in range(7):
            symbol = week_str[day_idx]
            commit_count = symbol_to_commit_count(symbol)

            # Date for this cell: first_sunday + (week_idx weeks) + (day_idx days)
            day = first_sunday + datetime.timedelta(weeks=week_idx, days=day_idx)
            make_commits_for_day(repo, day, commit_count)

def main():
    # -------------------------
    # Parse command line args
    # -------------------------
    if len(sys.argv) < 2:
        print("Usage: python generate_git_art.py <year> [<matrix_file>]")
        sys.exit(1)

    try:
        year = int(sys.argv[1])
    except ValueError:
        print("Error: <year> must be an integer.")
        sys.exit(1)

    # ---------------------------------------
    # Load matrix (either from file or demo)
    # ---------------------------------------
    if len(sys.argv) >= 3:
        matrix_file = sys.argv[2]
        print(f"[INFO] Loading matrix from file: {matrix_file}")
        matrix = load_matrix_from_file(matrix_file)
    else:
        print("[INFO] No matrix file provided; using demo matrix.")
        matrix = load_demo_matrix()

    # ---------------------------------------
    # Generate the Git art
    # ---------------------------------------
    print(f"[INFO] Generating git art for year {year}...")
    try:
        generate_git_art(matrix, year)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print("[INFO] Done. Review your commit history with 'git log' or on GitHub after pushing.")

if __name__ == "__main__":
    main()
