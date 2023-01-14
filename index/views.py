from django.shortcuts import render

# 以下を追加
def index (request):
    return render(request,'index/index.html')