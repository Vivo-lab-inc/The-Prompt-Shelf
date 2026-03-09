#!/bin/bash
# notify-search-engines.sh — デプロイ後にIndexNowでサーチエンジンに通知

SITE_URL="https://thepromptshelf.dev"
SITEMAP_URL="$SITE_URL/sitemap-index.xml"
INDEXNOW_KEY="8397e05fd39843bcb9945bd5f13312ed"

echo "=== Search Engine Notification (IndexNow) ==="
echo "Site: $SITE_URL"
echo ""

# サイトマップから全URLを抽出（macOS互換）
URL_ARRAY=$(curl -s "$SITEMAP_URL" | python3 -c "
import sys, re, json, urllib.request
content = sys.stdin.read()
sub_sitemaps = re.findall(r'<loc>([^<]+)</loc>', content)
all_urls = []
for sm in sub_sitemaps:
    try:
        sm_content = urllib.request.urlopen(sm).read().decode()
        all_urls.extend(re.findall(r'<loc>([^<]+)</loc>', sm_content))
    except: pass
if not all_urls:
    all_urls = sub_sitemaps
print(json.dumps(all_urls))
")

echo "URLs to notify: $(echo "$URL_ARRAY" | python3 -c "import sys,json; print(len(json.loads(sys.stdin.read())))")"

# IndexNow API にPOST
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://api.indexnow.org/IndexNow" \
  -H "Content-Type: application/json" \
  -d "{
    \"host\": \"thepromptshelf.dev\",
    \"key\": \"$INDEXNOW_KEY\",
    \"keyLocation\": \"$SITE_URL/$INDEXNOW_KEY.txt\",
    \"urlList\": $URL_ARRAY
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
echo "IndexNow response: HTTP $HTTP_CODE"
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "202" ]; then
  echo "IndexNow: OK"
else
  echo "IndexNow: Warning"
fi

echo "=== Done ==="
