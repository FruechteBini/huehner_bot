#!/usr/bin/python
# -*- coding: utf-8 -*-
import Adafruit_DHT
import time
import logging
import os
import threading
import datetime
import telegram
import subprocess

from telegram.ext import Updater, CommandHandler

# Sensor should be set to Adafruit_DHT.DHT11,
sensor = Adafruit_DHT.DHT11

pin = 4

log = ""

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

def check_sensor(update, context):
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print("temp read.")
    except:
        update.message.reply_text("Da stimmt was beim Sensor nicht. Aber der IT-Daddy ist sicher schon dran...")
        print("exception")
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        update.message.reply_text("Hühnertemperatur: {} *C\nFeuchtigkeit: {}%".format(temperature, humidity))
        return temperature, humidity
    else:
        print('Failed to get reading. Try again!')

def log_sensor_data():
    global log
    prev_logged_hour = 0
    prev_report_hour = 0
    while True:
        now = datetime.datetime.now()
        if now.hour % 1 is 0 and prev_logged_hour is not now.hour:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None:
                try:
                    file = open("log.txt","a")
                    log = ("\nAm {}.{} um {}:{} Uhr:\nTemperatur: {} *C\nFeuchtigkeit: {}%\n".format(now.day, now.month, now.hour, now.minute, temperature, humidity))
                    file.write(log)
                    file.close()
                    prev_logged_hour = now.hour
                    prev_logged_day = now.day
                    print(log)
                    time.sleep(600)
                except:
                    continue
def empty_log(update, context):
    global log
    try:
        file = open("log.txt", "w+")
        file.write(" ")
        file.close()
        update.message.reply_text("log of temp and humidity now empty.")
    except:
        return 0

def get_temp_log(update, context):
    try:
        with open("log.txt", "r") as file:
            temp_log = file.read()
            update.message.reply_text(temp_log)
            print(temp_log)
    except:
        update.message.reply_text("sorry, Bruder! Der Sensor is grad beschäftigt, probiers nachher nochmal!")
        return 0
def start(update, context):
    update.message.reply_text('Hi!\nWillkommen beim Gtown-Hühnerbot.\n\nKommandos sind Tanjas Stärke, die hat da was vorbereitet:\n\n\
    - Tippe /stream für den Stream-Link (wir sind hier live: https://www.twitch.tv/huehnerstasi \n\
    - Tippe /temp für die aktuelle Temperatur und Feuchtigkeit.\n\
    - Tippe /sensor für den Sensor Log der letzten Tage.\n\
    - Tippe /info für eine Übersicht unserer Hühner.\n\
    - Tippe /info_bogdan , um mehr über Bogdan zu erfahren (nichts für schwache Nerven)\n\
    - Tippe /info_flash , um mehr über Flash zu erfahren (kurz und knapp)\n\
    - Tippe /info_tanja , um mehr über Tanja zu erfahren (ACHTUNG: Gossip)')

def info(update, context):
    update.message.reply_text("Wir sind Bogdan, Flash und Tanja, drei Drufflerhauben aus Gräfelfing und haben Bog Bog Bog unser Leben mit euch zu teilen!\n\
    Unsere Daddys sind Mazze, Sebi und  Korbi, drei stabile Dudes im besten Alter.\n\
 Und übrigens: Es ist ganz normal bei uns Hühnern, drei Papas zu haben.\n\
\n\
Mit /info_bogdan, /info_flash, /info_tanja könnt ihr mehr über unseren bisherigen Lebensweg und Charakter erfahren.")  

def info_bog(update, context):
    update.message.reply_text("Bogdan wollte nicht interviewt werden, deshalb übernehmen wir hier, die Daddys.\n\
Über Bogdans Vergangenheit ist wenig bekannt. Er bleibt in dieser Hinsicht auch stets stumm. Spricht man ihn darauf an, zieht er sich schnell in den Hühnerstall zurück.\n\
Was wir bisher herausfinden konnten: Bogdan ist auf jeden Fall osteuropäischer Herkunft.\n\
Wir schätzen sein Alter auf irgendwas zwischen 12 und 50 und vermuten, dass er nicht nur im Jugoslawien-Krieg mitgekämpft hat, sondern für dessen Ausbruch maßgeblich verantwortlich war.\n\
Derartige Vermutungen konnten im Zuge schlafwandlerischer Aktivitäten Bogdans durchsickern.\n\
Das Messer unter Bogdans Heukissen stützt die Spekulation auf eine dunkle Vergangenheit.\n\
Die abgewetzten Krallen zeugen wohl von einer knochenharten Flucht zu Fuß.\n\
Seine Obrigkeitshörigkeit hat wohl im Zuge einer für ihn enttäuschend endenden Machtregimeperiode eklatant gelitten.\n\
Bogdan hört einfach nicht auf uns!")

