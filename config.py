BOT_API_TOKEN = '5775245125:AAGFxKnUcz-nH9q4nABWIP-8JzKB5Y5eDiQ'

HOROSCOPE_URL = 'https://1001goroskop.ru/?znak='

ZODIACS = {
    'Овен': 'aries',
    'Телец': 'taurus',
    'Близнецы': 'gemini',
    'Рак': 'cancer',
    'Лев': 'leo',
    'Дева': 'virgo',
    'Весы': 'libra',
    'Скорпион': 'scorpio',
    'Стрелец': 'sagittarius',
    'Козерог': 'capricorn',
    'Водолей': 'aquarius',
    'Рыбы': 'pisces'
}

FUNY_STICKERS = [
    r'CAACAgIAAxkBAAEF9l5jNw54Bay8iLpuRe9ZDk6P_JQmzAAC8x8AAtYAAaBJFivStpTRYM8qBA',
    r'CAACAgIAAxkBAAEF9mBjNw6jG6KF2YoEp1bH_KtQUq-bkAACHxgAAnwYUEs7tw8AAQh9rfEqBA',
    r'CAACAgIAAxkBAAEF9mJjNw6yVaxJtTc3zMK_zXdcpUrd1QACgxcAAkG5SEv9LGdSRMElwSoE',
    r'CAACAgIAAxkBAAEF9mRjNw6_tLUhKTmmpBKUtCet3IVcaAAC0xwAAndkAUlFY4prcKJTySoE',
    r'CAACAgIAAxkBAAEF9mZjNw7lGBKleFqpn3HgtFvIhGakYQACcSAAAngKqEhGgCkpIWcd4CoE',
    r'CAACAgIAAxkBAAEF9mhjNw74sDP6NQABjyB3w3cla8rVqTYAAtAfAAKAkjBJXazaURDg9R8qBA',
    r'CAACAgIAAxkBAAEF9mpjNw8D8LhhH03HddUju21LOi-CAQACgwEAAksODwABETQ9CyUNJfwqBA',
    r'CAACAgEAAxkBAAEF9m5jNw8VIBLaXjJk91JyqM0yle2ywAACeAADzOwNIKV7AWTXS5a3KgQ',
    r'CAACAgIAAxkBAAEF9nBjNw8f1fABuJpdZ_O6JXTpDB9dxQAC1h8AAqGwgUipeK0no0CzYSoE',
    r'CAACAgIAAxkBAAEF9nJjNw8tCo2xotuv619LealSgPSNwgACfh8AAh8_UUjCjSxA1VHWyioE',
    r'CAACAgUAAxkBAAEF9nRjNw813lpIlqiDhgl-GVY2EMWh7wACAQIAAhPSiVVscGbgN7Q4NioE',
    r'CAACAgIAAxkBAAEF9nZjNw9mZ-6Xi0Z-sVPX3uP7G1dKyAACGhoAAvIIiEnfbYu6d9ZPLyoE',
    r'CAACAgIAAxkBAAEF9nhjNw9o3t_-jfc22KyGcO87qJkAAeMAApUbAAJaeIFJuz_lINwi5XIqBA',
    r'CAACAgIAAxkBAAEF9npjNw99RihiyXI1r1HhDeRNLc5vKQACEAADO3teCtNRfbBBCUjFKgQ',
    r'CAACAgIAAxkBAAEF9nxjNw-J4rfe9KOF0BZPM0KgAoxTuQACVh0AAhzIAAFLPWA7Rti41BsqBA',
    r'CAACAgIAAxkBAAEF9n5jNw-ameBCaGqsyZoI5yLciv7vYQACVhMAAqjKEUhodlVXf60UXCoE',
    r'CAACAgIAAxkBAAEF9oBjNw-nZYtRZac92nkqPkpldN-DXQAC3w8AAhxwSEnyUgQg1CF9BCoE',
    r'CAACAgIAAxkBAAEF9oJjNw-_AAE7qFkYEY9Jm4akYlEbQBcAArwCAAJWnb0Kw0-SBqhuCWsqBA',
    r'CAACAgIAAxkBAAEF9oRjNw_M2ip3uUD2S-mGO0h_KBXy2gACVgEAAhAabSLlG4wu95KQ9ioE'
]

