#!/bin/bash
# 用法: bash scripts/publish_wechat.sh "<标题>" "<html_file>" "<摘要>" [cover_image_path]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/../skills/weixin-wechat-channel"

if [ $# -lt 3 ]; then
    echo "用法: bash publish_wechat.sh <标题> <html文件路径> <摘要> [封面图路径]"
    exit 1
fi

TITLE="$1"
HTML_FILE="$2"
DIGEST="$3"
COVER_PATH="$4"

# 加载环境变量
set -a
source "$SCRIPT_DIR/../.env"
set +a

# 若有封面图，先上传获取 media_id
THUMB_MEDIA_ID=""
if [ -n "$COVER_PATH" ] && [ -f "$COVER_PATH" ]; then
    echo "上传封面图..."
    THUMB_MEDIA_ID=$(python3 -c "
import os, requests, sys
s = requests.Session()
s.trust_env = False
appid = os.environ.get('WECHAT_APPID') or os.environ.get('WECHAT_APP_ID')
secret = os.environ.get('WECHAT_APPSECRET') or os.environ.get('WECHAT_APP_SECRET')
r = s.get('https://api.weixin.qq.com/cgi-bin/token', params={'grant_type': 'client_credential', 'appid': appid, 'secret': secret}, timeout=60)
token = r.json().get('access_token', '')
if not token:
    print('')
    exit(0)
cover_path = sys.argv[1]
with open(cover_path, 'rb') as f:
    files = {'media': (cover_path.split('/')[-1], f, 'image/jpeg')}
    r2 = s.post(f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image', files=files, timeout=60)
resp = r2.json()
print(resp.get('media_id',''))
" "$COVER_PATH")
    
    if [ -n "$THUMB_MEDIA_ID" ]; then
        echo "封面上传成功: $THUMB_MEDIA_ID"
    fi
fi

# 执行推送
echo "推送草稿箱..."
python3 "$SKILL_DIR/scripts/push_draft.py" "$TITLE" "$HTML_FILE" "$DIGEST" "$THUMB_MEDIA_ID"
