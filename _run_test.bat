@echo off
cd /d C:\Users\Administrator\WorkBuddy\Claw\quantai-app
python _test_sdk.py > _test_sdk_output.txt 2>&1
type _test_sdk_output.txt
