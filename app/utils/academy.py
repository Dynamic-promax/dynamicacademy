"""
Central academy information, mirrored into every template via a Flask
context processor (see app/__init__.py -> inject_academy_info).

Change the academy name, phone numbers, address, or social links HERE
and they update everywhere on the site - templates should never
hard-code this information directly.
"""

ACADEMY = {
    "name": "Dynamic Academy",
    "motto": "Think. Learn. Create. Lead.",
    "tagline": "Practical education for the next generation of creators, problem-solvers and technology leaders.",
    "phone": "0811 900 1010",              # general enquiries line
    "phone_display": "0811 900 1010",
    "whatsapp_number": "2349090575783",    # registration/contact WhatsApp (08119001010)
    "whatsapp_display": "0909 057 5783",
    "email": "info@dynamicacademy.ng",     # placeholder - update once a real inbox exists
    "address": "Apex Garden Estate, Kukwaba District, Abuja, Nigeria",
    "address_line1": "Apex Garden Estate",
    "address_line2": "Kukwaba District, Abuja, Nigeria",
    "google_maps_url": "https://www.google.com/maps/search/?api=1&query=Kukwaba+District+Abuja+Nigeria",
    "google_maps_embed": "https://www.google.com/maps?q=Kukwaba+District+Abuja+Nigeria&output=embed",
    "social": {
        "facebook": "https://facebook.com/DynamicAcademyai",
        "instagram": "https://instagram.com/dynamic_academy.ai",
        "tiktok": "https://tiktok.com/@dynamicacademy_ai",
        "youtube": "https://youtube.com/@DynamicAcademy-ai",
        "linkedin": "https://linkedin.com/company/dynamicacademy",
    },
}

WHATSAPP_MESSAGES = {
    "general": "Hello Dynamic Academy, I would like to enquire about your courses.",
    "course": lambda name: f"Hello Dynamic Academy, I am interested in enrolling in {name}.",
    "parent": "Hello Dynamic Academy, I would like to register my child for a course.",
    "tutor": "Hello Dynamic Academy, I am interested in applying to teach at Dynamic Academy.",
    "corporate": "Hello Dynamic Academy, I would like to enquire about corporate training for my organisation.",
    "program": lambda name: f"Hello Dynamic Academy, I would like to enquire about the {name} programme.",
}
