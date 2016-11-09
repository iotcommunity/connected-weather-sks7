'''
This workflow looks up the device location based on IP address.  It then looks up the weather
based on the location.  The workflow will publish a MQTT message back to the device with location
and weather information.

'''
import M1Geolocation
import Weather
import json
import MQTT
import datetime
from datetime import timedelta
import DateConversion


# WAN IP address of the board
current_ip = IONode.get_input('in1')['event_data']['value']

# LAN IP address of the board
lan_ip = IONode.get_input('in3')['event_data']['value']

# Timezone lookup
timezone_lookup = [
  {
    "offset": -12,
    "utc": [
      "Etc/GMT+12"
    ]
  },
  {
    "offset": -11,
    "utc": [
      "Etc/GMT+11",
      "Pacific/Midway",
      "Pacific/Niue",
      "Pacific/Pago_Pago"
    ]
  },
  {
    "offset": -10,
    "utc": [
      "Etc/GMT+10",
      "Pacific/Honolulu",
      "Pacific/Johnston",
      "Pacific/Rarotonga",
      "Pacific/Tahiti"
    ]
  },
  {
    "offset": -8,
    "utc": [
      "America/Anchorage",
      "America/Juneau",
      "America/Nome",
      "America/Sitka",
      "America/Yakutat"
    ]
  },
  {
    "offset": -7,
    "utc": [
      "America/Santa_Isabel"
    ]
  },
  {
    "offset": -7,
    "utc": [
      "America/Dawson",
      "America/Los_Angeles",
      "America/Tijuana",
      "America/Vancouver",
      "America/Whitehorse",
      "PST8PDT"
    ]
  },
  {
    "offset": -7,
    "utc": [
      "America/Creston",
      "America/Dawson_Creek",
      "America/Hermosillo",
      "America/Phoenix",
      "Etc/GMT+7"
    ]
  },
  {
    "offset": -6,
    "utc": [
      "America/Chihuahua",
      "America/Mazatlan"
    ]
  },
  {
    "offset": -6,
    "utc": [
      "America/Boise",
      "America/Cambridge_Bay",
      "America/Denver",
      "America/Edmonton",
      "America/Inuvik",
      "America/Ojinaga",
      "America/Yellowknife",
      "MST7MDT"
    ]
  },
  {
    "offset": -6,
    "utc": [
      "America/Belize",
      "America/Costa_Rica",
      "America/El_Salvador",
      "America/Guatemala",
      "America/Managua",
      "America/Tegucigalpa",
      "Etc/GMT+6",
      "Pacific/Galapagos"
    ]
  },
  {
    "offset": -5,
    "utc": [
      "America/Chicago",
      "America/Indiana/Knox",
      "America/Indiana/Tell_City",
      "America/Matamoros",
      "America/Menominee",
      "America/North_Dakota/Beulah",
      "America/North_Dakota/Center",
      "America/North_Dakota/New_Salem",
      "America/Rainy_River",
      "America/Rankin_Inlet",
      "America/Resolute",
      "America/Winnipeg",
      "CST6CDT"
    ]
  },
  {
    "offset": -5,
    "utc": [
      "America/Bahia_Banderas",
      "America/Cancun",
      "America/Merida",
      "America/Mexico_City",
      "America/Monterrey"
    ]
  },
  {
    "offset": -6,
    "utc": [
      "America/Regina",
      "America/Swift_Current"
    ]
  },
  {
    "offset": -5,
    "utc": [
      "America/Bogota",
      "America/Cayman",
      "America/Coral_Harbour",
      "America/Eirunepe",
      "America/Guayaquil",
      "America/Jamaica",
      "America/Lima",
      "America/Panama",
      "America/Rio_Branco",
      "Etc/GMT+5"
    ]
  },
  {
    "offset": -4,
    "utc": [
      "America/Detroit",
      "America/Havana",
      "America/Indiana/Petersburg",
      "America/Indiana/Vincennes",
      "America/Indiana/Winamac",
      "America/Iqaluit",
      "America/Kentucky/Monticello",
      "America/Louisville",
      "America/Montreal",
      "America/Nassau",
      "America/New_York",
      "America/Nipigon",
      "America/Pangnirtung",
      "America/Port-au-Prince",
      "America/Thunder_Bay",
      "America/Toronto",
      "EST5EDT"
    ]
  },
  {
    "offset": -4,
    "utc": [
      "America/Indiana/Marengo",
      "America/Indiana/Vevay",
      "America/Indianapolis"
    ]
  },
  {
    "offset": -4.5,
    "utc": [
      "America/Caracas"
    ]
  },
  {
    "offset": -4,
    "utc": [
      "America/Asuncion"
    ]
  },
  {
    "offset": -3,
    "utc": [
      "America/Glace_Bay",
      "America/Goose_Bay",
      "America/Halifax",
      "America/Moncton",
      "America/Thule",
      "Atlantic/Bermuda"
    ]
  },
  {
    "offset": -4,
    "utc": [
      "America/Campo_Grande",
      "America/Cuiaba"
    ]
  },
  {
    "offset": -4,
    "utc": [
      "America/Anguilla",
      "America/Antigua",
      "America/Aruba",
      "America/Barbados",
      "America/Blanc-Sablon",
      "America/Boa_Vista",
      "America/Curacao",
      "America/Dominica",
      "America/Grand_Turk",
      "America/Grenada",
      "America/Guadeloupe",
      "America/Guyana",
      "America/Kralendijk",
      "America/La_Paz",
      "America/Lower_Princes",
      "America/Manaus",
      "America/Marigot",
      "America/Martinique",
      "America/Montserrat",
      "America/Port_of_Spain",
      "America/Porto_Velho",
      "America/Puerto_Rico",
      "America/Santo_Domingo",
      "America/St_Barthelemy",
      "America/St_Kitts",
      "America/St_Lucia",
      "America/St_Thomas",
      "America/St_Vincent",
      "America/Tortola",
      "Etc/GMT+4"
    ]
  },
  {
    "offset": -4,
    "utc": [
      "America/Santiago",
      "Antarctica/Palmer"
    ]
  },
  {
    "offset": -2.5,
    "utc": [
      "America/St_Johns"
    ]
  },
  {
    "offset": -3,
    "utc": [
      "America/Sao_Paulo"
    ]
  },
  {
    "offset": -3,
    "utc": [
      "America/Argentina/La_Rioja",
      "America/Argentina/Rio_Gallegos",
      "America/Argentina/Salta",
      "America/Argentina/San_Juan",
      "America/Argentina/San_Luis",
      "America/Argentina/Tucuman",
      "America/Argentina/Ushuaia",
      "America/Buenos_Aires",
      "America/Catamarca",
      "America/Cordoba",
      "America/Jujuy",
      "America/Mendoza"
    ]
  },
  {
    "offset": -3,
    "utc": [
      "America/Araguaina",
      "America/Belem",
      "America/Cayenne",
      "America/Fortaleza",
      "America/Maceio",
      "America/Paramaribo",
      "America/Recife",
      "America/Santarem",
      "Antarctica/Rothera",
      "Atlantic/Stanley",
      "Etc/GMT+3"
    ]
  },
  {
    "offset": -2,
    "utc": [
      "America/Godthab"
    ]
  },
  {
    "offset": -3,
    "utc": [
      "America/Montevideo"
    ]
  },
  {
    "offset": -3,
    "utc": [
      "America/Bahia"
    ]
  },
  {
    "offset": -2,
    "utc": [
      "America/Noronha",
      "Atlantic/South_Georgia",
      "Etc/GMT+2"
    ]
  },
  {
    "offset": -1,
  },
  {
    "offset": 0,
    "utc": [
      "America/Scoresbysund",
      "Atlantic/Azores"
    ]
  },
  {
    "offset": -1,
    "utc": [
      "Atlantic/Cape_Verde",
      "Etc/GMT+1"
    ]
  },
  {
    "offset": 1,
    "utc": [
      "Africa/Casablanca",
      "Africa/El_Aaiun"
    ]
  },
  {
    "offset": 0,
    "utc": [
      "America/Danmarkshavn",
      "Etc/GMT"
    ]
  },
  {
    "offset": 1,
    "utc": [
      "Atlantic/Canary",
      "Atlantic/Faeroe",
      "Atlantic/Madeira",
      "Europe/Dublin",
      "Europe/Guernsey",
      "Europe/Isle_of_Man",
      "Europe/Jersey",
      "Europe/Lisbon",
      "Europe/London"
    ]
  },
  {
    "offset": 0,
    "utc": [
      "Africa/Abidjan",
      "Africa/Accra",
      "Africa/Bamako",
      "Africa/Banjul",
      "Africa/Bissau",
      "Africa/Conakry",
      "Africa/Dakar",
      "Africa/Freetown",
      "Africa/Lome",
      "Africa/Monrovia",
      "Africa/Nouakchott",
      "Africa/Ouagadougou",
      "Africa/Sao_Tome",
      "Atlantic/Reykjavik",
      "Atlantic/St_Helena"
    ]
  },
  {
    "offset": 2,
    "utc": [
      "Arctic/Longyearbyen",
      "Europe/Amsterdam",
      "Europe/Andorra",
      "Europe/Berlin",
      "Europe/Busingen",
      "Europe/Gibraltar",
      "Europe/Luxembourg",
      "Europe/Malta",
      "Europe/Monaco",
      "Europe/Oslo",
      "Europe/Rome",
      "Europe/San_Marino",
      "Europe/Stockholm",
      "Europe/Vaduz",
      "Europe/Vatican",
      "Europe/Vienna",
      "Europe/Zurich"
    ]
  },
  {
    "offset": 2,
    "utc": [
      "Europe/Belgrade",
      "Europe/Bratislava",
      "Europe/Budapest",
      "Europe/Ljubljana",
      "Europe/Podgorica",
      "Europe/Prague",
      "Europe/Tirane"
    ]
  },
  {
    "offset": 2,
    "utc": [
      "Africa/Ceuta",
      "Europe/Brussels",
      "Europe/Copenhagen",
      "Europe/Madrid",
      "Europe/Paris"
    ]
  },
  {
    "offset": 2,
    "utc": [
      "Europe/Sarajevo",
      "Europe/Skopje",
      "Europe/Warsaw",
      "Europe/Zagreb"
    ]
  },
  {
    "offset": 1,
    "utc": [
      "Africa/Algiers",
      "Africa/Bangui",
      "Africa/Brazzaville",
      "Africa/Douala",
      "Africa/Kinshasa",
      "Africa/Lagos",
      "Africa/Libreville",
      "Africa/Luanda",
      "Africa/Malabo",
      "Africa/Ndjamena",
      "Africa/Niamey",
      "Africa/Porto-Novo",
      "Africa/Tunis",
      "Etc/GMT-1"
    ]
  },
  {
    "offset": 1,
    "utc": [
      "Africa/Windhoek"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Nicosia",
      "Europe/Athens",
      "Europe/Bucharest",
      "Europe/Chisinau"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Beirut"
    ]
  },
  {
    "offset": 2,
    "utc": [
      "Africa/Cairo"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Damascus"
    ]
  },
  {
    "offset": 3,
  },
  {
    "offset": 2,
    "utc": [
      "Africa/Blantyre",
      "Africa/Bujumbura",
      "Africa/Gaborone",
      "Africa/Harare",
      "Africa/Johannesburg",
      "Africa/Kigali",
      "Africa/Lubumbashi",
      "Africa/Lusaka",
      "Africa/Maputo",
      "Africa/Maseru",
      "Africa/Mbabane",
      "Etc/GMT-2"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Europe/Helsinki",
      "Europe/Kiev",
      "Europe/Mariehamn",
      "Europe/Riga",
      "Europe/Sofia",
      "Europe/Tallinn",
      "Europe/Uzhgorod",
      "Europe/Vilnius",
      "Europe/Zaporozhye"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Europe/Istanbul"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Jerusalem"
    ]
  },
  {
    "offset": 2,
    "utc": [
      "Africa/Tripoli"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Amman"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Baghdad"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Europe/Kaliningrad",
      "Europe/Minsk"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Asia/Aden",
      "Asia/Bahrain",
      "Asia/Kuwait",
      "Asia/Qatar",
      "Asia/Riyadh"
    ]
  },
  {
    "offset": 3,
    "utc": [
      "Africa/Addis_Ababa",
      "Africa/Asmera",
      "Africa/Dar_es_Salaam",
      "Africa/Djibouti",
      "Africa/Juba",
      "Africa/Kampala",
      "Africa/Khartoum",
      "Africa/Mogadishu",
      "Africa/Nairobi",
      "Antarctica/Syowa",
      "Etc/GMT-3",
      "Indian/Antananarivo",
      "Indian/Comoro",
      "Indian/Mayotte"
    ]
  },
  {
    "offset": 4.5,
    "utc": [
      "Asia/Tehran"
    ]
  },
  {
    "offset": 4,
    "utc": [
      "Asia/Dubai",
      "Asia/Muscat",
      "Etc/GMT-4"
    ]
  },
  {
    "offset": 5,
    "utc": [
      "Asia/Baku"
    ]
  },
  {
    "offset": 4,
    "utc": [
      "Europe/Moscow",
      "Europe/Samara",
      "Europe/Simferopol",
      "Europe/Volgograd"
    ]
  },
  {
    "offset": 4,
    "utc": [
      "Indian/Mahe",
      "Indian/Mauritius",
      "Indian/Reunion"
    ]
  },
  {
    "offset": 4,
    "utc": [
      "Asia/Tbilisi"
    ]
  },
  {
    "offset": 4,
    "utc": [
      "Asia/Yerevan"
    ]
  },
  {
    "offset": 4.5,
    "utc": [
      "Asia/Kabul"
    ]
  },
  {
    "offset": 5,
    "utc": [
      "Antarctica/Mawson",
      "Asia/Aqtau",
      "Asia/Aqtobe",
      "Asia/Ashgabat",
      "Asia/Dushanbe",
      "Asia/Oral",
      "Asia/Samarkand",
      "Asia/Tashkent",
      "Etc/GMT-5",
      "Indian/Kerguelen",
      "Indian/Maldives"
    ]
  },
  {
    "offset": 5,
    "utc": [
      "Asia/Karachi"
    ]
  },
  {
    "offset": 5.5,
    "utc": [
      "Asia/Calcutta"
    ]
  },
  {
    "offset": 5.5,
    "utc": [
      "Asia/Colombo"
    ]
  },
  {
    "offset": 5.75,
    "utc": [
      "Asia/Katmandu"
    ]
  },
  {
    "offset": 6,
    "utc": [
      "Antarctica/Vostok",
      "Asia/Almaty",
      "Asia/Bishkek",
      "Asia/Qyzylorda",
      "Asia/Urumqi",
      "Etc/GMT-6",
      "Indian/Chagos"
    ]
  },
  {
    "offset": 6,
    "utc": [
      "Asia/Dhaka",
      "Asia/Thimphu"
    ]
  },
  {
    "offset": 6,
    "utc": [
      "Asia/Yekaterinburg"
    ]
  },
  {
    "offset": 6.5,
    "utc": [
      "Asia/Rangoon",
      "Indian/Cocos"
    ]
  },
  {
    "offset": 7,
    "utc": [
      "Antarctica/Davis",
      "Asia/Bangkok",
      "Asia/Hovd",
      "Asia/Jakarta",
      "Asia/Phnom_Penh",
      "Asia/Pontianak",
      "Asia/Saigon",
      "Asia/Vientiane",
      "Etc/GMT-7",
      "Indian/Christmas"
    ]
  },
  {
    "offset": 7,
    "utc": [
      "Asia/Novokuznetsk",
      "Asia/Novosibirsk",
      "Asia/Omsk"
    ]
  },
  {
    "offset": 8,
    "utc": [
      "Asia/Hong_Kong",
      "Asia/Macau",
      "Asia/Shanghai"
    ]
  },
  {
    "offset": 8,
    "utc": [
      "Asia/Krasnoyarsk"
    ]
  },
  {
    "offset": 8,
    "utc": [
      "Asia/Brunei",
      "Asia/Kuala_Lumpur",
      "Asia/Kuching",
      "Asia/Makassar",
      "Asia/Manila",
      "Asia/Singapore",
      "Etc/GMT-8"
    ]
  },
  {
    "offset": 8,
    "utc": [
      "Antarctica/Casey",
      "Australia/Perth"
    ]
  },
  {
    "offset": 8,
    "utc": [
      "Asia/Taipei"
    ]
  },
  {
    "offset": 8,
    "utc": [
      "Asia/Choibalsan",
      "Asia/Ulaanbaatar"
    ]
  },
  {
    "offset": 9,
    "utc": [
      "Asia/Irkutsk"
    ]
  },
  {
    "offset": 9,
    "utc": [
      "Asia/Dili",
      "Asia/Jayapura",
      "Asia/Tokyo",
      "Etc/GMT-9",
      "Pacific/Palau"
    ]
  },
  {
    "offset": 9,
    "utc": [
      "Asia/Pyongyang",
      "Asia/Seoul"
    ]
  },
  {
    "offset": 9.5,
    "utc": [
      "Australia/Adelaide",
      "Australia/Broken_Hill"
    ]
  },
  {
    "offset": 9.5,
    "utc": [
      "Australia/Darwin"
    ]
  },
  {
    "offset": 10,
    "utc": [
      "Australia/Brisbane",
      "Australia/Lindeman"
    ]
  },
  {
    "offset": 10,
    "utc": [
      "Australia/Melbourne",
      "Australia/Sydney"
    ]
  },
  {
    "offset": 10,
    "utc": [
      "Antarctica/DumontDUrville",
      "Etc/GMT-10",
      "Pacific/Guam",
      "Pacific/Port_Moresby",
      "Pacific/Saipan",
      "Pacific/Truk"
    ]
  },
  {
    "offset": 10,
    "utc": [
      "Australia/Currie",
      "Australia/Hobart"
    ]
  },
  {
    "offset": 10,
    "utc": [
      "Asia/Chita",
      "Asia/Khandyga",
      "Asia/Yakutsk"
    ]
  },
  {
    "offset": 11,
    "utc": [
      "Antarctica/Macquarie",
      "Etc/GMT-11",
      "Pacific/Efate",
      "Pacific/Guadalcanal",
      "Pacific/Kosrae",
      "Pacific/Noumea",
      "Pacific/Ponape"
    ]
  },
  {
    "offset": 11,
    "utc": [
      "Asia/Sakhalin",
      "Asia/Ust-Nera",
      "Asia/Vladivostok"
    ]
  },
  {
    "offset": 12,
    "utc": [
      "Antarctica/McMurdo",
      "Pacific/Auckland"
    ]
  },
  {
    "offset": 12,
    "utc": [
      "Etc/GMT-12",
      "Pacific/Funafuti",
      "Pacific/Kwajalein",
      "Pacific/Majuro",
      "Pacific/Nauru",
      "Pacific/Tarawa",
      "Pacific/Wake",
      "Pacific/Wallis"
    ]
  },
  {
    "offset": 12,
    "utc": [
      "Pacific/Fiji"
    ]
  },
  {
    "offset": 12,
    "utc": [
      "Asia/Anadyr",
      "Asia/Kamchatka",
      "Asia/Magadan",
      "Asia/Srednekolymsk"
    ]
  },
  {
    "offset": 13,
  },
  {
    "offset": 13,
    "utc": [
      "Etc/GMT-13",
      "Pacific/Enderbury",
      "Pacific/Fakaofo",
      "Pacific/Tongatapu"
    ]
  },
  {
    "offset": 13,
    "utc": [
      "Pacific/Apia"
    ]
  }
]

