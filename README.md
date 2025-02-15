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

**Method**: GET
**Service**: facade
**Url**: http://0.0.0.0:8000/facade-service 
<img src="imgs/facade_get.png" />

<br>

**Method**: POST
**Service**: facade
**Url**: http://0.0.0.0:8000/facade-service 
<img src="imgs/facade_post.png" />


<br>

**Method**: GET
**Service**: logging
**Url**: http://0.0.0.0:8001/logging-service
<img src="imgs/logging_get.png" />
After adding one more message:
<img src="imgs/logging_get2.png" />

<br>

**Method**: POST
**Service**: logging
**Url**: http://0.0.0.0:8001/logging-service
**Console output:**
<img src="imgs/console_output.png" />

<br>