package com.example.phonelistener

import android.annotation.SuppressLint
import android.util.Log
import org.json.JSONObject
import java.net.URLEncoder
import kotlin.random.Random

object LocationSender {

    @SuppressLint("MissingPermission")
    fun sendRandomLocation(phoneNumber: String) {

        val lat = Random.nextDouble(29.45, 33.33)
        val lon = Random.nextDouble(34.27, 35.78)

        val json = JSONObject().apply {
            put("latitude", lat)
            put("longitude", lon)
        }

        val encoded = URLEncoder.encode(phoneNumber, "UTF-8")
        ApiClient.put("devices/$encoded/location", json)

        Log.i("GPS", "Sent random location for $phoneNumber")
    }
}
