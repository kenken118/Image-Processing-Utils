#!/bin/bash

# IPアドレスを取得
MY_IP=$(curl -s ipinfo.io/ip)/32

# IPアドレスの確認
echo "Detected IP: $MY_IP"

# CloudFormationスタックを作成
aws cloudformation create-stack \
  --stack-name dev-stack \
  --template-body file://cloudformation_template.yml \
  --parameters ParameterKey=PJPrefix,ParameterValue=dev ParameterKey=KeyName,ParameterValue=$AWS_KEY_NAME ParameterKey=MyIP,ParameterValue=$MY_IP \
  --capabilities CAPABILITY_NAMED_IAM

# 以下のメッセージを表示
echo "Stack creation initiated. Please check AWS Management Console for its status."