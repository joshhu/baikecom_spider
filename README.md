# 使用`scrapy`爬取百度百科
## 一、前言
由於中文語料庫不多，因此需要爬取自己的資料。維基百科可以下載不需要爬，但百度百科沒有開放要自己爬。因此爬取百度百科的資料，並且存在`mongodb`的資料庫中。

## 二、開發環境
### 1、基本環境準備
* Ubuntu 22.04
* Visual Studio Code從Windows11遠端連接至Ubuntu
* Docker，用來啟動`mongodb`資料庫和`mongo-express`從網頁查看資料庫。
* python 3.8.13
* scrapy

### 2、Docker環境
由於`mongodb`的儲存希望持久化，因此將資料庫實際資料的部分存放在container之外。一開始使用bind mount對應到硬碟的某個資料夾，但發現把container殺掉之後再開新的`mongodb` container，就無法找到`collection`，因此使用docker的`volume`進行存放。建立步驟如下

1. 建立docker volume，`docker volume create mongodb_storage`
2. 建立docker network，讓`mongodb`和`mongo-express`之間可以互相溝通。指令：`docker network create mongodb`
3. 啟動`mongodb`的container，指令：`docker run -d --name baike -p 27017:27017 -v mongodb_storage:/data/db --network mongodb mongo`
4. 啟動`mongo-express`，指令如下`docker run -d --name mongo-express -p 8081:8081 --network mongodb -e ME_CONFIG_MONGODB_SERVER=baike mongo-express`

以上步驟即完成了`mongodb`和`mongo-express`的啟動。

## 三、`scrapy`架構
## 1、`scrapy`架構
```
├── baikecom_spider
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── baikecom.py
│       ├── __init__.py
├── baikecom_spider.log
└── scrapy.cfg
```

## 2、注意事項
需要注意的是，百度百科有兩個版本，一個是簡體版，網址是`baike.baidu.com`，另一個是繁體版，網址是`baihe.baidu.hk`，兩者的網頁結構不同，因此需要分別爬取。主要還是Title和Subtitle的不一樣。分別如下：

**繁體版百度香港**
```xpath=
'//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()'
'//dd[@class="lemmaWgt-lemmaTitle-title"]/h2/text()'
```
**簡體版百度百科**
```xpath=
'//dd[contains(@class, "lemmaWgt-lemmaTitle-title") and contains(@class, "J-lemma-title")]/span/h1/text()'
'//dl[contains(@class, "lemmaWgt-lemmaTitle") and contains(@class, "lemmaWgt-lemmaTitle-")]/div[@class="lemma-desc"]/text()'
```
其它看程式。

## 3、性能
**每小時約15萬個詞條**。本來怕檔案太大，因此`mongodb`本來放在32TB的HDD中，後來發現百度號稱3000萬個詞條，最多佔硬碟空間約100GB，因此改放在SSD中，NVME SSD的大小為4TB

## 四、參考資料
* [Mongodb在Python下的使用](https://www.1ju.org/mongodb/mongodb-python)
* [Scrapy爬百度](https://github.com/vinsssss/EnhanceBaike)
* [Youtube尚硅谷90-103](https://www.youtube.com/watch?v=wRllz8DWXUI)

