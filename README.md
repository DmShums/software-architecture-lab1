# software-architecture-lab4

```bash
for i in {1..10}; do
    curl -X POST http://127.0.0.1:8000/facade-service \
         -H "Content-Type: application/json" \
         -d "{\"text\": \"msg$i\"}"
done
```