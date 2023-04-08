wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install ./google-chrome-stable_current_amd64.deb
# 查看 chrome 版本
google-chrome --version
# Google Chrome 74.0.3729.131
# 到chrome driver網站下載對應版本的 driver。
# 安裝 chrome driver (v74版)
wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
# 這邊將 chromedriver 放到家目錄下 (docker image以/root為家目錄)
unzip chromedriver_linux64.zip -d ./
export USER="b09902110"
export PASSWORD="Bubu011878"