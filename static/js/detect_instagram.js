// Enhanced Device and Location Detection

// Parse User Agent to get detailed device info
function parseUserAgent() {
  const ua = navigator.userAgent;
  
  // Detect device type
  let deviceType = 'Desktop';
  if (/iPad/.test(ua)) deviceType = 'iPad';
  else if (/iPhone/.test(ua)) deviceType = 'iPhone';
  else if (/Android/.test(ua) && /Mobile/.test(ua)) deviceType = 'Android Phone';
  else if (/Android/.test(ua)) deviceType = 'Android Tablet';
  else if (/Windows Phone/.test(ua)) deviceType = 'Windows Phone';
  
  // Detect browser/app
  let browser = 'Unknown Browser';
  if (/Instagram/.test(ua)) browser = 'Instagram App';
  else if (/FBAN|FBAV/.test(ua)) browser = 'Facebook App';
  else if (/WhatsApp/.test(ua)) browser = 'WhatsApp';
  else if (/Snapchat/.test(ua)) browser = 'Snapchat';
  else if (/Twitter/.test(ua)) browser = 'Twitter App';
  else if (/EdgiOS/.test(ua)) browser = 'Edge iOS';
  else if (/CriOS/.test(ua)) browser = 'Chrome iOS';
  else if (/FxiOS/.test(ua)) browser = 'Firefox iOS';
  else if (/Safari/.test(ua) && /Version/.test(ua)) browser = 'Safari';
  else if (/Chrome/.test(ua) && !/Edge/.test(ua)) browser = 'Chrome';
  else if (/Firefox/.test(ua)) browser = 'Firefox';
  else if (/Edge/.test(ua)) browser = 'Edge';
  
  // Detect OS version
  let os = 'Unknown OS';
  let osVersion = '';
  
  if (/iPhone|iPad/.test(ua)) {
    os = 'iOS';
    const match = ua.match(/OS (\d+)_(\d+)_?(\d+)?/);
    if (match) {
      osVersion = match[1] + '.' + match[2] + (match[3] ? '.' + match[3] : '');
    }
  } else if (/Android/.test(ua)) {
    os = 'Android';
    const match = ua.match(/Android (\d+(\.\d+)?)/);
    if (match) {
      osVersion = match[1];
    }
  } else if (/Windows/.test(ua)) {
    os = 'Windows';
    if (/Windows NT 10/.test(ua)) osVersion = '10';
    else if (/Windows NT 6.3/.test(ua)) osVersion = '8.1';
    else if (/Windows NT 6.2/.test(ua)) osVersion = '8';
  } else if (/Mac OS X/.test(ua)) {
    os = 'macOS';
    const match = ua.match(/Mac OS X (\d+)[_.](\d+)/);
    if (match) {
      osVersion = match[1] + '.' + match[2];
    }
  }
  
  // Detect device model (for iPhones)
  let deviceModel = '';
  const screenWidth = window.screen.width;
  const screenHeight = window.screen.height;
  const pixelRatio = window.devicePixelRatio || 1;
  
  if (deviceType === 'iPhone') {
    // Guess iPhone model based on screen size
    const size = Math.max(screenWidth, screenHeight) * pixelRatio;
    if (size >= 2796) deviceModel = 'iPhone 15 Pro Max / 14 Pro Max';
    else if (size >= 2556) deviceModel = 'iPhone 15 Pro / 14 Pro';
    else if (size >= 2532) deviceModel = 'iPhone 15 / 14 / 13 / 12';
    else if (size >= 2436) deviceModel = 'iPhone X / XS / 11 Pro';
    else if (size >= 2208) deviceModel = 'iPhone 8 Plus / 7 Plus';
    else if (size >= 1920) deviceModel = 'iPhone 8 / 7 / 6s';
    else if (size >= 1334) deviceModel = 'iPhone SE';
  } else if (deviceType === 'iPad') {
    const size = Math.max(screenWidth, screenHeight) * pixelRatio;
    if (size >= 2732) deviceModel = 'iPad Pro 12.9"';
    else if (size >= 2388) deviceModel = 'iPad Pro 11"';
    else deviceModel = 'iPad / iPad Air / iPad Mini';
  }
  
  return {
    deviceType,
    deviceModel,
    browser,
    os,
    osVersion,
    screenSize: `${screenWidth}x${screenHeight}`,
    pixelRatio,
    userAgent: ua
  };
}

