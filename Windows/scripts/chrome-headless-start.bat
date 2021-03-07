@echo off

REM  "C:\Users\jakub\AppData\Local\ms-playwright\chromium-775089\chrome-win\chrome.exe"  "C:\Users\jakub\Repos\puppeteer-recorder\lib\node_modules\puppeteer\.local-chromium\win64-756035\chrome-win\chrome.exe"

start /b "" "C:\Users\jakub\Repos\puppeteer-recorder\lib\node_modules\puppeteer\.local-chromium\win64-756035\chrome-win\chrome.exe" --remote-debugging-port=9223 --headless --disable-gpu --ignore-certificate-errors --no-sandbox --disable-setuid-sandbox --disable-accelerated-2d-canvas --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-renderer-backgrounding


REM --ignore-certificate-errors --no-sandbox --disable-setuid-sandbox --disable-accelerated-2d-canvas --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-renderer-backgrounding