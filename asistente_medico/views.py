from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone


openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Hola, soy tu asistente médico virtual. Estoy aquí para ayudarte con información sobre tus síntomas. ¿Podrías contarme más sobre lo que estás experimentando? Además, ¿hay alguna condición médica preexistente o medicamento que estés tomando actualmente que deba tener en cuenta para proporcionarte las mejores recomendaciones posibles"},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer
    
def asistente_medico(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('asistente_medico')
        else:
            error_message = 'Usuario invalido o contraseña'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('asistente_medico')
            except:
                error_message = 'Error al crear la cuenta'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'La contraseña no coinciden'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')