from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User


openai_api_key = 'API-KEYS'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Soy tu asistente médico virtual, aquí para brindarte información sobre tus síntomas. ¿Podrías compartir más detalles sobre lo que estás experimentando? También, ¿tienes alguna condición médica preexistente o estás tomando algún medicamento en este momento que deba tener en cuenta para ofrecerte las mejores recomendaciones?Quiero resaltar que puedo proporcionarte opciones que incluyan recetas naturales venezolanas, así como medicamentos y tratamientos disponibles en Venezuela. Estaré enfocado en brindarte información relevante y accesible para tu ubicación. Si es necesario, puedo sugerir hasta tres medicamentos de origen natural (si existen) y tres de origen de venta libre, cuyos componentes sean similares o que tengan propiedades efectivas para tratar los síntomas que estás experimentando. ¿En qué más puedo ayudarte"},
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
