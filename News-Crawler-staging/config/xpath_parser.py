
xpath_parser_dict = {
    "publisher_mapping": {
        "www.moneycontrol.com": "moneycontrol",
        "www.malayalamexpress.in":"Malayalam Express Online",
        "www.livemint.com": "Livemint",
        "www.latestly.com": "Latestly",
        "news.abplive.com": "ABP Live",
        "www.newsbytesapp.com": "NewsBytes",
        "indianexpress.com": "The Indian Express",
        "www.republicworld.com": "Republic world",
        "www.ndtv.com": "NDTV",
        "www.businessinsider.in": "Business Insider",
        "mintgenie.livemint.com": "Mintgenie",
        "www.wionews.com": "WION",
        "www.benzinga.com":"Benzinga",
        "theprint.in": "The Print",
        "www.financialexpress.com": "Financial Express",
        "www.thenewsminute.com": "The News Minute",
        "www.mid-day.com": "Mid-Day",
        "zeenews.india.com": "Zee News",
        "www.thequint.com": "The Quint",
        "tamil.news18.com": "News18 Tamil",
        "www.firstpost.com":"Firstpost",
        "telanganatoday.com": "Telangana Today",
        "www.crictracker.com": "CricTracker",
        "www.slurrp.com":"Slury",
        "www.thestatesman.com": "The Statesman",
        "www.freepressjournal.in": "The Free Press Journal",
        "www.hindustantimes.com": "Hindustan Times",
        "english.jagran.com": "Jagran English",
        "www.etvbharat.com":"ETV Bharat",
        "www.lokmattimes.com":"Lokmat Times",
        "www.cnbctv18.com":"CNBC TV18",
        "firstsportz.com":"First Sportz",
        "www.insidesport.in": "InsideSport",
        "newsable.asianetnews.com": "Asianet Newsable",
        "odishabytes.com": "Odisha Bytes",
        "www.chinimandi.com": "chinimandi",
        "www.onlymyhealth.com": "Only My Health",
        "glamsham.com": "Glamsham",
        "timesapplaud.com": "Times Applaud",
        "newsnext.live":"News Next",
        "www.newsvoir.com": "NewsVoir",
        "www.sportstiger.com": "Sports Tiger",
        "www.thetelugufilmnagar.com": "Telugu Filmnagar English",
        "agritimes.co.in": "AgriTimes",
        "firstcuriosity.com": "First Curiosity",
        "www.headlinesoftoday.com": "Headlines of Today",
        "www.pinkvilla.com": "Pinkvilla",
        "www.ottplay.com": "OTTplay",
        "www.prameyanews.com": "Prameya News",
        "telugu.filmibeat.com": "FilmiBeat",
        "www.dnaindia.com": "DNA",
        "www.news18.com": "News18",
        "www.udayavani.com": "Udayavani English",
        "www.bqprime.com": "BQ Prime",
        "www.cricketnmore.com": "Cricketnmore",
        "suryaa.com": "Suryaa News English",
        "www.amarujala.com": "Amar Ujala",
        "hindi.news18.com": "News18 Hindi",
        "www.tv9hindi.com": "TV9 Hindi",
        "www.prabhatkhabar.com": "Prabhat Khabar",
        "www.naidunia.com": "Naidunia",
        "www.punjabkesari.in": "Punjab Kesari",
        "hindi.latestly.com": "Latestly Hindi",
        "www.livehindustan.com": "Hindustan",
        "aninews.in": "ANI",
        "sportsdigest.in": "Sports Digest",
        "www.businesstoday.in": "Business Today",
        "crictoday.com": "Crictoday",
        "nenow.in": "Northeast Now English",
        "www.goodreturns.in": "Good Returns",
        "www.bollywoodshaadis.com": "Bollywood Shaadis",
        "www.shortpedia.com": "Shortpedia",
        "english.loktej.com": "Loktej English",
        "www.india.com": "India.com",
        "www.tvj.co.in": "TVJ",
        "www.startupstories.in": "Startup Stories",
        "himachalabhiabhi.com": "Himachal Abhi Abhi",
        "www.hellomumbainews.com": "Hello Mumbai",
        "english.nilkantho.in": "Nilkantho English",
        "www.epainassist.com": "ePainAssist",
        "www.nyoooz.com": "NYOOOZ",
        "www.chhavitarot.com": "Chhavi Tarot",
        "www.vishvasnews.com": "Vishvas News Hindi",
        "www.abplive.com": "ABP News",
        "www.patrika.com": "Patrika",
        "www.newsnationtv.com": "News Nation",
        "ndtv.in": "NDTV India",
        "www.jagran.com": "Dainik Jagran",
        "www.poorvanchalmedia.com": "Poorvanchal Media",
        "hindi.dynamitenews.com": "Dynamite News Hindi",
        "hindi.moneycontrol.com": "moneycontrol Hindi",
        "hindi.asianetnews.com": "Asianet News Hindi",
        "www.divyahimachal.com": "Divya Himachal",
        "hindi.newsbytesapp.com": "NewsBytes Hindi",
        "hindi.theprint.in": "The Print Hindi",
        "24ghanteonline.com": "24 Ghante Online",
        "www.sabkuchgyan.com": "Sabkuch Gyan",
        "localvocalindia.com": "Local Vocal India",
        "www.samacharjagat.com": "Samachar Jagat",
        "hindi.thequint.com": "The Quint Hindi",
        "hindi.cricketnmore.com": "Cricketnmore Hindi",
        "hindi.filmibeat.com": "FilmiBeat Hindi",
        "www.lokmatnews.in": "Lokmat Samachar",
        "bharat.republicworld.com": "Republic Bharat",
        "hindi.crictracker.com": "CricTracker Hindi",
        "www.herzindagi.com": "Her Zindagi Hindi",
        "telugu.suryaa.com": "Suryaa News",
        "telugu.news18.com": "News18 Telugu",
        "tv9telugu.com": "TV9 Telugu",
        "telugu.abplive.com": "ABP Desam",
        "telugu.asianetnews.com": "Asianet News Telugu",
        "ntvtelugu.com": "NTV",
        "www.v6velugu.com": "V6 Velugu",
        "telugu.hindustantimes.com": "HT Telugu",
        "oktelugu.com": "OK Telugu",
        "www.esakal.com": "Sakal",
        "www.saamtv.com": "Saam Tv",
        "www.tv9marathi.com": "TV9 Marathi",
        "lokmat.news18.com": "News18 Lokmat",
        "marathi.abplive.com": "ABP Majha",
        "www.dainikgomantak.com": "Dainik Gomantak",
        "www.dainikprabhat.com": "Dainik Prabhat",
        "www.sarkarnama.in": "Sarkarnama",
        "marathi.hindustantimes.com": "HT Marathi",
        "www.navarashtra.com": "Navarashtra",
        "www.asianetnews.com": "Asianet News Malayalam",
        "malayalam.news18.com": "News18 Malayalam"
    },
    "publisher_entites": {
        "moneycontrol":[
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Malayalam Express Online":[
            "Headline",
            "Article_Body",
            "Date_Published"
        ],
        "Livemint": [
            "Headline",
            "Article_Body"
        ],
        "Latestly": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ABP Live": [
            "Headline",
            "Article_Body",
            "Author"
        ],
        "NewsBytes": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Indian Express": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Republic world": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "NDTV": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Business Insider": [
            "Headline",
            "Article_Body"
        ],
        "Mintgenie": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "WION": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Benzinga": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Print": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Financial Express": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The News Minute": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Mid-Day": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Zee News": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Quint": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News18 Tamil": [
            "Headline",
            "Article_Body",
             "Author",
            "Date_Published"
        ],
        "Firstpost": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Telangana Today": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "CricTracker": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Slury": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Statesman": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Free Press Journal": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Hindustan Times": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Jagran English": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ETV Bharat": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Lokmat Times": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "CNBC TV18": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "First Sportz": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "InsideSport": [
            "Headline",
            "Article_Body",
            "Author"
        ],
        "Asianet Newsable": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Odisha Bytes": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "chinimandi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Only My Health": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Glamsham": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Times Applaud": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News Next": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "NewsVoir": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Sports Tiger": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Telugu Filmnagar English": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "AgriTimes": [
            "Headline",
            "Article_Body"
        ],
        "First Curiosity": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Headlines of Today":[
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Pinkvilla": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "OTTplay": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Prameya News": [
            "Headline",
            "Article_Body",
            "Date_Published"
        ],
        "FilmiBeat": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "DNA": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News18": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Udayavani English": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "BQ Prime": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Cricketnmore": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Suryaa News English": [
            "Headline",
            "Article_Body"
        ],
        "Amar Ujala": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News18 Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "TV9 Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Prabhat Khabar": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Naidunia": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Punjab Kesari": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Latestly Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Hindustan": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ANI": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Sports Digest": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Business Today": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Crictoday": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Northeast Now English": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Bollywood Shaadis": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Shortpedia": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Loktej English": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "India.com": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "TVJ": [
            "Headline",
            "Article_Body",
            "Date_Published"
        ],
        "Startup Stories": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Himachal Abhi Abhi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Hello Mumbai": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Nilkantho English": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ePainAssist": [
            "Headline",
            "Article_Body",
            "Author"
        ],
        "NYOOOZ": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Chhavi Tarot": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Vishvas News Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ABP News": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Patrika": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News Nation": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "NDTV India": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Dainik Jagran": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Poorvanchal Media": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Dynamite News Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "moneycontrol Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Asianet News Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Divya Himachal": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "NewsBytes Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Print Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "24 Ghante Online": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Sabkuch Gyan": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Local Vocal India": [
            "Headline",
            "Article_Body",
            "Date_Published"
        ],
        "Samachar Jagat": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "The Quint Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Cricketnmore Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "FilmiBeat Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Lokmat Samachar": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Republic Bharat": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "CricTracker Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Her Zindagi Hindi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Suryaa News": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News18 Telugu": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "TV9 Telugu": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ABP Desam": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Asianet News Telugu": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "NTV": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "V6 Velugu": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "HT Telugu": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "OK Telugu": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Sakal": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Saam Tv": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "TV9 Marathi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News18 Lokmat": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "ABP Majha": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Dainik Gomantak": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Dainik Prabhat": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Sarkarnama": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "HT Marathi": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Navarashtra": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "Asianet News Malayalam": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ],
        "News18 Malayalam": [
            "Headline",
            "Article_Body",
            "Author",
            "Date_Published"
        ]
    }
}