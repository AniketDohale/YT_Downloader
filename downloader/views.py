from django.shortcuts import render
from yt_dlp import YoutubeDL

def download_Video(request):

    if 'download_success' in request.session:
        del request.session['download_success']

    download_Success = False
    if request.method == 'POST':
        url = request.POST.get('url')
        
        if url:
            ydl_opts = {
                'format' : 'best',
                'outtmpl' : 'downloads/%(title)s.%(ext)s',
            }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            download_Success = True

        except Exception as e:
            print(f"Error Downloading Video {e}")
            download_Success = False
    
    return render(request, 'index.html', {'download_Success': download_Success})