SHOCK_STICKERS = [
    r'CAACAgIAAxkBAAEF_BBjOmphQwEiCm1bFUcvHNECC3g3hwACNx8AAtqnwElx1TM-_AnG6CoE',
    r'CAACAgIAAxkBAAEF_BBjOmphQwEiCm1bFUcvHNECC3g3hwACNx8AAtqnwElx1TM-_AnG6CoE',
    r'CAACAgIAAxkBAAEF_BJjOmp0zDEka5jeJ2V81FUaTH792wAC3hsAAjwqwUm9jFkQ-Cf91CoE',
    r'CAACAgIAAxkBAAEF_BRjOmp8u_qi2DWza1ThSPrXOO15awACICIAAt_GwEktf0gc4t3T6ioE',
    r'CAACAgIAAxkBAAEF_BZjOmqysICJVJnxEa84I83XrLxQGwACiCEAAnk1YEjF7RgSUCNNqioE',
    r'CAACAgIAAxkBAAEF_BhjOmrFIcSu5WYPHPK2DMA1RohqxQACsh0AAonwaEg-3FBNab7lxCoE',
    r'CAACAgIAAxkBAAEF_BpjOmrHARQc4CVLF95fd-tA8N0G9AACqx4AAkvwaEiA99nNOZW40CoE',
    r'CAACAgIAAxkBAAEF_BxjOmrSCq4f3dCZ2Uz261-L7m2NcgACBBcAAioTSEsNdp9G7XDZmyoE',
    r'AACAgIAAxkBAAEF_B5jOmrYYm_nt3dCvNzevAXmtWfUzwACBhUAAi83SUs_IQ3eiTp9uioE',
    r'CAACAgIAAxkBAAEF_CBjOmrnlYwjQdt5qN6ZVT5XAAFBdmQAAoEcAAKGbklJGXqXPLJp2m8qBA',
    r'CAACAgIAAxkBAAEF_CJjOmrywIccGZ00j1n2MS5Yd-9k2QACYA4AAtOjeEjkA5jWn6WlSyoE',
    r'CAACAgIAAxkBAAEF_CRjOmsDEpB9O9N1cUDkRJFN6TWongACEhoAAqs-OUmefz1sAeIKmioE',
    r'CAACAgIAAxkBAAEF_CVjOmsEeyqMpiDN9CefdRqPGCnC-QACmh4AArnQOElQMqtCWphS8CoE',
    r'CAACAgIAAxkBAAEF_ChjOmsIGAABo_8EXOKu_gERA2Q4O4YAAqABAAJLDg8AATkLCKxNoz5AKgQ',
    r'CAACAgEAAxkBAAEF_CpjOmsNluJ6Ee3HBLQ0sJPrtRNYXgACYgADzOwNIKFPncsqJw40KgQ',
    r'CAACAgUAAxkBAAEF_C1jOmsUKrVgYqWGRR-OxZ2LlGutowACbgEAAnVrkVVGJU9uWgizBCoE',
    r'CAACAgIAAxkBAAEF_DBjOmsWtDFZdodtS2U0ElaSQTqzZAACURwAAhzzUUiXaPa7xf1wNSoE'
]

GOODMAN_STICKERS = [
    r'CAACAgIAAxkBAAEF_DRjOmwknAgLs5qkS19SsC2Aye7svAACog8AAiFQ-Ehdi-Xqd2-fhCoE',
    r'CAACAgIAAxkBAAEF_DVjOmwl79oFI_6-L0ABvBbjQc-BEgACHw4AAupQ-Ehu3Fz52zoO2yoE',
    r'CAACAgIAAxkBAAEF_DdjOmwmeBPGZR2esfK2x6dRSu4bOAACWBQAAjBE-EjwNbvNCZ7aECoE',
    r'CAACAgIAAxkBAAEF_DpjOmwqZ-66MAPCPvhI4rkZIyNGuQACaA8AAi38AUnlpsXzzLmvFioE',
    r'CAACAgIAAxkBAAEF_DxjOmwrvoQybiTw_s6WKVA4FBClAwACfBEAAk2w-EhkzHIut5C61ioE',
    r'CAACAgIAAxkBAAEF_D5jOmwt_WdzBakbhgl0V-m5F5gOnAACvhEAAvpP-EgKBbUn8Ot4dyoE',
    r'CAACAgIAAxkBAAEF_EBjOmxACyLWyhosDc-S8rXlWsvSKAACvhQAAiMM-UjaiiWaH7q1IioE'
]
