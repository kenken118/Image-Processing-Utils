# Imgage-Processing-Utils

## Description

本リポジトリは、画像処理の一連のパイプラインをサポートしています。<br>
以下の主要タスクを順番に実行することで、迅速に画像処理タスクを実行することができます。<br>

1. image_scraping: インターネット上から必要な画像を収集します。
2. auto_annotation: 収集した画像に自動的にアノテーションを付与します。（アノテーションコスト削減）
3. data_augmentation: アノテーションされた画像とそれに対応するラベルを拡張し、学習の前準備としてデータをtrain, valid, testに分割します。
4. object_detection: 学習から評価、そして推論までの一連の物体検知タスクを行います。

## Requirement

- AWSアカウント
- AWS CLIがインストールされていること
- AWSクレデンシャル（アクセスキー, シークレットアクセスキー）
- .pemファイル（EC2インスタンスへのSSH接続用）

## Configuration Notes
CloudFormationテンプレートには、特定の設定値が事前に定義されています。以下の項目をご確認の上、必要に応じてテンプレートを適宜修正してください。

- リージョン: 現在は東京リージョン（`ap-northeast-1`）を対象としています。
- インスタンスタイプ: 使用されるEC2インスタンスのタイプは`g4dn.xlarge`です。
- AMIのID: 特定のUbuntuバージョンや他のOSを使用したい場合は、適切なAMI IDに変更してください。
- ボリュームサイズ: EC2インスタンスのルートボリュームサイズは`30GB`に設定されています。

## Usage
以下の手順に従って、本リポジトリをセットアップおよびデプロイしてください。<br>
1. リポジトリのclone<br>
ローカルマシンに本リポジトリをcloneします。
```
$ git clone https://github.com/kenken118/Image-Processing-Utils
```

2. ディレクトリの移動
```
$ cd Image-Processing-Utils
```

3. AWS CLIの設定<br>
アクセスキー、シークレットアクセスキー、リージョン、出力形式を入力する必要があります。
```
$ aws configure
```
注意：リージョンは東京リージョン（`ap-northeast-1`）を指定してください。

4. 環境変数のエクスポート<br>
`.pem`拡張子を除いたキーペアの名前を設定します。
```
$ export AWS_KEY_NAME={pemファイル名}
```

5. デプロイの実行<br>
`deploy.sh`を実行します。このスクリプトはAWS CloudFormationを使用してリソースをデプロイします。
```
$ ./deploy.sh
```
注意：CloudFormationでのスタックの展開は、Docker環境の構築も含めて実行されるため、少し時間がかかります。完了まで2~3分ほどお待ちください。

6. EC2へのSSH接続<br>
デプロイが完了したら、起動したEC2インスタンスにSSH接続します。AWS Management ConsoleのEC2ダッシュボードから該当インスタンスの「パブリックIpV4DNS」を確認します。
```
$ ssh -i /path/to/＄{AWS_KEY_NAME}.pem ubuntu@{パブリックIpV4DNS}
```

7. リモートホストへのリポジトリのclone<br>
接続先のEC2インスタンスに本リポジトリをcloneします。
```
$ git clone https://github.com/kenken118/Image-Processing-Utils
```

8. ディレクトリの移動
```
$ cd Image-Processing-Utils
```

9. Dockerイメージのビルド
```
$ docker compose build
```

10. Dockerコンテナをバックグラウンドで起動
```
$ docker compose up -d
```

11. jupyter-labに接続<br>
コンテナの起動が完了したら、webブラウザを開いて以下のURLにアクセスし、jupyter-labに接続します。
```
http://{パブリックIpV4DNS}:8888
```
注意：使用が終わったら、AWS Management ConsoleのCloudFormationダッシュボードから`dev-stack`というスタックを削除してください。