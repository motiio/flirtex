const TelegramBot = require('node-telegram-bot-api');
const botToken = process.env.BOT_TOKEN;
const webAppUrl = process.env.WEB_APP_URL;
const templateAppUrl = process.env.TEMPLATE_APP_URL;
const bot = new TelegramBot(botToken, {polling: true});
const adminIdList = process.env.ADMIN_LIST.split(',').map(id => parseInt(id.trim(), 10));

bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;
    const userId = msg.from.id

    if (text === '/start') {
        return bot.sendMessage(chatId, 'Жми открыть и начинай общение!', {
            reply_markup: {
                inline_keyboard: [
                    [
                        {text: 'Открыть', web_app: {url: webAppUrl}},
                    ]
                ]
            },
        })
    }

    if (text === '/info') {
        return  bot.sendMessage(chatId, 'Привет! Это приложение, которое поможет тебе находить новые знакомства, заводить друзей и, возможно, даже найти свою любовь.\n' +
            '💖 Мы предоставляем тебе возможность находить интересных людей с помощью простого свайпа!\n' +
            '💬 Общайся и встречайся только с реальными людьми, расширяй круг общения и находи новых друзей.\n' +
            '📝 Просматривай профили пользователей, чтобы лучше узнать их. \n' +
            '‼️ Не нужно скачивать никаких приложений. Используй телеграм!\n' +
            '❤️ FlirteX - для вас ❤️ https://t.me/FlirtexBot/app', {
            reply_markup: {
                inline_keyboard: [
                    [
                        {text: '💒 Открыть', web_app: {url: webAppUrl}},
                    ]
                ]
            },
        })
    }

    if (text === '/help') {
        return bot.sendMessage(chatId, 'Возникли вопросы по работе приложения?', {
            reply_markup: {
                inline_keyboard: [
                    [{text: '❓ FAQ', url: 'https://telegra.ph/FAQ-02-12-12'}],
                    [{text: '⛏ Сообщить об ошибке', url: 'https://t.me/flirtex_admin'}],
                ]
            },
        })
    }

    if (text === '/links') {
        return bot.sendMessage(chatId, 'Наши социальные сети.\nПрисоединяйтесь к нам и будьте в курсе всех новостей и обновлений.', {
            reply_markup: {
                inline_keyboard: [
                    [
                        {text: '✉️ Новости', url: 'https://t.me/flirtex'},
                        {text: '🔥 Общий чат', url: 'https://t.me/flirtex_chat'},
                    ],
                    [{text: '💊 Группа Вконтакте', url: 'https://vk.com/flirtex'}],
                    [{text: '⛏ Сообщить об ошибке', url: 'https://t.me/flirtex_admin'}],
                ]
            },
        })
    }

    if (text === '/dev') {
        if (adminIdList.includes(userId)) {
            return bot.sendMessage(chatId, 'FlirteX', {
                reply_markup: {
                    inline_keyboard: [
                        [
                            {text: 'Открыть приложение для разработки', web_app: {url: templateAppUrl}}
                        ]
                    ]
                },
            })
        }
    }
});

bot.setMyCommands([
    { command: '/start', description: 'Запуск бота' },
    { command: '/links', description: 'Связаться с нами' },
    { command: '/info', description: 'Информация' },
    { command: '/help', description: 'Помощь' },
])

bot.on('inline_query', (query) => {
    bot.answerInlineQuery(query.id,
        [{
            id: 3228,
            type: 'article',
            title: 'Вставить ссылку',
            input_message_content: {
                message_text: 'Заходи и свайпай @FlirteXBot'
            }
        }], {
            switch_to_pm: 'Посетить бота',
        })
})
