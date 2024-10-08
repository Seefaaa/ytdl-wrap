import datetime
from typing import Optional


def list_to_string(items: list[str]) -> Optional[str]:
	if not items:
		return ""
	match len(items):
		case 1:
			return items[0]
		case 2:
			return f"{items[0]} and {items[1]}"
		case _:
			return ", ".join(items[:-1]) + f", and {items[-1]}"


def try_find_artist(info: dict[str, any]) -> Optional[str]:
	if "artists" in info:
		return list_to_string(info["artists"])
	elif "creators" in info:
		return list_to_string(info["creators"])
	else:
		return None


def try_find_channel(info: dict[str, any]) -> Optional[str]:
	if "channel" in info:
		return info["channel"]
	elif "uploader" in info:
		return info["uploader"]
	else:
		return None


# From https://stackoverflow.com/a/50992575
def make_ordinal(n: int) -> str:
	n = int(n)
	if 11 <= (n % 100) <= 13:
		suffix = "th"
	else:
		suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
	return str(n) + suffix


def format_date(date_string: str) -> Optional[str]:
	if not date_string:
		return None
	try:
		date = datetime.strptime(date_string, "%Y%m%d")
		return date.strftime("%B {}, %Y").format(make_ordinal(date.day))
	except Exception:
		return None
