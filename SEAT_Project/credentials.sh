#!/bin/sh

echo \
"[default] 
aws_access_key_id=ASIAZSPXN3SF44NHLCGI 
aws_secret_access_key=xysMJ1dGIfEVemLbUMyTVV3kXC/kTBpl3HXGl1fE 
aws_session_token=FwoGZXIvYXdzEIL//////////wEaDMBXOJMd4tzvEmTLYSLXAUAEB4ycuLExgBht0m9yH7SHGVespdinB9GwDF82eFc68KYvnR3lv9GdXSfkH8UC/Dd2KIspSKQiO0fsLKTFVYOrfCIJo4/mM1CuRvX3nltepAJRe0rVnKJynWWbww6k1/TpbrxK4h0wyCHT7qUF3be/ZLAEPr3pgT9rUVr9TABar0/ZbcTJ+Dok5nYBJNv3qeItQuEGLE5nP6Y2Rhgi5lQR7Lz5PY8tAZg4PNF7FlDAGBub8R38tViMQOKVTDLacSKxo2CDqyE/yyvohOAIi5qmzIf5TjixKLfz+JoGMi1rye7sl6X8WPenoigRMUIuLujhQZdBSZz1pM4es1aJuMHcxx07kk2Y+5BHcuE=" > $HOME/.aws/credentials 

cp $HOME/.aws/credentials ./accountingService/credentials
cp $HOME/.aws/credentials ./quoteService/credentials
cp $HOME/.aws/credentials ./reservationService/credentials
cp $HOME/.aws/credentials ./reviewService/credentials