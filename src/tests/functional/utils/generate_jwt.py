import jwt
import time


def generate_token(user_id: str):
    # Установите время жизни токена (в секундах)
    expiration_time = time.time() + 3600  # Например, 1 час

    # Создайте токен с использованием HS256 алгоритма и секретного ключа 'secret'
    token = jwt.encode(
        {
            "exp": expiration_time,
            "user_id": user_id
        },
        'secret',
        algorithm='HS256'
    )

    return token


# Генерировать токен
generated_token = generate_token('3fa85f64-5717-4562-b3fc-2c963f66afa6')

# Вывести сгенерированный токен
print(generated_token)
