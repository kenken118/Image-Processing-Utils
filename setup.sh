#!/bin/bash

# Chromeのインストール
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt update -y
apt install -y ./google-chrome-stable_current_amd64.deb

# Chromeのバージョンを取得
CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | sed 's/\..*//')
echo "Chrome Version: $CHROME_VERSION"

# 対応するChromedriverのバージョンを取得
LATEST_CHROMEDRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "Chromedriver Version: $LATEST_CHROMEDRIVER_VERSION"

# Chromedriverのダウンロードとインストール
wget "https://chromedriver.storage.googleapis.com/$LATEST_CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/bin/
rm chromedriver_linux64.zip

# 一時的にダウンロードしたChromeのdebファイルを削除
rm google-chrome-stable_current_amd64.deb
