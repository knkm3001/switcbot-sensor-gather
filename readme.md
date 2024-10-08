# switchbot sensor gather

## develop
以下でビルド
```
>> docker build -t core.harbor.ing.k8s-cluster.internal/sensor-data/switchbot-call-api:latest .
>> docker run --rm  --env-file .env -d core.harbor.ing.k8s-cluster.internal/sensor-data/switchbot-call-api:latest
>> docker exec -it <container id> /bin/bash
```

動作チェック問題なければpush
```
>> docker push core.harbor.ing.k8s-cluster.internal/sensor-data/switchbot-call-api:latest
```
