from django.shortcuts import render
from yt_dlp import YoutubeDL

def download_Video(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            ydl_opts = {
                'format' : 'best',
                'outtmpl' : 'downloads/%(title)s.%(ext)s',
            }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return render(request, 'download_Complete.html')
    
    return render(request, 'index.html')