package com.example.phonelistener

import android.annotation.SuppressLint
import android.content.Context
import android.telephony.TelephonyManager

object DeviceInfo {

    @SuppressLint("MissingPermission")
    fun getPhoneNumber(context: Context): String {
        val telephony = context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
        return telephony.line1Number ?: "unknown"
    }
}
