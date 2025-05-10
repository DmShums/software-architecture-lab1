# software-architecture-lab1

### Install dependencies
```bash
python3 -m pip install -r requirements.txt
```

### Run python file
```bash
python3 runner.py
```

### Implementation

**Method**: GET<br>
**Service**: facade<br>
**Url**: http://0.0.0.0:8000/facade-service <br>
<img src="imgs/facade_get.png" />

<br>

**Method**: POST<br>
**Service**: facade<br>
**Url**: http://0.0.0.0:8000/facade-service <br>
<img src="imgs/facade_post.png" />


<br>

**Method**: GET<br>
**Service**: logging<br>
**Url**: http://0.0.0.0:8001/logging-service<br>
<img src="imgs/logging_get.png" />
After adding one more message:
<img src="imgs/logging_get2.png" />

<br>

**Method**: POST<br>
**Service**: logging<br>
**Url**: http://0.0.0.0:8001/logging-service<br>
**Console output:**
<img src="imgs/console_output.png" />

<br>


# Additional tasks

First of all run sepparately all services

```bash
python3 logging_service.py    # listens on 8001
python3 messages_service.py   # listens on 8002
uvicorn facade_service:facade_service --port 8000
```


Let's make post request using `grpc`
<img src="imgs/additional1.png"/>

Let's make get request
<img src="imgs/additional2.png"/>

Let's try to implement retry mechanism. Here I disconnected logging service. We can see there are three attempts:
<img src="imgs/additional3.png"/>
<img src="imgs/additional4.png"/>

Now let's reconnect logging service:
<img src="imgs/additional5.png"/>
<img src="imgs/additional6.png"/>