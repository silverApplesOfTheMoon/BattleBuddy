from django.shortcuts import render

# Home view for the root URL
def home_view(request):
    return render(request, 'chatbot/home.html')

# Other views...
def chatbot_view(request):
    response = None
    if request.method == "POST":
        query = request.POST.get("query", "")
        response = f"You asked: {query}"  # Placeholder response
    return render(request, 'chatbot/chatbot.html', {"response": response})

def quiz_view(request):
    return render(request, 'chatbot/quiz.html')

def admin_visualization_view(request):
    return render(request, 'chatbot/admin_visualization.html')
