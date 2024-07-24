#!/usr/bin/env python3
import argparse
import datetime
import sys
import time
from typing import Any, List, Optional


ARG_PARSER = argparse.ArgumentParser()


def parse_args() -> argparse.Namespace:
    ARG_PARSER.add_argument("time", nargs='*', help=(
        "time either could be defined as:\n"
        "1) integer number of seconds;\n"
        "2) integer with 's' for seconds, 'm' for minutes,"
        " 'h' for hours or 'd' for days (like '3s', '2m' and/or '1h');\n"
        "3) target time, '%%H:%%M' or '%%H:%%M:%%S'."
    ))
    ARG_PARSER.add_argument("-c", "--countdown", action='store_true', help=(
        "show interactive countdown"
    ))
    ARG_PARSER.set_defaults(countdown=False)
    args = ARG_PARSER.parse_args()
    return args


ARGS = parse_args()


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


def sleep_til_date(target_date: datetime.datetime) -> None:
    current_date = datetime.datetime.now()
    wait_seconds = (target_date - current_date).total_seconds()
    print(f"Gonna wait for {round(wait_seconds)} seconds (til {target_date.strftime('%H:%M:%S')})")
    if not ARGS.countdown:
        time.sleep(wait_seconds)
    else:
        prev_time = time.time()
        while current_date < target_date:
            seconds_left = round((target_date - current_date).total_seconds())
            write_replace_current_line(datetime.timedelta(seconds=seconds_left))
            time.sleep(1 - (time.time() - prev_time))
            prev_time = time.time()
            current_date = datetime.datetime.now()
        write_replace_current_line('0:00:00')
        print()


def main() -> None:
    current_date = datetime.datetime.now()
    target_date_parts = ARGS.time
    if not target_date_parts:
        raise TimeParsingError("No time provided")
    target_date = None
    if len(target_date_parts) == 1 and ':' in target_date_parts[0]:
        target_date = parse_exact_time(target_date_parts[0], current_date=current_date)
    else:
        target_date = parse_time_delta(target_date_parts, current_date=current_date)
    if not target_date:
        raise TimeParsingError(f"Can't parse the date/time: \"{' '.join(target_date_parts)}\'")
    sleep_til_date(target_date)


def cli() -> None:
    try:
        main()
    except TimeParsingError as exc:
        print(exc)
        print()
        ARG_PARSER.print_help()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nReceived SIGINT. Cancelling the timer.")
        sys.exit(130)


if __name__ == "__main__":
    cli()
