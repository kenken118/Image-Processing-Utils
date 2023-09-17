# Imgage-Processing-Utils

## Description

本リポジトリは画像処理における様々なタスクをサポートしています。

## Requirement

- AWSアカウント

## Preparation

AWSマネジメントコンソールからGPU搭載のEC2インスタンスタイプを起動します。<br>
本リポジトリでは最もコスパに優れている**g4dn.xlarge**を選択して使用しています。

## Environment Setup

EC2のubuntuサーバー上にGPU対応のdocker環境を構築し、コンテナを立ち上げて使用します。<br>
以下の手順を実施してください。<br>

1. **Launching EC2 Instance**
    - AWS Management Console にログインし、EC2ダッシュボードに移動します。
    - 「インスタンスの起動」ボタンをクリックし、GPU対応のインスタンスタイプ（例：g4dn.xlarge）を選択します。
    - 必要に応じてインスタンスの設定を行い、起動します。

2. **Volume Configuration**
    - 必要に応じて、追加のEBSボリュームを作成またはアタッチします。

3. **Security Group Configuration**
    - SSH (ポート22) へのインバウンドトラフィックを許可するセキュリティグループルールを追加します。
    - その他の必要なポートもここで設定できます。

