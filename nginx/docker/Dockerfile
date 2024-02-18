# Используйте официальный образ Nginx как базовый
FROM nginx:stable-alpine

# Установка Certbot
RUN apk add --no-cache certbot certbot-nginx

# Копирование скрипта для запуска и обновления сертификатов
COPY entrypoint.sh /entrypoint.sh

# Сделайте скрипт исполняемым
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
