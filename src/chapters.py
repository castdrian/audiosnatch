from gazpacho import get, Soup
from urllib.parse import urlparse
from re import search
from os import makedirs, path, sep
from json5 import loads
from src.download import download

SKIP_CHAPTER = 'https://file.tokybook.com/upload/welcome-you-to-tokybook.mp3'
MEDIA_URL = 'https://files01.tokybook.com/audio/'
MEDIA_FALLBACK_URL = 'https://files02.tokybook.com/audio/'

def get_chapters(BOOK_URL):
	html = get(BOOK_URL)

	soup = Soup(html)
	js = soup.find('script')

	for crap in js:
		match = search(r"tracks\s*=\s*(\[[^\]]+\])\s*", crap.text)
		if match:
			string = match.group(1)
			break

	json = loads(string)
	chapters = [{'name': x['name'], 'url': x['chapter_link_dropbox']} for x in json if x['chapter_link_dropbox'] != SKIP_CHAPTER]

	book_path = urlparse(BOOK_URL).path
	download_dir = path.normpath('downloads' + sep + book_path)
	makedirs(download_dir, exist_ok=True)

	for item in chapters:
		download_file = path.join(download_dir, item['name']+'.mp3')
		try:
			download(MEDIA_URL+item['url'], download_file)
			print()
		except RuntimeError:
			try:
				download(MEDIA_FALLBACK_URL+item['url'], download_file)
				print()
			except Exception as e:
				print(f'An error occured: {e}')
				break
		except Exception as e:
			print(f'An error occured: {e}')
			break

