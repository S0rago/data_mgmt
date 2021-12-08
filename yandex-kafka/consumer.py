from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'logs-topic',
    api_version=(0, 10, 2),
    bootstrap_servers='rc1b-uchmc3jfebod8f9m.mdb.yandexcloud.net:9092',
    security_protocol="SASL_PLAINTEXT",
    # sasl_mechanism="SCRAM-SHA-512",
    # sasl_plain_password='user_producer',
    # sasl_plain_username='qwerty12345',
    # ssl_cafile="/usr/local/share/ca-certificates/Yandex/YandexCA.crt"
    )

print("ready")

for msg in consumer:
    print(msg.key.decode("utf-8") + ":" + msg.value.decode("utf-8"))