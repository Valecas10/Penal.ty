package com.penalty.app

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class PenaltyFirebaseMessagingService : FirebaseMessagingService() {

    override fun onMessageReceived(remoteMessage: RemoteMessage) {

        val title = remoteMessage.data["title"]
            ?: remoteMessage.notification?.title
            ?: "PENAL.TY"

        val body = remoteMessage.data["body"]
            ?: remoteMessage.notification?.body
            ?: "¡Un partido fue a penales!"

        val type = remoteMessage.data["type"] ?: "alert"

        showNotification(
            title = title,
            body = body,
            isAlert = type == "alert"
        )
    }

    private fun showNotification(
        title: String,
        body: String,
        isAlert: Boolean
    ) {

        val channelId = if (isAlert) {
            "penalties_alert"
        } else {
            "penalties_update"
        }

        val notificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE)
                    as NotificationManager

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {

            val importance = if (isAlert) {
                NotificationManager.IMPORTANCE_HIGH
            } else {
                NotificationManager.IMPORTANCE_LOW
            }

            val channel = NotificationChannel(
                channelId,
                if (isAlert) "Alertas de penales" else "Actualizaciones de penales",
                importance
            )

            notificationManager.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setPriority(
                if (isAlert) {
                    NotificationCompat.PRIORITY_HIGH
                } else {
                    NotificationCompat.PRIORITY_LOW
                }
            )
            .setAutoCancel(false)
            .setOnlyAlertOnce(!isAlert)
            .build()

        notificationManager.notify(1, notification)
    }
}