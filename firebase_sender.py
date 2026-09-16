import firebase_admin
from firebase_admin import credentials, messaging

SERVICE_ACCOUNT_FILE = "penal-ty-firebase-adminsdk-fbsvc-e521735942.json"

cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)


def send_penalty_notification(title, body, topic):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic=topic
    )

    response = messaging.send(message)

    print("🔔 Notificación enviada:", response)
    return response


if __name__ == "__main__":

    send_penalty_notification(
        "⚽ PENAL.TY",
        "🔥 ¡Un partido va a penales!",
        "copa_argentina"
    )