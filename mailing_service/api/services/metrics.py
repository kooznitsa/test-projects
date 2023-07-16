from prometheus_client import Counter, Info

info = Info(name='notification_service_metrics', documentation='')
info.info({'version': '1.0', 'language': 'python', 'framework': 'fastapi'})

mailouts_total_created = Counter(
    name='mailouts_total_created',
    documentation='Total number of mailouts created',
    labelnames=['tag'],
)

customers_total_created = Counter(
    name='customers_total_created',
    documentation='Total number of customers created',
    labelnames=['tag'],
)

messages_total_sent = Counter(
    name='messages_total_sent',
    documentation='Total number of messages successfully sent per mailout id',
    labelnames=['mailout_id'],
)

messages_total_failed = Counter(
    name='messages_total_failed',
    documentation='Total number of messages failed (after a number of retries) per mailout id',
    labelnames=['mailout_id'],
)
