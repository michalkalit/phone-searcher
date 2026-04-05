object ApiClient {

    private val http = OkHttpClient()
    private const val JSON = "application/json"

    private val baseUrl: String
        get() = BuildConfig.API_BASE_URL

    fun post(path: String, json: JSONObject) {
        val body = json.toString().toRequestBody(JSON.toMediaType())

        val request = Request.Builder()
            .url("$baseUrl/$path")
            .post(body)
            .build()

        http.newCall(request).enqueue(loggingCallback("POST"))
    }

    fun put(path: String, json: JSONObject) {
        val body = json.toString().toRequestBody(JSON.toMediaType())

        val request = Request.Builder()
            .url("$baseUrl/$path")
            .put(body)
            .build()

        http.newCall(request).enqueue(loggingCallback("PUT"))
    }

    private fun loggingCallback(method: String) = object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            Log.e("HTTP", "$method failed: ${e.message}")
        }

        override fun onResponse(call: Call, response: Response) {
            Log.d("HTTP", "$method response: ${response.body?.string()}")
        }
    }
}
