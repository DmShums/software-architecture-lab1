# 1) Kafka bootstrap list (must match your exposed EXTERNAL ports)
curl -X PUT http://localhost:8500/v1/kv/config/kafka/bootstrap \
     --data-binary localhost:29092,localhost:29093,localhost:29094

# 2) MQ queue name
curl -X PUT http://localhost:8500/v1/kv/config/mq/queue_name \
     --data-binary messages

# 3) Hazelcast member endpoints
curl -X PUT http://localhost:8500/v1/kv/config/hazelcast/members \
     --data-binary 127.0.0.1:5701,127.0.0.1:5702,127.0.0.1:5703

# 4) Hazelcast cluster name
curl -X PUT http://localhost:8500/v1/kv/config/hazelcast/cluster \
     --data-binary dev
