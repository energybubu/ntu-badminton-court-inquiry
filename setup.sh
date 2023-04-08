# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# apt install ./google-chrome-stable_current_amd64.deb
# 查看 chrome 版本

# Google Chrome 74.0.3729.131
# 到chrome driver網站下載對應版本的 driver。
# 安裝 chrome driver (v74版)
wget -P ./chromedriver https://chromedriver.storage.googleapis.com/index.html?path=112.0.5615.49/
# 這邊將 chromedriver 放到家目錄下 (docker image以/root為家目錄)

