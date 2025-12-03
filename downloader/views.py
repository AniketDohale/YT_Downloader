from django.shortcuts import render
from yt_dlp import YoutubeDL

def download_Video(request):

    if 'download_success' in request.session:
        del request.session['download_success']

    download_Success = False
    video_Info = None
    formats = None
    
    if request.method == 'POST':
        url = request.POST.get('url')
        action = request.POST.get('action')
        selected_Format = request.POST.get('format_id')
        print(action)
        
        if url:
            ydl_opts = {
                # 'format' : 'best',
                # 'outtmpl' : 'downloads/%(title)s.%(ext)s',
                'quiet' : True,
                'skip_download' : True,
            }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_Dict = ydl.extract_info(url, download=False)

                if action == 'fetch':
                    video_Info = {
                        'title' : info_Dict.get('title'),
                        'thumbnail' : info_Dict.get('thumbnail'),
                    }

                    formats = []
                    for f in info_Dict.get('formats', []):
                        formats.append({
                            'format_id': f.get('format_id'),
                            'ext': f.get('ext'),
                            'resolution': f.get('resolution') or f.get('height'),
                            'fps': f.get('fps'),
                            'filesize': f.get('filesize'),
                            'video_codec': f.get('vcodec'),
                            'audio_codec': f.get('acodec'),
                        })

                elif action == 'download' and selected_Format:
                   ydl_opts = {
                       'format' : selected_Format,
                       'outtmpl' : 'downloads/%(title)s.%(ext)s',
                   }

                   with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                   download_Success = True
                
                else:
                    print("No Valid Action or Format Selected..")

        except Exception as e:
            print(f"Error Downloading Video {e}")
            download_Success = False
    
    return render(request, 'index.html', {'video_Info': video_Info, 'formats': formats, 'download_Success': download_Success})