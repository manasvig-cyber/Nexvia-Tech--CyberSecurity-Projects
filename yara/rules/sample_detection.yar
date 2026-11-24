rule MalwareBazaar_3797d508_IP_Profiler {
    meta:
        description = "Detects 64-bit Windows sample querying pro.ip-api.com for host geolocation"
        author = "Manasvi V"
        sha256 = "3797d5082f3612a2493ce6430ed09a61922573f6871401f95b0d2e735a12ada1"
        date = "2026-11-24"
    strings:
        $mz = { 4D 5A }
        $api_url = "https://pro.ip-api.com/line/?key=QPVvv1rHQJD2pd2&fields=25948155" ascii wide
        $domain1 = "pro.ip-api.com" ascii wide
        $domain2 = "BreakingSecurity.net" ascii wide
    condition:
        $mz at 0 and ($api_url or ($domain1 and $domain2))
}
