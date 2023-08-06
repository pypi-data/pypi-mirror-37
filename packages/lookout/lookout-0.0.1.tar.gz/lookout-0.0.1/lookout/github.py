#!/usr/bin/env python3

import github


def main() -> None:
    g = github.Github()
    repo = g.get_repo("libffi/libffi")
    for r in repo.get_releases():
        print(r.tag_name, r)
        for a in r.get_assets():
            print("asset", a.name, a.browser_download_url)
    for t in repo.get_tags():
        print(t)


if __name__ == "__main__":
    main()
