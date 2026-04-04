const { spawn } = require('child_process');
const path = require('path');

process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');

const env = {
  ...process.env,
  JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
  ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
  ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk'
};
env.PATH = 'C:\\Program Files\\nodejs;' + env.JAVA_HOME + '\\bin;' + env.ANDROID_HOME + '\\platform-tools;' + env.ANDROID_HOME + '\\cmdline-tools\\latest\\bin;' + process.env.PATH;

const nodePath = 'C:\\Program Files\\nodejs\\node.exe';
const capBin = path.join(process.cwd(), 'node_modules', '@capacitor', 'cli', 'dist', 'index.js');

console.log('Starting Capacitor CLI...');
console.log('CWD:', process.cwd());

const child = spawn(nodePath, [capBin, 'add', 'android'], {
  env,
  shell: false,
  stdio: ['pipe', 'pipe', 'pipe']
});

child.stdout.on('data', (data) => {
  console.log('STDOUT:', data.toString());
});

child.stderr.on('data', (data) => {
  console.log('STDERR:', data.toString());
});

child.on('error', (err) => {
  console.error('Process error:', err.message);
});

child.on('close', (code) => {
  console.log('Process exited with code:', code);
});
