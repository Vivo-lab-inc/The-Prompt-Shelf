#!/bin/bash
# notify-search-engines.sh — デプロイ後にサーチエンジンに通知
# IndexNow + Google/Bing Sitemap Ping

SITE_URL="https://thepromptshelf.dev"
SITEMAP_URL="$SITE_URL/sitemap-index.xml"
INDEXNOW_KEY="8397e05fd39843bcb9945bd5f13312ed"

echo "=== Search Engine Notification ==="
echo "Site: $SITE_URL"
echo "Sitemap: $SITEMAP_URL"
echo ""

# 1. IndexNow
echo "--- IndexNow ---"
URLS=$(curl -s "$SITEMAP_URL" | grep -oP '(?<=<loc>)[^<]+')
SITEMAP_URLS=""
for sm in $URLS; do
  PAGE_URLS=$(curl -s "$sm" | grep -oP '(?<=<loc>)[^<]+')
  SITEMAP_URLS="$SITEMAP_URLS $PAGE_URLS"
done

URL_ARRAY=$(echo $SITEMAP_URLS | tr ' ' '\n' | python3 -c "
import sys, json
urls = [l.strip() for l in sys.stdin if l.strip()]
print(json.dumps(urls))
")

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

# 2. Google Sitemap Ping
echo ""
echo "--- Google Sitemap Ping ---"
PING_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "https://www.google.com/ping?sitemap=$SITEMAP_URL")
echo "Google Ping: HTTP $PING_RESPONSE"

# 3. Bing Sitemap Ping
echo ""
echo "--- Bing Sitemap Ping ---"
BING_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "https://www.bing.com/ping?sitemap=$SITEMAP_URL")
echo "Bing Ping: HTTP $BING_RESPONSE"

echo ""
echo "=== Notification Complete ==="
