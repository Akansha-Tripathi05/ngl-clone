// Simple heuristics to detect username:
// 1) look for `u` query param: ?u=username
// 2) look for instagram profile in document.referrer like https://www.instagram.com/username/
// 3) fallback null
function getQueryParam(name) {
  const url = new URL(window.location.href);
  return url.searchParams.get(name);
}

function parseReferrerForInstagram() {
  try {
    const r = document.referrer;
    if(!r) return null;
    const u = new URL(r);
    if(u.hostname.includes('instagram.com')) {
      // path like /username/ or /username
      const parts = u.pathname.split('/').filter(Boolean);
      if(parts.length >= 1) return parts[0];
    }
    // For whatsapp, if referrer contains wa.me or web.whatsapp, not helpful for username
    return null;
  } catch (e) {
    return null;
  }
}

function detectUsername() {
  const q = getQueryParam('u') || getQueryParam('username');
  if(q) return q;
  const ref = parseReferrerForInstagram();
  if(ref) return ref;
  return null;
}
