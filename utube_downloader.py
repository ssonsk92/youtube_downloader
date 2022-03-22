from pytube import YouTube

#on_progress_callbak(stream, chunk, remain)

def download_youtube(url:str, output_path:str, progress_callback):
    print("url: %s, output_path: %s " %(url, output_path))
    yt = YouTube(url, progress_callback)
    #print("title %s" %yt.title)
    print(yt.streams)
    stream = yt.streams.get_by_itag(22)
    stream.download(output_path, yt.title + '.mp4')