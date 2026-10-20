"""Package and verify repository resources without a game installation."""
import sys

from localization import release_pack


def main():
    try:
        release_pack.build('build')
        release_pack.check(include_installed=False)
    except Exception as error:
        print(f'Build failed: {error}', file=sys.stderr)
        return 1
    print(f'Build complete. Open: {release_pack.DIST}')
    print(f'Install bundle: {release_pack.INSTALL_ZIP.name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
