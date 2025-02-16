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