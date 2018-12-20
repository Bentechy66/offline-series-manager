from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from config import video_path, opensubtitles_username, opensubtitles_password
from utils import log
from os import path

def main(video):
    log("info", "Loaded module subtitles")
    # Logging in to OST
    log("info", "Logging in to OST")
    ost = OpenSubtitles()
    token = ost.login(opensubtitles_username, opensubtitles_password)
    if isinstance(token, str):
        log("success", "Logged in to OpenSubtitles")
    else:
        log("critical", "Invalid username / password entered")
        return

    # Opening File
    file_path = video_path + video
    if not path.exists(file_path):
        log("critical", "Could not find specified video file")
        return

    # Hashing file
    log("info", "Generating video hash...")
    f = File(file_path)
    hash = f.get_hash()
    log("success", "File hash generated: " + hash)

    # Searching OST
    log("info", "Querying OpenSubtitles for subtitles...")
    data = ost.search_subtitles([{'sublanguageid': 'all', 'moviehash': hash}])
    if len(data) > 0:
        log("success", f"Found {len(data)} results.")
    else:
        log("warning", "No results found.")
        # TODO: Implement series and episode-based downloading
        return



if __name__ == "__main__":
    main()