def info_tan(update, context):
    update.message.reply_text("Reporter: Hallo liebe Tanja, schön, dass du da bist. Wie geht es dir?\n\
\n\
Tanja: Hayy, ja voll gut geht's mir, ich freu mich auch totaaal.\n\
\n\
Reporter: Erzählen sie doch mal etwas über sich!\n\
\n\
Tanja:Aaaalso, mein Name ist Tanja, die Jungs nennen mich aber immer Tyrannja, obwohl ich ihnen immer und immer wieder sage, dass sie das lassen sollen. Die sind so kindisch, aber ich mag sie trotzdem. Man könnte schon sagen, dass ich hier immer ein bisschen die Mama spielen muss. Neben aufmunternden Worten bin ich auch für die gebügelten Hemden und fleckenfreien Sporthosen von den Jungs zuständig.\n\
Aber ich mach das total gern, weil ich weiß ja, dass die Jungs total dankbar dafür sind - auch wenn sie das ruhig mal öfter zeigen könnten.\n\n\
Freitags skype ich immer mit meiner Freundin Lissie aus Erding, wir kennen uns schon seit Kükentagen. Wir sind zusammen durch dick und dünn gegangen - wobei - eine Zeitlang standen wir mal beide auf den stattlichen Johahn, da knirschte es dann schon mal etwas im Gebälk, wir haben uns aber wieder zusammengerauft. Ich würde schon sagen, dass sie meine ABF ist. Bei Lissie kann ich mich auch immer gut über die Jungs beschweren und mal ordentlich Dampf ablassen.\n\n\
Am liebsten - wenn denn mal Ruhe ist im Gehege - liege ich im Sandkasten und pflege mein Gefieder mit diversen Kosmetikprodukten (habe gehört Johahn soll wieder in der Stadt sein - davon erzähle ich Lissie aber lieber nichts, hihi).")


def info_flash(update, context):
    update.message.reply_text("Reporter: Hi Flash, wie geht es dir heute?\n\
\n\
Flash: Hi..ja voll gut ehm aber ich muss auch gleich wieder weiter..gleich geht die Klappe auf und da muss ich vor Bogdan sein, weil der braucht immer so eeeewig dadurch..gleich kommt der neue Kompost und ich hatte schon acht Stunden keinen Kaffeesatz..ich lieeebe Kaffeesatz..zum Glück bin ich hier ja der fitte..nachm Kaffeesatz jogge ich meistens mehrmals den Gehegezaun entlang um anschließend nach gains im Kompost zu suchen..ich lieeebe den Kompost. Bogdan und Tanja meinen immer, dass ich mal mehr chillen sollte. Seh ich nicht ein. Oha, die Klappe geht auf, tschüss auch!")

def get_stream(update, context):
    update.message.reply_text("Wir sind hier (meistens) live: https://www.twitch.tv/huehnerstasi")
def main():
    time.sleep(30)
    t1 = threading.Thread(target=log_sensor_data)
    t1.start()

    updater = Updater("1134724631:AAH4XVhX1NtURXFaVHzeZ95FQUPsyq9xPTM", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("temp", check_sensor))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("info_bogdan", info_bog))
    dp.add_handler(CommandHandler("info_tanja", info_tan))
    dp.add_handler(CommandHandler("info_flash", info_flash))
    dp.add_handler(CommandHandler("empty", empty_log))
    dp.add_handler(CommandHandler("sensor", get_temp_log))
    dp.add_handler(CommandHandler("stream", get_stream))
    updater.start_polling()
    updater.idle()
    #while True:
        #check_sensor()
        #time.sleep(5)

if __name__ == '__main__':
    main()