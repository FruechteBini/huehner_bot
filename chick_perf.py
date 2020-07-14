from telegram.ext import Updater, CommandHandler


class Chicken:
    performance_template = \
        """{id}s Performance:
        Gesamt: {output} 
        Höchste Streak: {record}
        Aktuelle Streak: {streak}
        """

    def __init__(self, name, initial_streak=0, initial_output=0, initial_record=0):
        self.name = name
        self.streak = initial_streak
        self.output = initial_output
        self.record = initial_record


    def performance_day(self):
        self.output += 1
        self.streak += 1
        if self.streak > self.record:
            self.record = self.streak

    def lay_day(self):
        self.streak = 0

    def show_performance(self):
        return self.performance_template.format(id=self.name,
                                                output=self.output,
                                                record=self.record,
                                                streak=self.streak)


bogdan = Chicken('Bogdan', 10, 15, 5)
flash = Chicken('Flash', 15, 20, 10)
tanja = Chicken('Tanja', 20, 25, 15)

def start(update, context):
    start_text = """
    Hi!
    Willkommen beim Performance-Hühnerbot:
    
    - Tippe /bogi_performed wenn bogdan heute performed hat
    - Tippe /bogi_chillt wenn bogdan heute kein Ei gelegt hat
    
    - Tippe /flash_performed wenn flash heute performed hat
    - Tippe /flash_chillt wenn flash heute kein Ei gelegt hat
    
    - Tippe /tanja_performed wenn tanja heute performed hat
    - Tippe /tanja_chillt wenn tanja heute kein Ei gelegt hat
    
    - Tippe /status für die aktuellen Daten
    """
    update.message.reply_text(start_text)

                              
def bogdan_performance_day(update, context):
    bogdan.performance_day()
    update.message.reply_text(bogdan.show_performance())


def bogdan_lay_day(update, context):
    bogdan.lay_day()
    update.message.reply_text(bogdan.show_performance())
    
    
def flash_performance_day(update, context):
    flash.performance_day()
    update.message.reply_text(flash.show_performance())


def flash_lay_day(update, context):
    flash.lay_day()
    update.message.reply_text(flash.show_performance())

    
def tanja_performance_day(update, context):
    tanja.performance_day()
    update.message.reply_text(tanja.show_performance())


def tanja_lay_day(update, context):
    tanja.lay_day()
    update.message.reply_text(tanja.show_performance())
    
def status(update, context):
    update.message.reply_text(bogdan.show_performance())
    update.message.reply_text(flash.show_performance())
    update.message.reply_text(tanja.show_performance())

    
    
def main():
    updater = Updater(token="1375900918:AAH-O1yud2bT0fXHGUXAi0txo-sTfW932xo", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("bogi_performed", bogdan_performance_day))
    dp.add_handler(CommandHandler("bogi_chillt", bogdan_lay_day))
    
    dp.add_handler(CommandHandler("bogi_performed", bogdan_performance_day))
    dp.add_handler(CommandHandler("flash_chillt", flash_lay_day))
    
    dp.add_handler(CommandHandler("flash_performed", flash_performance_day))
    dp.add_handler(CommandHandler("tanja_chillt", tanja_lay_day))
    dp.add_handler(CommandHandler("tanja_performed", tanja_performance_day))
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
