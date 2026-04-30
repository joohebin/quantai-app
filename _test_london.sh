#!/bin/bash
# Test MetaApi endpoints

TOKEN='eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI3MTI1Mzc1MTA0YjcwNjVkNzliNDMwMDRiMjMwYjkyYyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIjo6KioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6KioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyb2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImNvcHlmYWN0b3J5LWFwaSIsIm1ldGhvZHMiOlsiY29weWZhY3RvcnktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VhcmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6ImJpbGxpbmctYXBpIiwibWV0aG9kcyI6WyJiaWxsaW5nLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIl0sInJlc291cmNlcyI6WyIqOiBVU0VSX0lEJDoqIl19XSwiaWdub3JlUmF0ZUxpbWl0cyI6ZmFsc2UsInRva2VuSWQiOiIyMDIxMDIxMyIsImltcGVyc29uYXRlZCI6ZmFsc2UsInJlYWxVc2VySWQiOiI3MTI1Mzc1MTA0YjcwNjVkNzliNDMwMDRiMjMwYjkyYyIsImlhdCI6MTc3NTY0NDY3Nn0.WPFL-SducyQmM6_kL-i5kmq8HK0xYysEoUY52dOZlAbGyOnBdxU_3XZn1AtpowRjMQzapOU9Kjl5-PHVPehYoG1kb7Hxc3GOu0v83KFqKacNxX4WOUH9IL4q5LyyAhNrAzjG_w5wxPGR_DYILlcsq1NuHKR9Gw3lsbV-3PoCVkcimVBqhqpbm7hsNFDD652XnuVOdYix50t1USPQnRW1wAYY4F1atPdPtud3Kl_olGWUkWdelZTWgOyMDIq9nbeAhZ_rQYu7F6OKmOPBhMrnWHdaIcvAgateenmTb1YHVguqWfR-tHQgqCg22gaGq98C4tz-ShYqrKcHB3_1Ogu1w0QNv_8pVIu-glc7LtiqPhIJsv-7UmksOk2FHY0hpbEeB7x5v1kiRR4f5GuRRsTQNcUSv20bRBl7s1hp2X77GDg1JV7YqCuCx39RIFDUJBfi__NL5YcBsLgcGWrANkUDcWRxtKCVGEJW4X0w7Z5xwVwwq3DmTFT9nhyPH-ipw4fw87NguHRinR3dXhqMUYiQHIl1sgxeODeR89gXDRm_J-ZMcOFZUr7um9Hpa1ZxyMpR2CVQaQx3nswcyhK_dUZXoOmSIT0GWz5oWHM_xEHUQV0gFsuGg2T3Yzl8dc60ppuaf9B4HZuZx8nSLfhBHxHlJ3uRpEzqYeKQzheBA6mtczY'
ACCOUNT_ID='3791ec3f-4ef6-493f-b460-4cdbc40e33e4'

echo "============================================"
echo "Testing MetaApi endpoints from London Server"
echo "============================================"

echo ""
echo "[1] mt-client-api-v1.metaapi.io (Standard)"
echo "--------------------------------------------"
curl -s -w "\nHTTP Status: %{http_code}\n" \
    "https://mt-client-api-v1.metaapi.io/accounts/${ACCOUNT_ID}" \
    -H "Authorization: Bearer ${TOKEN}"

echo ""
echo "[2] mt-client-api-v1.metaapi.io with region=london"
echo "--------------------------------------------"
curl -s -w "\nHTTP Status: %{http_code}\n" \
    "https://mt-client-api-v1.metaapi.io/accounts/${ACCOUNT_ID}?region=london" \
    -H "Authorization: Bearer ${TOKEN}"

echo ""
echo "[3] london.agiliumtrade.ai (London Region)"
echo "--------------------------------------------"
curl -s -w "\nHTTP Status: %{http_code}\n" \
    "https://london.agiliumtrade.ai/v1/accounts/${ACCOUNT_ID}" \
    -H "Authorization: Bearer ${TOKEN}"

echo ""
echo "[4] mt-manager-api-v1.london.agiliumtrade.ai"
echo "--------------------------------------------"
curl -s -w "\nHTTP Status: %{http_code}\n" \
    "https://mt-manager-api-v1.london.agiliumtrade.ai/users/current/mt5/provisioning-profiles/${ACCOUNT_ID}/accounts" \
    -H "auth-token: ${TOKEN}"

echo ""
echo "============================================"
echo "Done"
echo "============================================"
