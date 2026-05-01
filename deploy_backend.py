"""Deploy QuantAI backend to EC2 via SSM"""
import boto3, time, base64, math, os, glob

session = boto3.Session(
    aws_access_key_id='AKIASMPR6CTXYKST5J6K',
    aws_secret_access_key='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',
    region_name='ap-northeast-1'
)
ssm = session.client('ssm')
INSTANCE = 'i-03c6b37fd18bcf9b4'
BASE = r'C:\Users\Administrator\WorkBuddy\Claw\quantai-app\backend'

def run(cmd, wait=5):
    r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName='AWS-RunShellScript',
                         Parameters={'commands': [cmd]})
    time.sleep(wait)
    return r

def upload_file(local, remote):
    with open(local, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('ascii')
    CHUNK = 80000
    n = math.ceil(len(b64) / CHUNK)
    
    run(f'mkdir -p $(dirname {remote})')
    
    for i in range(n):
        chunk = b64[i*CHUNK:(i+1)*CHUNK]
        esc = chunk.replace("'", "'\"'\"'")
        run(f'echo -n \'{esc}\' >> /tmp/be_b64')
        print(f'  Chunk {i+1}/{n}')
    
    run(f'base64 -d /tmp/be_b64 > {remote} && rm /tmp/be_b64')
    print(f'  Deployed: {remote} ({len(data)} bytes)')
    return len(data)

print('=== Deploying QuantAI Backend ===')

# Create remote dir
run('mkdir -p /home/ubuntu/quantai-backend/routers')

# Copy files
files = []
for root, dirs, fnames in os.walk(BASE):
    for fname in fnames:
        if fname.endswith('.py') or fname in ['requirements.txt', 'run.sh']:
            local = os.path.join(root, fname)
            rel = os.path.relpath(local, BASE)
            remote = f'/home/ubuntu/quantai-backend/{rel}'
            files.append((local, remote))

for local, remote in files:
    print(f'Uploading {os.path.basename(local)}...')
    upload_file(local, remote)

# Install deps and start
print('\n=== Installing dependencies ===')
run('cd /home/ubuntu/quantai-backend && pip install -r requirements.txt', 10)

print('\n=== Starting backend ===')
run('''
cat > /tmp/be.service << 'SERVICEEOF'
[Unit]
Description=QuantAI Backend API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/quantai-backend
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8002 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF
sudo mv /tmp/be.service /etc/systemd/system/quantai-backend.service
sudo systemctl daemon-reload
sudo systemctl enable quantai-backend
sudo systemctl restart quantai-backend
''', 5)

# Check
time.sleep(3)
r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName='AWS-RunShellScript',
                     Parameters={'commands': ['sudo systemctl status quantai-backend --no-pager --lines=5',
                                               'curl -s http://localhost:8002/']})
print('\n=== Status ===')
time.sleep(3)
print('Check: http://54.95.26.117:8002/')
print('Done!')
