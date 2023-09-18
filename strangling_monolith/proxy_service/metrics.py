from prometheus_client import Gauge, generate_latest

proxy_metrics = Gauge('proxy_metrics', 'Proxy metrics')