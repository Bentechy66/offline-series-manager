from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from config import video_path, opensubtitles_username, opensubtitles_password
from utils import log
from os import path

def main(video):
    log("info", "Loaded module subtitles")
    # Logging in to OST
    log("info", "Logging in to OpenSubtitles")
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
        log("critical", "Could not find specified video file '" + file_path + "'")
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
    subtitle_id = data[0]["IDSubtitleFile"]
    log("info", "Attempting download of subtitles with ID " + str(subtitle_id))
    try:
        if isinstance(ost.download_subtitles([subtitle_id], override_filenames={subtitle_id: video + '.srt'}, output_directory=video_path, extension='srt'), dict):
            log("success", "Subtitles successfully downloaded. Enjoy your video!")
        else:
            log("critical", "Subtitle download failed.")
            return
    except:
        #TODO: Make neater
        log("error", "Something went wrong. Trying second option in list(?)")
        subtitle_id = data[1]["IDSubtitleFile"]
        log("info", "Attempting download of subtitles with ID " + str(subtitle_id))
        try:
            if isinstance(ost.download_subtitles([subtitle_id], override_filenames={subtitle_id: video + '.srt'}, output_directory=video_path, extension='srt'), dict):
                log("success", "Subtitles successfully downloaded. Enjoy your video!")
            else:
                log("critical", "Subtitle download failed.")
                return
        except:
            log("critical", "giving up after too many tries")
            return



if __name__ == "__main__":
    main()
