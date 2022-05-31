import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CallbackContext, MessageHandler, filters, CommandHandler
import config
import functions
import os

TOKEN = config.SECRET_KEY
PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

start = [0]
active_person = []
familiar_person = []
to_ask = []
to_ask_source = []
asking = []
identifying = []
keyword = []
reply = []
try_correct = []
try_listen = []
try_reply = []
no_idea = []
try_idea = []
assure = []
plead = []


async def message(update: Update, context: CallbackContext.DEFAULT_TYPE):
    text = update.message.text.lower()

    if start[0] == 0:
        start.clear()
        start.append(1)

        functions.familiar(str(update.effective_chat.id), active_person, familiar_person)
        keyboard = [["TEACH ME"],
                    ["CHAT WITH ME"]]
        markups = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                       sticker="CAACAgIAAxkBAAICqGKOvt7bkApi0-0GWbyiGh4grnrWAAIdDQACHvvQSDHwOFDPb2R5JAQ")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"*Hello {update.effective_chat.first_name} {update.effective_chat.last_name}!*\nNice to meet you\nI love to learn new things",
                                       parse_mode='markdown', reply_markup=markups)

    elif start[0] == 1:
        if text == "teach me":
            # functions.cancel('Okay', update.effective_chat.id, context.bot)
            marks = ReplyKeyboardRemove()
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Okay',
                                           parse_mode="markdown", reply_markup=marks)
            quest = functions.ask("no idea", f'{update.effective_chat.first_name} {update.effective_chat.last_name}')
            if quest:
                for items in quest:
                    to_ask.append(items['listen'])
                    to_ask_source.append(items['Author'])
                    functions.delete_excess(items['listen'], items['Author'])

                await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                               sticker="CAACAgIAAxkBAAICsGKPVqAaM9h3xzUAAUroN0oD1RMEnwACFgEAAh8BTBU10Ep_XuXSUiQE")
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f'Please how do I reply\n if someone say:\n *{to_ask[0].capitalize()}*',
                                               parse_mode='markdown')
                asking.append(to_ask[0])
                identifying.append(to_ask_source[0])
                to_ask.remove(to_ask[0])
                to_ask_source.remove(to_ask_source[0])
                start.clear()
                start.append(3)

            else:
                await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                               sticker="CAACAgIAAxkBAAICq2KPU9YhLhqVUD7gSYmUkvAfBc2WAAJZFQAC3_s4SQnqEW74KtanJAQ")
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f'I am listening ...',
                                               parse_mode='markdown')
                start.clear()
                start.append(2)

        elif text == "chat with me":
            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAICtGKPWr9ghbw2jru3GjGLXio0-ca2AALTEgACvfE4SB6gKvyVXsfYJAQ")
            # functions.cancel('Really!\n I am flattered', update.effective_chat.id, context.bot)
            marks = ReplyKeyboardRemove()
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Really!\n I am flattered',
                                           parse_mode="markdown", reply_markup=marks)
            start.clear()
            start.append(5)

        else:
            # functions.invalid("That is wrong!\n *Press a button below*", update.effective_chat.id, update.message)
            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAPrYZgpuCc1LHLrxcN4T5mBMzKjXIQAAggNAAKmPTlIx6LTQyGewQciBA")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="That is wrong!\n *Press a button below*", parse_mode="markdown",
                                           reply_to_message_id=update.message.message_id)

    elif start[0] == 2:
        keyword.clear()
        keyword.append(text)

        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                       sticker="CAACAgEAAxkBAAICxWKPX5_Qoihty7wNla1iRIXKUEi_AAJGCAAC43gEAAGaajUPYa30iiQE")
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="How do i reply?",
                                       parse_mode='markdown')
        start.clear()
        start.append(3)

    elif start[0] == 3:
        reply.clear()
        reply.append(text)
        functions.store(asking, identifying, reply[0], asking,
                        f"{update.effective_chat.first_name} {update.effective_chat.last_name}",
                        try_correct, try_reply, try_listen, keyword, reply)

        if to_ask:
            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAICsGKPVqAaM9h3xzUAAUroN0oD1RMEnwACFgEAAh8BTBU10Ep_XuXSUiQE")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Please how do I reply\n if someone say:\n *{to_ask[0].capitalize()}*',
                                           parse_mode='markdown')
            asking.append(to_ask[0])
            identifying.append(to_ask_source[0])
            to_ask.remove(to_ask[0])
            to_ask_source.remove(to_ask_source[0])
            start.clear()
            start.append(3)
        else:
            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAICyGKPgkg7YDB4MzPZesmdZv2hPBrNAAKtDAAC8ZRBSKFwPL_6H9PpJAQ")
            # functions.confirm("Thanks very much\n Can you teach me more?", update.effective_chat.id, context.bot)
            keyboard = [["YES"],
                        ["NO"]]
            markup = ReplyKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Thanks very much\n Can you teach me more?",
                                           parse_mode='markdown', reply_markup=markup)
            start.clear()
            start.append(4)

    elif start[0] == 4:
        if text == 'yes':
            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAIC1GKPh5FNNEPAEKvDBatZROOHoKtbAAL3DQACQcOoSAGnwNyippitJAQ")
            # functions.cancel('Wow!\n you are a genius!\nI am listening ...', update.effective_chat.id, context.bot)
            marks = ReplyKeyboardRemove()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Wow!\n you are a genius!\nI am listening ...',
                                           parse_mode="markdown", reply_markup=marks)
            start.clear()
            start.append(2)

        elif text == 'no':
            start.clear()
            start.append(1)

            keyboard = [["TEACH ME"],
                        ["CHAT WITH ME"]]
            mark = ReplyKeyboardMarkup(keyboard)

            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAICzGKPhZufSQ_8F0Y1NHE5OQnQgbhOAAJqCwACtUuoSDL_p8pk4vHmJAQ")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Thank you {update.effective_chat.first_name} {update.effective_chat.last_name}\nWhat can we do now?",
                                           parse_mode='markdown', reply_markup=mark)

        else:
            # functions.invalid("That is wrong!\n *Press a button below*", update.effective_chat.id, update.message)
            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAPrYZgpuCc1LHLrxcN4T5mBMzKjXIQAAggNAAKmPTlIx6LTQyGewQciBA")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="That is wrong!\n *Press a button below*", parse_mode="markdown",
                                           reply_to_message_id=update.message.message_id)

    elif start[0] == 5:
        send = functions.think(no_idea, try_idea,
                               f"{update.effective_chat.first_name} {update.effective_chat.last_name}", text)

        if send:
            forward = send
        else:
            no_idea.clear()
            no_idea.append(1)
            find = functions.think(no_idea, try_idea,
                                   f"{update.effective_chat.first_name} {update.effective_chat.last_name}", text)

            if find:
                forward = find
            else:
                try_idea.clear()
                try_idea.append(1)
                finding = functions.think(no_idea, try_idea,
                                          f"{update.effective_chat.first_name} {update.effective_chat.last_name}", text)

                if finding:
                    forward = finding

                    try_listen.clear()
                    try_listen.append(text)

                    assure.clear()
                    assure.append(1)
                else:
                    forward = "no idea"
                    functions.keep(forward, text,
                                   f"{update.effective_chat.first_name} {update.effective_chat.last_name}")
                    plead.clear()
                    plead.append(1)
        if assure:
            try_reply.clear()
            try_reply.append(forward)

            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAIC5mKP8cCeTmlf5cwAASB2361S3jWStwACjw8AAnUuOUhbsCYf9OCDLyQE")
            # functions.confirm(f"{forward}\n\nAm I correct?", update.effective_chat.id, context.bot)
            keyboard = [["YES"],
                        ["NO"]]
            markup = ReplyKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"{forward}\n\nAm I correct?",
                                           parse_mode='markdown', reply_markup=markup)

            assure.clear()
            start.clear()
            start.append(6)

        elif plead:
            keyboard = [["TEACH ME"],
                        ["CHAT WITH ME"]]
            mark = ReplyKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=forward,
                                           parse_mode='markdown', reply_markup=mark)
            start.clear()
            start.append(1)
            plead.clear()
        else:
            if forward == 'no idea':
                keyboard = [["TEACH ME"],
                            ["CHAT WITH ME"]]
                mark = ReplyKeyboardMarkup(keyboard)

                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=forward,
                                               parse_mode='markdown', reply_markup=mark)
                start.clear()
                start.append(1)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=forward, parse_mode='markdown')

    elif start[0] == 6:
        # functions.cancel('Okay', update.effective_chat.id, context.bot)
        marks = ReplyKeyboardRemove()
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Okay',
                                       parse_mode="markdown", reply_markup=marks)
        if text == 'yes':
            try_correct.clear()
            try_correct.append(1)
            print(functions.store(asking, identifying, reply, asking,
                                  f"{update.effective_chat.first_name} {update.effective_chat.last_name}",
                                  try_correct, try_reply, try_listen, keyword, reply))

            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAIC22KP5ackXekCLRO-JaM__9cGvM-UAAKaCwACsqjQSBLncOfi0EbGJAQ")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks", parse_mode='markdown')

            start.clear()
            start.append(5)

        elif text == 'no':
            keyword.clear()
            keyword.append(try_listen[0])

            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgEAAxkBAAICxWKPX5_Qoihty7wNla1iRIXKUEi_AAJGCAAC43gEAAGaajUPYa30iiQE")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="How do i reply?",
                                           parse_mode='markdown')

            start.clear()
            start.append(3)

            try_reply.clear()
            try_listen.clear()

        else:
            try_reply.clear()
            try_listen.clear()

            await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                           sticker="CAACAgIAAxkBAAIC42KP8HSrKmVOreCOjuxURK0E4qVBAAKsDgACm205SDYlCZowOCzkJAQ")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Never mind\nI will do my research\nI am listening ...",
                                           parse_mode='markdown')

            start.clear()
            start.append(5)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', message)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    # application.run_polling()
    application.run_webhook(listen="0.0.0.0", port=PORT, url_path=config.SECRET_KEY, webhook_url=' https://telegrambot-io-2022.herokuapp.com/' + config.SECRET_KEY)

