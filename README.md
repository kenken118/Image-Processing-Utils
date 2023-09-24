# Imgage-Processing-Utils

## Description

本リポジトリは、画像処理の一蓮のパイプラインをサポートしています。<br>
以下の主要タスクを順番に実行することで、迅速に画像処理タスクを実行することができます。<br>

1. image_scraping: インターネット上から必要な画像を収集します。
2. auto_annotation: 収集した画像に自動的にアノテーションを付与します。（アノテーションコスト削減）
3. data_augmentation: アノテーションされた画像とそれに対応するラベルを拡張し、学習の前準備としてデータをtrain, valid, testに分割します。
4. object_detection: 学習から評価、そして推論までの一連の物体検知タスクを行います。

## Requirement

- AWSアカウント

## Preparation

### EC2 Environment Setup

AWSマネジメントコンソールからGPU搭載のEC2インスタンスタイプを起動します。<br>
本リポジトリでは最もコスパに優れている**g4dn.xlarge**を選択して使用しています。<br>
以下の手順を実施してください。<br>

1. **Launching EC2 Instance**
    - AWS Management Console にログインし、EC2ダッシュボードに移動します。
    - 「インスタンスの起動」ボタンをクリックし、GPU対応のインスタンスタイプ（例：g4dn.xlarge）を選択します。
    - 必要に応じてインスタンスの設定を行い、起動します。

2. **Volume Configuration**
    - ストレージの追加で20GBに設定します。
    - 作成したボリュームを起動中のインスタンスにアタッチします。

3. **Security Group Configuration**
    - セキュリティグループで、SSHのポート22とJupyter-labのポート8888へのインバウンドトラフィックを許可します。

### Docker Setup

EC2のubuntuサーバー上にGPU対応のdocker環境を構築し、コンテナを立ち上げて使用します。<br>
以下の手順を実施してください。<br>

1. ubuntu-drivers-commonパッケージのインストール
```
$ sudo apt-get update
$ sudo apt install -y ubuntu-drivers-common
```

2. NVIDIAデバイスとその関連ドライバーの情報を確認
```
$ lspci | grep -i nvidia
$ ubuntu-drivers devices
```

3. NVIVIAドライバーのインストール
```
$ sudo apt-get install nvidia-driver-525
```

4. NVIDIAのパッケージを確認
```
$ dpkg -l | grep nvidia
```

5. インストール後、OSの再起動
```
$ sudo systemctl reboot
```

6. OSの再起動後、NVIVIAのドライバーがロードされていることを確認
```
$ sudo dmesg | grep -i nvidia
```

7. NVIDIAドライバーの確認
```
$ nvidia-smi
```
8. nvidia-dockerのインストール
```
$ sudo apt-get -y install docker
$ curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
$ sudo apt-get update
$ sudo apt-get install -y nvidia-container-toolkit
$ sudo nvidia-ctk runtime configure --runtime=docker
$ sudo systemctl restart docker
```

9. nvidia-docker上でcudaとcudnnが認識できているかの確認
```
$ sudo docker run --rm --gpus all nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 nvidia-smi
```

10. dockerグループにubuntuユーザーを追加
```
$ sudo gpasswd -a ubuntu docker
```
上記の変更を有効にするために、ログアウト（exit）して再度SSHでログインしてください。<br>

### Repository Setup

以下コマンドを使用して、`/home/ubuntu/`配下に本リポジトリをcloneします。
```
$ git clone https://github.com/kenken118/Image-Processing-Utils
```
これで準備は完了です。<br>

## Usage
以下の手順を実施してください。<br>
1. ビルドコンテキストのあるディレクトリに移動
```
$ cd Image-Processing-Utils
```

2. Dockerイメージのビルド
```
$ docker compose build
```

3. Dockerコンテナをバックグラウンドで起動
```
$ docker compose up -d
```

4. アプリケーションへのアクセス
Webブラウザを開き、以下のアドレスにアクセスする。<br>
`{起動中のEC2インスタンスのパブリックIPv4DNS}:8888`
