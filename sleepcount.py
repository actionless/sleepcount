#!/usr/bin/env python3
import argparse
import datetime
import sys
import time
from typing import Any, List, Optional


def parse_args() -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
    )
    arg_parser.add_argument("time", nargs='*', help=(
        "time either could be defined as:\n"
        "1) integer number of seconds;\n"
        "2) integer with 's' for seconds, 'm' for minutes,"
        " 'h' for hours or 'd' for days (like '3s', '2m' and/or '1h');\n"
        "3) target time, '%%H:%%M' or '%%H:%%M:%%S'."
    ))
    arg_parser.add_argument("-c", "--countdown", action='store_true', help=(
        "show interactive countdown"
    ))
    arg_parser.add_argument("-t", "--update-title", type=int, default=1, help=(
        "update terminal title (default=1)"
    ))
    arg_parser.add_argument("-tp", "--title-prefix", default="", help=(
        "terminal title cuontdown prefix (default empty)"
    ))
    arg_parser.add_argument("-ts", "--title-postfix", default="", help=(
        "terminal title cuontdown postfix (default empty)"
    ))
    arg_parser.add_argument("-td", "--title-done", default="👌😸", help=(
        "terminal title when done (default=`👌😸`)"
    ))
    arg_parser.set_defaults(countdown=False)
    args = arg_parser.parse_args()
    return args, arg_parser


class TimeParsingError(Exception):
    pass


def parse_exact_time(
        time_string: str,
        current_date: datetime.datetime,
) -> Optional[datetime.datetime]:
    result = None
    for format_string in ('%H:%M', '%H:%M:%S'):
        try:
            result = datetime.datetime.strptime(time_string, format_string)
            result = result.replace(
                year=current_date.year,
                month=current_date.month,
                day=current_date.day,
                tzinfo=current_date.tzinfo
            )
            if result < current_date:
                result = result.replace(day=result.day + 1)
            break
        except ValueError:
            pass
    return result


def parse_time_delta(
        time_parts: List[str],
        current_date: datetime.datetime,
) -> Optional[datetime.datetime]:
    result = current_date

    def add_time_part(prop: str, delta: int) -> datetime.datetime:
        if prop in found_properties:
            raise TimeParsingError(
                f'Duplicated {prop} in time definition: "{" ".join(time_parts)}"'
            )
        found_properties.append(prop)
        return result + datetime.timedelta(**{prop: delta})

    found_properties: List[str] = []
    for time_part in time_parts:
        try:
            value = int(time_part)
            result = add_time_part('seconds', value)
            continue
        except ValueError:
            pass
        for postfix, property_name in (
                ('d', 'days'),
                ('h', 'hours'),
                ('m', 'minutes'),
                ('s', 'seconds'),
        ):
            if time_part.lower().endswith(postfix):
                result = add_time_part(property_name, int(
                    time_part.lower().rstrip(postfix)
                ))

    if len(found_properties) != len(time_parts):
        return None
    return result


def write_replace_current_line(text: Any) -> None:
    esc = chr(27)
    sys.stdout.write(
        f'{esc}[2K{esc}[\rb{text} '
    )
    sys.stdout.flush()


def update_title(title: str) -> None:
    #         # sys.stdout.write(f"\033]0;test{i}\007")
    sys.stdout.write(f"\x1b]2;{title}\x07")
    sys.stdout.flush()


def sleep_til_date(
        target_date: datetime.datetime,
        *,
        countdown: bool = False,
        update_terminal_title: bool = False,
        title_prefix: str = "",
        title_postfix: str = "",
        title_done: str = "👌😸",
) -> None:
    current_date = datetime.datetime.now()
    wait_seconds = (target_date - current_date).total_seconds()
    print(f"Gonna wait for {round(wait_seconds)} seconds (til {target_date.strftime('%H:%M:%S')})")
    if not countdown:
        if wait_seconds > 0:
            time.sleep(wait_seconds)
    else:
        prev_time = time.time()
        while current_date < target_date:
            seconds_left = round((target_date - current_date).total_seconds())
            text_to_write = str(datetime.timedelta(seconds=seconds_left))
            write_replace_current_line(text_to_write)
            if update_terminal_title:
                update_title(f"{title_prefix}{text_to_write}{title_postfix}")
            to_sleep = 1 - (time.time() - prev_time)
            if to_sleep > 0:
                time.sleep(to_sleep)
            prev_time = time.time()
            current_date = datetime.datetime.now()
        write_replace_current_line('0:00:00')
        if update_terminal_title:
            update_title(title_done)
        print()


def main(args: argparse.Namespace) -> None:
    current_date = datetime.datetime.now()
    target_date_parts = args.time
    if not target_date_parts:
        raise TimeParsingError("No time provided")
    target_date = None
    if len(target_date_parts) == 1 and ':' in target_date_parts[0]:
        target_date = parse_exact_time(target_date_parts[0], current_date=current_date)
    else:
        target_date = parse_time_delta(target_date_parts, current_date=current_date)
    if not target_date:
        raise TimeParsingError(f"Can't parse the date/time: \"{' '.join(target_date_parts)}\'")
    sleep_til_date(
        target_date,
        countdown=args.countdown,
        update_terminal_title=args.update_title,
        title_prefix=args.title_prefix,
        title_postfix=args.title_postfix,
        title_done=args.title_done,
    )


def cli() -> None:
    args, arg_parser = parse_args()
    try:
        main(args)
    except TimeParsingError as exc:
        print(exc)
        print()
        arg_parser.print_help()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nReceived SIGINT. Cancelling the timer.")
        sys.exit(130)


if __name__ == "__main__":
    cli()
