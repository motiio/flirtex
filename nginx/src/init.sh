#!/bin/sh

# Это пример скрипта, который использует 'envsubst' для подстановки всех
# переменных окружения, определенных в шаблоне конфигурации Nginx

# Загрузка всех переменных окружения в строку
vars_to_substitute=$(printf '${%s} ' $(env | cut -d= -f1))

# Использование 'envsubst' для замены переменных в шаблоне
envsubst "$vars_to_substitute" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Запуск Nginx
nginx -g 'daemon off;'
