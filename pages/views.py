from django.shortcuts import render
from datetime import datetime

def index(request):
	return render(request, 'pages/index.html', {'time':datetime.now(),})