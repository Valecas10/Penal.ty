import firebase_admin
from firebase_admin import credentials, messaging

SERVICE_ACCOUNT_FILE = "penal-ty-firebase-adminsdk-fbsvc-e521735942.json"

cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)


def send_penalty_notification(title, body):

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),

        # Por ahora enviamos a todos los usuarios suscriptos
        topic="penalties"
    )

    response = messaging.send(message)

    print("🔔 Notificación enviada:", response)


if __name__ == "__main__":

    send_penalty_notification(
        "⚽ PENAL.TY",
        "🔥 ¡Un partido va a penales!"
    )