# Function: Get Current Time
def get_current_iso_time():
    dtnow = datetime.datetime.now()
    dtutcnow = datetime.datetime.utcnow()
    delta = dtnow - dtutcnow
    hh,mm = divmod((delta.days * 24*60*60 + delta.seconds + 30) // 60, 60)
    return "%s%+03d:%02d" % (dtnow.isoformat(), hh, mm)

# Get time offset
def getoffset():
    for zone in timezone_lookup:
        if "utc" in zone:
            for zone_names in zone["utc"]:
                if "America/Los_Angeles" in zone_names:
                    log("TZ Offset: "+str(zone["offset"]))
                    return zone["offset"]
    return 0

def k2f(t):
    return int(round((t*9/5.0)-459.67))

tz_offset = getoffset()
TIME_OFFSET = timedelta(hours=tz_offset)

# Get current time
now = DateConversion.to_py_datetime(get_current_iso_time())

# Offset current time with Time Zone above to prepare the charts
now_w_offset = now.astimezone(DateConversion.UTC())+TIME_OFFSET
log(str(now_w_offset))
log(str(now_w_offset.hour))
log(str(now_w_offset.minute))

# Default to city/state
city = 'unknown'
state = 'unknown'

try:
    # use M1's location services to find city where device is located
    geo_data = M1Geolocation.get_location_from_ip(current_ip)
    log(geo_data)

    # save geo-location data
    IONode.set_output('out1', geo_data)

    try:
        # save the city if it's available in the geo lookup (depends on region)
        city = str(geo_data['city']['names']['en'])
    except Exception:
        log("No city found")

    try:
        state = str(geo_data['subdivisions'][0]['names']['en'])
    except Exception:
        log("No state found")

    # get location based on IP address
    gps_location = str(geo_data['location']['latitude']) + " " + str(geo_data['location']['longitude'])

    # save location result
    IONode.set_output('out3', {"gps_location":gps_location})

    # get current weather
    current_weather = Weather.get_weather_by_coordinates(float(gps_location.split(' ')[0]), float(gps_location.split(' ')[1]))

    # get weather forecast
    forecast_weather = Weather.get_5_day_forecast_by_coordinates(float(gps_location.split(' ')[0]), float(gps_location.split(' ')[1]))
    log(forecast_weather)

    # map weather to string for board
    weather_condition_forecast_map = {
            '01d':'Clear Skies',
            '01n':'Clear Skies',
            '02d':'Few Clouds',
            '02n':'Few Clouds',
            '03d':'Partly Cloudy',
            '03n':'Partly Cloudy',
            '04d':'Broken clouds',
            '04n':'Broken clouds',
            '09d':'Showers',
            '09n':'Showers',
            '10d':'Rain',
            '10n':'Rain',
            '11d':'Thunderstorm',
            '11n':'Thunderstorm',
            '13d':'Snow',
            '13n':'Snow',
            '50d':'Mist',
            '50n':'Mist'
    }

    weather_condition_map = {
            '01d':'Clear Skies',
            '01n':'Night Time',
            '02d':'Few Clouds',
            '02n':'Night Time',
            '03d':'Partly Cloudy',
            '03n':'Night Time',
            '04d':'broken clouds',
            '04n':'Night Time',
            '09d':'Showers',
            '09n':'Night Time',
            '10d':'Rain',
            '10n':'Night Time',
            '11d':'Thunderstorm',
            '11n':'Night Time',
            '13d':'Snow',
            '13n':'Night Time',
            '50d':'Mist',
            '50n':'Night Time'
    }

    # map weather to background image for board
    weather_pixel_forecast_background_map = {
            '01d':'GX_PIXELMAP_ID_BG_SUNNY',
            '01n':'GX_PIXELMAP_ID_BG_SUNNY',
            '02d':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '02n':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '03d':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '03n':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '04d':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '04n':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '09d':'GX_PIXELMAP_ID_BG_RAINY',
            '09n':'GX_PIXELMAP_ID_BG_RAINY',
            '10d':'GX_PIXELMAP_ID_BG_RAINY',
            '10n':'GX_PIXELMAP_ID_BG_RAINY',
            '11d':'GX_PIXELMAP_ID_BG_RAINY',
            '11n':'GX_PIXELMAP_ID_BG_RAINY',
            '13d':'GX_PIXELMAP_ID_BG_RAINY',
            '13n':'GX_PIXELMAP_ID_BG_RAINY',
            '50d':'GX_PIXELMAP_ID_BG_RAINY',
            '50n':'GX_PIXELMAP_ID_BG_RAINY'
    }

    weather_pixel_background_map = {
            '01d':'GX_PIXELMAP_ID_BG_SUNNY',
            '01n':'GX_PIXELMAP_ID_BG_RAINY',
            '02d':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '02n':'GX_PIXELMAP_ID_BG_RAINY',
            '03d':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '03n':'GX_PIXELMAP_ID_BG_RAINY',
            '04d':'GX_PIXELMAP_ID_BG_PARTLYCLOUDY',
            '04n':'GX_PIXELMAP_ID_BG_RAINY',
            '09d':'GX_PIXELMAP_ID_BG_RAINY',
            '09n':'GX_PIXELMAP_ID_BG_RAINY',
            '10d':'GX_PIXELMAP_ID_BG_RAINY',
            '10n':'GX_PIXELMAP_ID_BG_RAINY',
            '11d':'GX_PIXELMAP_ID_BG_RAINY',
            '11n':'GX_PIXELMAP_ID_BG_RAINY',
            '13d':'GX_PIXELMAP_ID_BG_RAINY',
            '13n':'GX_PIXELMAP_ID_BG_RAINY',
            '50d':'GX_PIXELMAP_ID_BG_RAINY',
            '50n':'GX_PIXELMAP_ID_BG_RAINY'
    }

    # map weather to icon for board
    weather_pixel_forecast_icon_map = {
            '01d':'GX_PIXELMAP_ID_ICON_SUNNY',
            '01n':'GX_PIXELMAP_ID_ICON_SUNNY',
            '02d':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '02n':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '03d':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '03n':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '04d':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '04n':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '09d':'GX_PIXELMAP_ID_ICON_RAINY',
            '09n':'GX_PIXELMAP_ID_ICON_RAINY',
            '10d':'GX_PIXELMAP_ID_ICON_RAINY',
            '10n':'GX_PIXELMAP_ID_ICON_RAINY',
            '11d':'GX_PIXELMAP_ID_ICON_RAINY',
            '11n':'GX_PIXELMAP_ID_ICON_RAINY',
            '13d':'GX_PIXELMAP_ID_ICON_RAINY',
            '13n':'GX_PIXELMAP_ID_ICON_RAINY',
            '50d':'GX_PIXELMAP_ID_ICON_RAINY',
            '50n':'GX_PIXELMAP_ID_ICON_RAINY'
    }

    weather_pixel_icon_map = {
            '01d':'GX_PIXELMAP_ID_ICON_SUNNY',
            '01n':'GX_PIXELMAP_ID_ICON_RAINY',
            '02d':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '02n':'GX_PIXELMAP_ID_ICON_RAINY',
            '03d':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '03n':'GX_PIXELMAP_ID_ICON_RAINY',
            '04d':'GX_PIXELMAP_ID_ICON_CLOUDY',
            '04n':'GX_PIXELMAP_ID_ICON_RAINY',
            '09d':'GX_PIXELMAP_ID_ICON_RAINY',
            '09n':'GX_PIXELMAP_ID_ICON_RAINY',
            '10d':'GX_PIXELMAP_ID_ICON_RAINY',
            '10n':'GX_PIXELMAP_ID_ICON_RAINY',
            '11d':'GX_PIXELMAP_ID_ICON_RAINY',
            '11n':'GX_PIXELMAP_ID_ICON_RAINY',
            '13d':'GX_PIXELMAP_ID_ICON_RAINY',
            '13n':'GX_PIXELMAP_ID_ICON_RAINY',
            '50d':'GX_PIXELMAP_ID_ICON_RAINY',
            '50n':'GX_PIXELMAP_ID_ICON_RAINY'
    }

    # map weather to animation for board
    weather_pixel_anime_map = {
            '01d':'GX_PIXELMAP_ID_ANIME_SUN_SHINING',
            '01n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '02d':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '02n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '03d':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '03n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '04d':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '04n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '09d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '09n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '10d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '10n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '11d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '11n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '13d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '13n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '50d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '50n':'GX_PIXELMAP_ID_ANIME_RAINING_2'
    }

    weather_pixel_forecast_anime_map = {
            '01d':'GX_PIXELMAP_ID_ANIME_SUN_SHINING',
            '01n':'GX_PIXELMAP_ID_ANIME_SUN_SHINING',
            '02d':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '02n':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '03d':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '03n':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '04d':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '04n':'GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD',
            '09d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '09n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '10d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '10n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '11d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '11n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '13d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '13n':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '50d':'GX_PIXELMAP_ID_ANIME_RAINING_2',
            '50n':'GX_PIXELMAP_ID_ANIME_RAINING_2'
    }

    # map weather to animation setting for board
    weather_pixel_forecast_anime_map_2 = {
            '01d':'0',
            '01n':'0',
            '02d':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '02n':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '03d':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '03n':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '04d':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '04n':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '09d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '09n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '10d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '10n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '11d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '11n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '13d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '13n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '50d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '50n':'GX_PIXELMAP_ID_ANIME_RAINING_1'
    }

    weather_pixel_anime_map_2 = {
            '01d':'0',
            '01n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '02d':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '02n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '03d':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '03n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '04d':'GX_PIXELMAP_ID_ANIME_CLOUD',
            '04n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '09d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '09n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '10d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '10n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '11d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '11n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '13d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '13n':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '50d':'GX_PIXELMAP_ID_ANIME_RAINING_1',
            '50n':'GX_PIXELMAP_ID_ANIME_RAINING_1'
    }

    day_array = ["MON","TUE","WED","THU","FRI","SAT","SUN"]

    # get current day of week
    day = day_array[datetime.datetime.today().weekday()]

    # set next 3 days
    day0 = datetime.datetime.today()
    day1 = datetime.datetime.today() + datetime.timedelta(days=1)
    day2 = datetime.datetime.today() + datetime.timedelta(days=2)

    # get min temperature range over day 1
    d1_min_temp = min([forecast_weather['list'][0]['main']['temp_min'],
                       forecast_weather['list'][1]['main']['temp_min'],
                       forecast_weather['list'][2]['main']['temp_min'],
                       forecast_weather['list'][3]['main']['temp_min'],
                       forecast_weather['list'][4]['main']['temp_min'],
                       forecast_weather['list'][5]['main']['temp_min'],
                       forecast_weather['list'][6]['main']['temp_min'],
                       forecast_weather['list'][7]['main']['temp_min']])

    # get max temperature range over day 1
    d1_max_temp = max([forecast_weather['list'][0]['main']['temp_max'],
                       forecast_weather['list'][1]['main']['temp_max'],
                       forecast_weather['list'][2]['main']['temp_max'],
                       forecast_weather['list'][3]['main']['temp_max'],
                       forecast_weather['list'][4]['main']['temp_max'],
                       forecast_weather['list'][5]['main']['temp_max'],
                       forecast_weather['list'][6]['main']['temp_max'],
                       forecast_weather['list'][7]['main']['temp_max']])

    # get min temperature range over day 2
    d2_min_temp = min([forecast_weather['list'][8]['main']['temp_min'],
                       forecast_weather['list'][9]['main']['temp_min'],
                       forecast_weather['list'][10]['main']['temp_min'],
                       forecast_weather['list'][11]['main']['temp_min'],
                       forecast_weather['list'][12]['main']['temp_min'],
                       forecast_weather['list'][13]['main']['temp_min'],
                       forecast_weather['list'][14]['main']['temp_min'],
                       forecast_weather['list'][15]['main']['temp_min']])

    # get max temperature range over day 2
    d2_max_temp = max([forecast_weather['list'][8]['main']['temp_max'],
                       forecast_weather['list'][9]['main']['temp_max'],
                       forecast_weather['list'][10]['main']['temp_max'],
                       forecast_weather['list'][11]['main']['temp_max'],
                       forecast_weather['list'][12]['main']['temp_max'],
                       forecast_weather['list'][13]['main']['temp_max'],
                       forecast_weather['list'][14]['main']['temp_max'],
                       forecast_weather['list'][15]['main']['temp_max']])

    # generate response for board
    response = {"DOW":day0.weekday(),
                    "City":city,
                    "State":state,
                    "D0_Day":day_array[day0.weekday()],
                    "D0_Condition":weather_condition_map[current_weather['weather'][0]['icon']],
                    "D0_Humidity":int(round(current_weather['main']['humidity'])),
                    "D0_Temp_Hi":k2f(current_weather['main']['temp_max']),
                    "D0_Temp_Lo":k2f(current_weather['main']['temp_min']),
                    "D0_BG":weather_pixel_background_map[current_weather['weather'][0]['icon']],
                    "D0_Icon":weather_pixel_icon_map[current_weather['weather'][0]['icon']],
                    "D0_ANIME_1":weather_pixel_anime_map[current_weather['weather'][0]['icon']],
                    "D0_ANIME_2":weather_pixel_anime_map_2[current_weather['weather'][0]['icon']],
                    "D1_Day":day_array[day1.weekday()],
                    "D1_Condition":weather_condition_forecast_map[forecast_weather['list'][5]['weather'][0]['icon']],
                    "D1_Humidity":int(round(forecast_weather['list'][5]['main']['humidity'])),
                    "D1_Temp_Hi":k2f(d1_max_temp),
                    "D1_Temp_Lo":k2f(d1_min_temp),
                    "D1_BG":weather_pixel_forecast_background_map[forecast_weather['list'][5]['weather'][0]['icon']],
                    "D1_Icon":weather_pixel_forecast_icon_map[forecast_weather['list'][5]['weather'][0]['icon']],
                    "D1_ANIME_1":weather_pixel_forecast_anime_map[forecast_weather['list'][5]['weather'][0]['icon']],
                    "D1_ANIME_2":weather_pixel_forecast_anime_map_2[forecast_weather['list'][5]['weather'][0]['icon']],
                    "D2_Day":day_array[day2.weekday()],
                    "D2_Condition":weather_condition_forecast_map[forecast_weather['list'][13]['weather'][0]['icon']],
                    "D2_Humidity":int(round(forecast_weather['list'][13]['main']['humidity'])),
                    "D2_Temp_Hi":k2f(d2_max_temp),
                    "D2_Temp_Lo":k2f(d2_min_temp),
                    "D2_BG":weather_pixel_forecast_background_map[forecast_weather['list'][13]['weather'][0]['icon']],
                    "D2_Icon":weather_pixel_forecast_icon_map[forecast_weather['list'][13]['weather'][0]['icon']],
                    "D2_ANIME_1":weather_pixel_forecast_anime_map[forecast_weather['list'][13]['weather'][0]['icon']],
                    "D2_ANIME_2":weather_pixel_forecast_anime_map_2[forecast_weather['list'][13]['weather'][0]['icon']],
                    "Hour": "%02d" % (now_w_offset.hour),
                    "Minute": "%02d" % (now_w_offset.minute),
                    "IP_Address":lan_ip,
                   }

    log(response)

    # send response to the board
    MQTT.publish_event_to_client(IONode.get_input('in2')['event_data']['value'], json.dumps(response))

    # save response to stream
    IONode.set_output('out2', response)

except Exception:
    log("Failed to get IP lookup ")

    # default response if failed to get location or weather
    response = {"DOW":0,
            "City":"Unknown",
            "State":"Unknown",
            "D0_Day":"SAT",
            "D0_Condition":"Sunny",
            "D0_Humidity":72,
            "D0_Temp_Hi":84,
            "D0_Temp_Lo":73,
            "D0_BG":"GX_PIXELMAP_ID_BG_SUNNY",
            "D0_ANIME_1":"GX_PIXELMAP_ID_ANIME_SUN_SHINING",
            "D0_ANIME_2":"0",
            "D0_Icon":"GX_PIXELMAP_ID_ICON_SUNNY",
            "D1_Day":"SUN",
            "D1_Condition":"Partly Cloudy",
            "D1_Humidity":50,
            "D1_Temp_Hi":77,
            "D1_Temp_Lo":67,
            "D1_BG":"GX_PIXELMAP_ID_BG_PARTLYCLOUDY",
            "D1_Icon":"GX_PIXELMAP_ID_ICON_CLOUDY",
            "D1_ANIME_1":"GX_PIXELMAP_ID_ANIME_SUN_ONCLOUD",
            "D1_ANIME_2":"GX_PIXELMAP_ID_ANIME_CLOUD",
            "D2_Day":"MON",
            "D2_Condition":"Rain",
            "D2_Humidity":99,
            "D2_Temp_Hi":68,
            "D2_Temp_Lo":60,
            "D2_BG":"GX_PIXELMAP_ID_BG_RAINY",
            "D2_Icon":"GX_PIXELMAP_ID_ICON_RAINY",
            "D2_ANIME_1":"GX_PIXELMAP_ID_ANIME_RAINING_2",
            "D2_ANIME_2":"GX_PIXELMAP_ID_ANIME_RAINING_1",
            "Hour": "%02d" % (now_w_offset.hour),
            "Minute": "%02d" % (now_w_offset.minute),
            "IP_Address":lan_ip,
            }

    log(response)

    # send response to board
    MQTT.publish_event_to_client(IONode.get_input('in2')['event_data']['value'], json.dumps(response))


    # save response to stream
    IONode.set_output('out2', response)

# set temperature to 60
MQTT.publish_event_to_client(IONode.get_input('in2')['event_data']['value'], "60")