// Get location using multiple APIs
async function getLocationData() {
  try {
    // Try IP-based geolocation
    const response = await fetch('https://ipapi.co/json/', {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    
    if (response.ok) {
      const data = await response.json();
      return {
        city: data.city || 'Unknown',
        region: data.region || 'Unknown',
        country: data.country_name || 'Unknown',
        countryCode: data.country_code || '',
        postal: data.postal || '',
        latitude: data.latitude || null,
        longitude: data.longitude || null,
        timezone: data.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone,
        isp: data.org || 'Unknown ISP',
        ip: data.ip || 'Unknown'
      };
    }
  } catch (e) {
    console.log('Primary geolocation failed, trying backup...');
  }
  
  // Backup method using ipify + ipwhois
  try {
    const ipResponse = await fetch('https://api.ipify.org?format=json');
    const ipData = await ipResponse.json();
    
    return {
      city: 'Unknown',
      region: 'Unknown',
      country: 'Unknown',
      countryCode: '',
      postal: '',
      latitude: null,
      longitude: null,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      isp: 'Unknown ISP',
      ip: ipData.ip
    };
  } catch (e) {
    console.error('All geolocation methods failed');
  }
  
  // Final fallback
  return {
    city: 'Unknown',
    region: 'Unknown',
    country: 'Unknown',
    countryCode: '',
    postal: '',
    latitude: null,
    longitude: null,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    isp: 'Unknown ISP',
    ip: 'Unknown'
  };
}

// Get battery info (helps identify device)
async function getBatteryInfo() {
  try {
    if ('getBattery' in navigator) {
      const battery = await navigator.getBattery();
      return {
        charging: battery.charging,
        level: Math.round(battery.level * 100),
        chargingTime: battery.chargingTime,
        dischargingTime: battery.dischargingTime
      };
    }
  } catch (e) {}
  return null;
}

// Get connection info
function getConnectionInfo() {
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if (connection) {
    return {
      type: connection.effectiveType || connection.type || 'unknown',
      downlink: connection.downlink || null,
      rtt: connection.rtt || null,
      saveData: connection.saveData || false
    };
  }
  return null;
}

// Canvas fingerprint for tracking
async function getCanvasFingerprint() {
  try {
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 50;
    const ctx = canvas.getContext('2d');
    
    ctx.textBaseline = 'top';
    ctx.font = '14px "Arial"';
    ctx.fillStyle = '#f60';
    ctx.fillRect(125, 1, 62, 20);
    ctx.fillStyle = '#069';
    ctx.fillText('Device ID', 2, 15);
    
    const dataURL = canvas.toDataURL();
    
    // Create simple hash
    let hash = 0;
    for (let i = 0; i < dataURL.length; i++) {
      const char = dataURL.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).substring(0, 12).toUpperCase();
  } catch (e) {
    return 'UNKNOWN';
  }
}

// Main function to collect all data
async function collectDeviceAndLocationData() {
  console.log('📱 Collecting device and location data...');
  
  const deviceInfo = parseUserAgent();
    const locationData = await getLocationData();
  const batteryInfo = await getBatteryInfo();
  const connectionInfo = getConnectionInfo();
  const fingerprint = await getCanvasFingerprint();
  
  const data = {
    // Device info
    deviceType: deviceInfo.deviceType,
    deviceModel: deviceInfo.deviceModel,
    browser: deviceInfo.browser,
    os: deviceInfo.os,
    osVersion: deviceInfo.osVersion,
    screenSize: deviceInfo.screenSize,
    pixelRatio: deviceInfo.pixelRatio,
    
    // Location info
    city: locationData.city,
    region: locationData.region,
    country: locationData.country,
    countryCode: locationData.countryCode,
    timezone: locationData.timezone,
    isp: locationData.isp,
    ip: locationData.ip,
    coordinates: locationData.latitude && locationData.longitude 
      ? `${locationData.latitude},${locationData.longitude}` 
      : null,
    
    // Additional info
    battery: batteryInfo,
    connection: connectionInfo,
    fingerprint: fingerprint,
    
    // Timestamps
    timestamp: new Date().toISOString(),
    localTime: new Date().toLocaleString()
  };
  
  console.log('✅ Data collected:', data);
  return data;
}