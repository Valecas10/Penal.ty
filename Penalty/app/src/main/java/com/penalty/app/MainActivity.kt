package com.penalty.app

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.firebase.messaging.FirebaseMessaging
import com.penalty.app.ui.theme.PenaltyTheme

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        enableEdgeToEdge()

        // 🔔 Permiso de notificaciones
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {

            if (
                ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {

                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                    100
                )
            }
        }

        setContent {
            PenaltyTheme {
                PenaltyApp()
            }
        }
    }
}

fun updateTournamentSubscription(
    topic: String,
    enabled: Boolean
) {
    val task = if (enabled) {
        FirebaseMessaging.getInstance().subscribeToTopic(topic)
    } else {
        FirebaseMessaging.getInstance().unsubscribeFromTopic(topic)
    }

    task.addOnCompleteListener { result ->
        if (result.isSuccessful) {
            Log.d(
                "PENALTY",
                "${if (enabled) "Suscripto a" else "Desuscripto de"} $topic"
            )
        } else {
            Log.e(
                "PENALTY",
                "Error con topic $topic",
                result.exception
            )
        }
    }
}

@Composable
fun PenaltyApp() {

    var ligaArgentina by remember { mutableStateOf(true) }
    var copaArgentina by remember { mutableStateOf(true) }
    var libertadores by remember { mutableStateOf(true) }
    var sudamericana by remember { mutableStateOf(true) }

    Scaffold(
        modifier = Modifier.fillMaxSize()
    ) { innerPadding ->

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {

            Spacer(modifier = Modifier.height(30.dp))

            Text(
                text = "⚽ PENAL.TY",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(20.dp))

            Text(
                text = "🔥 PENALTIES",
                fontSize = 22.sp,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = "Recibí una notificación cuando un partido vaya a penales.",
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(35.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp)
            ) {

                Column(
                    modifier = Modifier.padding(20.dp)
                ) {

                    Text(
                        text = "🏆 TORNEOS",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold
                    )

                    Spacer(modifier = Modifier.height(15.dp))

                    TournamentCheckbox(
                        "Liga Argentina",
                        ligaArgentina
                    ) {
                        ligaArgentina = it
                        updateTournamentSubscription(
                            "liga_argentina",
                            it
                        )
                    }

                    TournamentCheckbox(
                        "Copa Argentina",
                        copaArgentina
                    ) {
                        copaArgentina = it
                        updateTournamentSubscription(
                            "copa_argentina",
                            it
                        )
                    }

                    TournamentCheckbox(
                        "Libertadores",
                        libertadores
                    ) {
                        libertadores = it
                        updateTournamentSubscription(
                            "libertadores",
                            it
                        )
                    }

                    TournamentCheckbox(
                        "Sudamericana",
                        sudamericana
                    ) {
                        sudamericana = it
                        updateTournamentSubscription(
                            "sudamericana",
                            it
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(25.dp))

            Text(
                text = "🔔 Notificaciones activadas",
                fontWeight = FontWeight.Medium
            )
        }
    }
}


@Composable
fun TournamentCheckbox(
    name: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {

    Row(
        verticalAlignment = Alignment.CenterVertically
    ) {

        Checkbox(
            checked = checked,
            onCheckedChange = onCheckedChange
        )

        Spacer(modifier = Modifier.width(8.dp))

        Text(
            text = name,
            fontSize = 17.sp
        )
    }
}