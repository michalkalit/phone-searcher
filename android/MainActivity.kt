package com.example.phonelistener

import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.material3.Text
import androidx.compose.material3.Scaffold
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.phonelistener.ui.theme.PhoneListenerTheme
import com.google.firebase.FirebaseApp
import com.google.firebase.messaging.FirebaseMessaging
import org.json.JSONObject
import android.util.Log

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        FirebaseApp.initializeApp(this)

        Permissions.requestAll(this)

        FirebaseMessaging.getInstance().token.addOnSuccessListener { token ->
            val phone = DeviceInfo.getPhoneNumber(this)

            val json = JSONObject().apply {
                put("token", token)
                put("phoneNumber", phone)
            }

            ApiClient.post("devices", json)
            Log.d("FCM", "Sent token on launch: $token")
        }

        enableEdgeToEdge()
        setContent {
            PhoneListenerTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { padding ->
                    Text("Phone Listener", modifier = Modifier.padding(padding))
                }
            }
        }
    }
}
