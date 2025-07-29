from typing import Dict
from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import re
import os
import sys
import multiprocessing
import util

app = FastAPI()
yt_id_regex = re.compile(r"^[a-zA-Z0-9_-]{11}$")


class Media(BaseModel):
	url: str
	opts: Dict = {
		"format": "bestaudio[ext=mp3]/best[ext=mp4][height <= 360]/bestaudio[ext=m4a]/bestaudio[ext=aac]",
		"geo_bypass": True,
		"geo_bypass_country": "US",
		"noplaylist": True,
		"wait_for_video": False,
		"encoding": "utf-8",
		"extractor_args": {"youtube": {"lang": "en", "skip": ["translated_subs"]}},
	}


@app.get("/get")
def get(media: Media):
	url = (
		f"https://www.youtube.com/watch?v={media.url}"
		if yt_id_regex.match(media.url)
		else media.url
	)
	with YoutubeDL({"color": "never", **media.opts}) as ydl:
		try:
			info = ydl.extract_info(url, download=False)
		except DownloadError as err:
			raise HTTPException(status_code=404, detail=str(err))
		data = {
			"title": info["title"],
			"webpage_url": info.get("webpage_url", url),
			"sound_url": info["url"],
			"duration": info["duration"],
			"start": info.get("start_time", 0),
			"end": info.get("end_time", info["duration"]),
			"upload_date": util.format_date(info.get("upload_date", None)),
			"channel": util.try_find_channel(info),
			"artist": util.try_find_artist(info),
			"album": info.get("album", None),
			"track": info.get("track", None),
		}
		return data


if __name__ == "__main__":
	load_dotenv()
	host = os.getenv("host", "0.0.0.0")
	port = int(sys.argv[1] or os.getenv("port", 8000))
	multiprocessing.freeze_support()
	uvicorn.run(app, host=host, port=port, reload=False, workers=1)
