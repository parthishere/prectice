from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .recognizer import RecognizerClass

def index(request):
    	return render(request, 'app/index.html')
 
def face_detact(request):
    return render(request, "app/face-detect.html", {})

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		
def facecam_feed(request):
	return StreamingHttpResponse(gen(RecognizerClass(username='parth', unique_id='parththakkar')),
					content_type='multipart/x-mixed-replace; boundary=frame')