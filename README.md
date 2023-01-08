# 整理每個時段，共15面球場的剩餘可租借場次

## 介紹

每次打羽毛球前都要擔心台大新館羽毛球場有沒有被訂光，上網找的時候還要將總共15面的場地一面一面點開來看，真的很麻煩。

## 環境設置

1. 安裝Chrome瀏覽器到預設安裝位置
2. 輸入下方指令，安裝環境所需套件

```shell
pip install -r requirements.txt
```

- 若環境設置仍有問題，可以使用anaconda創造一個python=3.9的環境

## 使用方法

```shell
python badminton_court.py [計中學號] [計中密碼]
```

- 此程式將會在資料夾下分別產生“court_information”跟“summary”兩個資料夾
- “court_information”放總共15個場中，每一個場的租借情形
- “summary”放整理好的可租借的時間，每個時間段都會寫上剩餘幾個場可以借。