#!/bin/sh

# Функция для получения сертификатов с Certbot
get_certificates() {
    certbot certonly --nginx \
    -d flirtex.fun -d "*.flirtex.fun" \
    --non-interactive \
    --agree-tos \
    --email motiio.none@gmail.com \
    --no-eff-email \
    --keep-until-expiring
}

# Функция для автоматического обновления сертификатов
auto_renew() {
    echo "0 0,12 * * * root certbot renew --quiet --post-hook 'nginx -s reload'" >> /etc/crontabs/root
    crond
}

# Вызов функции для получения или обновления сертификатов
#get_certificates

# Настройка crontab для автоматического обновления сертификатов
auto_renew

# Запуск Nginx в foreground
exec nginx -g 'daemon off;'
