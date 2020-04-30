
FROM nginx:1.13

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
