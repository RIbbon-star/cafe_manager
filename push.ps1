param([string]$msg = "Update")
# 실행할 때 메시지 안 넣으면 "Update"가 기본값

git add .
git commit -m $msg
git push

# .\push.ps1