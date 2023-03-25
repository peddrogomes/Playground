/*

Pedro Gomes

18-10-2022

*/
#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClientSecureBearSSL.h>

#include <Arduino_JSON.h>
#include "secrets.h"

ESP8266WiFiMulti WiFiMulti;

#include <Adafruit_SSD1306.h>
#include <U8g2_for_Adafruit_GFX.h>

Adafruit_SSD1306 display(/*MOSI*/ D7, /*CLK*/ D5, /*DC*/ D1, /*RESET*/ D3, /*CS*/ D8);
U8G2_FOR_ADAFRUIT_GFX u8g2_for_adafruit_gfx;

void setup() {
  // display.clearDisplay();
  Serial.begin(115200);
  // Serial.setDebugOutput(true);
  Serial.println();
  Serial.println();
  Serial.println();

  display.begin(SSD1306_SWITCHCAPVCC);
  u8g2_for_adafruit_gfx.begin(display);  
  
  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);

  }


  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(SECRET_SSID, SECRET_PASS);


}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);

    //client->setFingerprint(fingerprint);
    // Or, if you happy to ignore the SSL certificate, then use the following line instead:
    client->setInsecure();

    HTTPClient https;

    //Serial.print("[HTTPS] begin...\n");
    if (https.begin(*client, "https://www.asaas.com/api/v3/finance/balance")) {  // HTTPS

      https.addHeader("Content-Type", "application/json");
      https.addHeader("access_token", access_token);
//      Serial.print("[HTTPS] GET...\n");
      // start connection and send HTTP header
      int httpCode = https.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTPS] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = https.getString();

//          Serial.println(payload);
          payload = payload.substring(11,payload.length()-1);
          float saldo = payload.toFloat();
          Serial.println(saldo); //remove o "{"balance":"

          display.clearDisplay();                               // clear the graphcis buffer  
          u8g2_for_adafruit_gfx.setFont(u8g2_font_helvR14_tf);  // select u8g2 font from here: https://github.com/olikraus/u8g2/wiki/fntlistall
          u8g2_for_adafruit_gfx.setFontMode(3);                 // use u8g2 transparent mode (this is default)
          u8g2_for_adafruit_gfx.setFontDirection(0);            // left to right (this is default)
          u8g2_for_adafruit_gfx.setForegroundColor(WHITE);      // apply Adafruit GFX color
          //u8g2_for_adafruit_gfx.setCursor(0,10);                // start writing at this position
          u8g2_for_adafruit_gfx.setCursor(10,22);   
          u8g2_for_adafruit_gfx.print("Saldo: ");
          //u8g2_for_adafruit_gfx.setFontMode(3);   
          //u8g2_for_adafruit_gfx.setCursor(10,22);                // start writing at this position
          u8g2_for_adafruit_gfx.print(saldo);
          display.display();

        }
      } else {
        Serial.printf("[HTTPS] GET... failed, error: %s\n", https.errorToString(httpCode).c_str());
      }

      https.end();
    } else {
      Serial.printf("[HTTPS] Unable to connect\n");
    }
  }

  Serial.println("Wait 2s before next round...");
  delay(2000);

}
