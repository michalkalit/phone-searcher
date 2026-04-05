package com.example.phonelistener

import android.Manifest
import android.annotation.SuppressLint
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.phonelistener.ui.theme.PhoneListenerTheme
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.location.Location
import android.os.Build
import android.telephony.SmsMessage
import android.telephony.TelephonyManager
import android.util.Log
import androidx.annotation.RequiresPermission
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.android.gms.location.LocationServices
import com.google.firebase.FirebaseApp
import com.google.firebase.messaging.FirebaseMessaging
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import okhttp3.Call
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException
import okhttp3.Callback
import java.net.URLEncoder

class MainActivity : ComponentActivity() {
        override fun onCreate(savedInstanceState: Bundle?) {
            super.onCreate(savedInstanceState)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                requestPermissions(arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 1)
            }

            FirebaseApp.initializeApp(this)

            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.READ_PHONE_STATE,
                    Manifest.permission.READ_PHONE_NUMBERS,
                    Manifest.permission.READ_SMS
                ),
                101
            )
            FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    val token = task.result
                    Log.d("FCM", "Token on app launch: $token")

                    // Send to backend on every app launch
                    sendTokenToBackend(this, token)

                } else {
                    Log.w("FCM", "Failed to get token on launch", task.exception)
                }
            }






            enableEdgeToEdge()
            setContent {
                PhoneListenerTheme {
                    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                        Greeting(
                            name = "Android",
                            modifier = Modifier.padding(innerPadding)
                        )
                    }
                }
            }

            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                ),
                101
            )


            if (ContextCompat.checkSelfPermission(
                    this,
                    Manifest.permission.RECEIVE_SMS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.RECEIVE_SMS),
                    101
                )
            }


        }
    }
@SuppressLint("MissingPermission")
fun getPhoneNumber(context: Context): String? {
    val telephony = context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
    return telephony.line1Number // may return null on some carriers
}

fun sendTokenToBackend(context: Context, token: String) {
    val phoneNumber = getPhoneNumber(context) ?: "unknown"

    val json = JSONObject().apply {
        put("token", token)
        put("phoneNumber", phoneNumber)
    }

    val requestBody = json.toString()
        .toRequestBody("application/json".toMediaType())

    val request = Request.Builder()
        .url("https://0dmcl4x3y1.execute-api.us-west-2.amazonaws.com/Development/devices")
        .post(requestBody)
        .build()


    OkHttpClient().newCall(request).enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            Log.e("HTTP", "Request failed: ${e.message}")
        }

        override fun onResponse(call: Call, response: Response) {
            Log.d("HTTP", "Response: ${response.body?.string()}")
        }
    })
}

    @Composable
    fun Greeting(name: String, modifier: Modifier = Modifier) {
        Text(
            text = "Hello $name!",
            modifier = modifier
        )
    }


    class MyFirebaseMessagingService : FirebaseMessagingService() {


        override fun onCreate() {
            super.onCreate()

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                val channel = NotificationChannel(
                    "default",
                    "Default Channel",
                    NotificationManager.IMPORTANCE_HIGH
                )
                val manager = getSystemService(NotificationManager::class.java)
                manager.createNotificationChannel(channel)
            }
        }


        override fun onNewToken(token: String) {
            super.onNewToken(token)
            Log.d("FCM", "Refreshed token: $token")

            // you can drop phoneNumber entirely if you want
            val json = JSONObject().apply {
                put("token", token)
            }

            val requestBody = json.toString().toRequestBody("application/json".toMediaType())
            val request = Request.Builder()
                .url("https://0dmcl4x3y1.execute-api.us-west-2.amazonaws.com/Development/devices")
                .post(requestBody)
                .build()

            OkHttpClient().newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    Log.e("HTTP", "Request failed: ${e.message}")
                }

                override fun onResponse(call: Call, response: Response) {
                    Log.d("HTTP", "Response: ${response.body?.string()}")
                }
            })
        }

        // ✅ Handle incoming FCM message
        @RequiresPermission(allOf = [Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION])
        override fun onMessageReceived(remoteMessage: RemoteMessage) {
            remoteMessage.notification?.let {
                val title = it.title
                val body = it.body
                Log.d("FCM", "Notification - Title: $title, Body: $body")
            }

            if (remoteMessage.data.isNotEmpty()) {
                val action = remoteMessage.data["action"]
                val phoneNumber = remoteMessage.data["phoneNumber"]

                Log.d("FCM", "Data - Action: $action, User ID: , Phone: $phoneNumber")

                if (action == "get-gps") {
                    sendDeviceGps(phoneNumber)
                }
            }
        }

        @SuppressLint("MissingPermission")
        private fun sendDeviceGps(phoneNumber: String?) {

            if (phoneNumber == null) {
                Log.e("HTTP", "Missing phone number")
                return
            }

            // Generate random coordinate inside Israel
            val lat = 29.45 + Math.random() * (33.33 - 29.45)
            val lon = 34.27 + Math.random() * (35.78 - 34.27)

            val json = JSONObject().apply {
                put("latitude", lat)
                put("longitude", lon)
            }

            val requestBody = json
                .toString()
                .toRequestBody("application/json; charset=utf-8".toMediaType())


            // Encode +1555... → %2B1555...
            val encodedPhone = URLEncoder.encode(phoneNumber, "UTF-8")

            val url =
                "https://0dmcl4x3y1.execute-api.us-west-2.amazonaws.com/Development/devices/${encodedPhone}/location"

            val httpRequest = Request.Builder()
                .url(url)
                .put(requestBody)
                .header("Content-Type", "application/json")
                .build()


            OkHttpClient().newCall(httpRequest).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    Log.e("HTTP", "GPS Request failed: ${e.message}")
                }

                override fun onResponse(call: Call, response: Response) {
                    val body = response.body?.string()
                    Log.i("HTTP", "GPS Response: $body")
                }
            })
        }



    }


