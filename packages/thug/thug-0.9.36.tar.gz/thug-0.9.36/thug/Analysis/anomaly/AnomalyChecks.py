ELEMENT_ALERTS = {
    'OUT_OF_HTML' : "[ANOMALY] Detected {} element (type: {}) out of HTML tag ({})",
    'IN_HEAD'     : "[ANOMALY] Detected {} element (type: {}) in HEAD tag ({})",
}
    
ELEMENT_CHECKLIST = {
    'script' : [
        ('check_element_out_of_html', ('potentially compromised website', )),
        ('check_element_in_head'    , ('potentially compromised website', )),
    ],
}
