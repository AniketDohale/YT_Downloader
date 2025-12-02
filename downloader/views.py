from django.shortcuts import render
from yt_dlp import YoutubeDL

def download_Video(request):

    if 'download_success' in request.session:
        del request.session['download_success']

    download_Success = False
    video_Info = None
    
    if request.method == 'POST':
        url = request.POST.get('url')
        action = request.POST.get('action')
        print(action)
        
        if url:
            ydl_opts = {
                'format' : 'best',
                'outtmpl' : 'downloads/%(title)s.%(ext)s',
                'quiet' : True,
            }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                if action == 'fetch':
                    info_Dict = ydl.extract_info(url, download=False)
                    video_Info = {
                        'title' : info_Dict.get('title'),
                        'thumbnail' : info_Dict.get('thumbnail'),
                    }

                elif action == 'download':
                   ydl.download([url])
                   download_Success = True

        except Exception as e:
            print(f"Error Downloading Video {e}")
            download_Success = False
    
    return render(request, 'index.html', {'video_Info': video_Info, 'download_Success': download_Success})