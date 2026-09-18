import firebase_admin
from firebase_admin import credentials, messaging

SERVICE_ACCOUNT_FILE = "penal-ty-firebase-adminsdk-fbsvc-e521735942.json"

cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)


def send_penalty_notification(
    title,
    body,
    topic,
    notification_type="alert",
    match_id=None
):
    data = {
        "title": title,
        "body": body,
        "type": notification_type,
    }

    if match_id is not None:
        data["match_id"] = str(match_id)

    message = messaging.Message(
        data=data,
        topic=topic,
        android=messaging.AndroidConfig(
            priority="high"
        )
    )

    response = messaging.send(message)

    print("🔔 Notificación enviada:", response)

    return response


if __name__ == "__main__":
    send_penalty_notification(
        "PENAL.TY",
        "¡Un partido va a penales!",
        "copa_argentina",
        notification_type="alert",
        match_id="test"
    )