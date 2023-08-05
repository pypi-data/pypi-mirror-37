

import argparse
import sys
import os

from distance import DefaultClasses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--separation', type=float, default=200.0,
                        help="Separation between objects.")
    parser.add_argument('-f', '--force', action='store_true',
                        help="Overwrite output file if it exists.")
    parser.add_argument('OUTPUT',
                        help="Output file name.")
    parser.add_argument('INPUT', nargs='*',
                        help="Customobject files to group.")
    args = parser.parse_args()

    group = DefaultClasses.level_objects.create('Group', children=[])
    position = (len(args.INPUT) - 1) * -.5 * args.separation

    if args.force:
        write_mode = 'wb'
    else:
        write_mode = 'xb'
        if args.OUTPUT != '-' and os.path.exists(args.OUTPUT):
            print(f"Output file already exists. Use -f to overwrite.")
            return 1

    for filename in args.INPUT:
        obj = DefaultClasses.customobjects.read(filename)
        obj.real_transform = obj.real_transform.set(pos=(position, 0, 0))
        group.children.append(obj)
        position += args.separation

    if args.OUTPUT == '-':
        group.write(sys.stdout.buffer)
    else:
        group.write(args.OUTPUT, write_mode=write_mode)

    return 0


if __name__ == '__main__':
    exit(main())


# vim:set sw=4 et:
