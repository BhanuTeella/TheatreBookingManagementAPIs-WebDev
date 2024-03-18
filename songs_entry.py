import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('db_directory/music_streaming_app.db')
c = conn.cursor()

with open('sample_audio.mp3', 'rb') as file:
    song_file = file.read()


date_list=['2003-08-11', '2002-01-18', '2012-02-29', '2006-07-26', '2017-04-13', '2001-11-02', '2014-06-06', '2016-09-15', '2008-09-19', '2021-07-28', '2002-04-24', '2019-02-23', '2006-01-11', '2004-04-05', '2018-05-24', '2001-09-17', '2003-04-19', '2008-05-05', '2017-10-02', '2013-03-30', '2012-03-06', '2009-05-20', '2014-09-14', '2010-02-09', '2015-10-08', '2011-08-07', '2005-06-09', '2019-04-03', '2007-11-16', '2004-12-11', '2022-07-15', '2018-01-28', '2008-06-13', '2013-01-30', '2016-11-16', '2001-04-29', '2009-07-18', '2003-12-31', '2010-09-10', '2005-12-13', '2011-12-23', '2015-03-01', '2017-11-25', '2002-09-03', '2012-09-24', '2019-11-12', '2006-06-21', '2004-11-02', '2001-06-14', '2018-12-09', '2007-05-17', '2014-04-14', '2013-09-28', '2016-02-26', '2011-05-19', '2009-10-15', '2010-07-08', '2005-02-21', '2002-11-27', '2008-02-14', '2013-07-23', '2014-12-04', '2016-05-30', '2004-08-12', '2015-01-17', '2017-01-12', '2001-08-18', '2019-07-06', '2018-09-30', '2010-12-22', '2003-02-20', '2012-06-08', '2007-09-05', '2006-11-19', '2011-02-10', '2014-08-02', '2005-09-26', '2001-01-26', '2013-12-15', '2009-01-25', '2015-05-10', '2016-07-08', '2008-12-16', '2002-06-26', '2017-08-21', '2004-01-05', '2018-02-19', '2010-04-27', '2019-08-31', '2007-02-05', '2011-04-02', '2016-03-19', '2003-07-31', '2006-03-14',
           '2003-08-11', '2002-01-18', '2012-02-29', '2006-07-26', '2017-04-13', '2001-11-02', '2014-06-06', '2016-09-15', '2008-09-19', '2021-07-28', '2002-04-24', '2019-02-23', '2006-01-11', '2004-04-05', '2018-05-24', '2001-09-17', '2003-04-19', '2008-05-05', '2017-10-02', '2013-03-30', '2012-03-06', '2009-05-20', '2014-09-14', '2010-02-09', '2015-10-08', '2011-08-07', '2005-06-09', '2019-04-03', '2007-11-16', '2004-12-11', '2022-07-15', '2018-01-28', '2008-06-13', '2013-01-30', '2016-11-16', '2001-04-29', '2009-07-18', '2003-12-31', '2010-09-10', '2005-12-13', '2011-12-23', '2015-03-01', '2017-11-25', '2002-09-03', '2012-09-24', '2019-11-12', '2006-06-21', '2004-11-02', '2001-06-14', '2018-12-09', '2007-05-17', '2014-04-14', '2013-09-28', '2016-02-26', '2011-05-19', '2009-10-15', '2010-07-08', '2005-02-21', '2002-11-27', '2008-02-14', '2013-07-23', '2014-12-04', '2016-05-30', '2004-08-12', '2015-01-17', '2017-01-12', '2001-08-18', '2019-07-06', '2018-09-30', '2010-12-22', '2003-02-20', '2012-06-08', '2007-09-05', '2006-11-19', '2011-02-10', '2014-08-02', '2005-09-26', '2001-01-26', '2013-12-15', '2009-01-25', '2015-05-10', '2016-07-08', '2008-12-16', '2002-06-26', '2017-08-21', '2004-01-05', '2018-02-19', '2010-04-27', '2019-08-31', '2007-02-05', '2011-04-02', '2016-03-19', '2003-07-31', '2006-03-14']

creators=[2,5]

# Sample data in JSON format
    
lyrics = '''Teri Meri Gallan Ho Gayi Mashhoor
Kar Na Kabhi Tu Mujhe Nazron Se Door'''

json_data =''' [
    {
        "song_id": 1,
        "name": "Tum Hi Ho",
        "lyrics": "Hum tere bin ab reh nahi sakte\\n  Hum tere bin ab reh nahi sakte",
        "genre": "Dance Numbers",
        "duration": 240,
        "date_created": "2022-01-01T00:00:00Z",
        "creator_id": 1
    },
    {
        "song_id": 2,
        "name": "Dil Se Re",
        "lyrics": "Dil se re, dil se re\\n Dil se re, dil se re",
        "genre": "Romantic Songs",
        "duration": 300,
        "date_created": "2022-01-02T00:00:00Z",
        "creator_id": 23
    },
    {
        "song_id": 3,
        "name": "Roobaroo",
        "lyrics": "Roobaroo roshni\\n Roobaroo roshni",
        "genre": "Pop",
        "duration": 210,
        "date_created": "2022-01-03T00:00:00Z",
        "creator_id": 12
    },
    {
        "song_id": 4,
        "name": "Chaiyya Chaiyya",
        "lyrics": "Chaiyya chaiyya chaiyya chaiyya\\n Arey Chaiyya chaiyya chaiyya chaiyya",
        "genre": "Dance Numbers",
        "duration": 250,
        "date_created": "2022-01-04T00:00:00Z",
        "creator_id": 7
    },
    {
        "song_id": 5,
        "name": "Kal Ho Naa Ho",
        "lyrics": "Har ghadi badal rahi hai roop zindagi\\n ",
        "genre": "Romantic Songs",
        "duration": 320,
        "date_created": "2022-01-05T00:00:00Z",
        "creator_id": 15
    },
    {
        "song_id": 6,
        "name": "Jai Ho",
        "lyrics": "Jai ho, jai ho, jai ho, jai ho\\n ",
        "genre": "Pop",
        "duration": 220,
        "date_created": "2022-01-06T00:00:00Z",
        "creator_id": 9
    },
    {
        "song_id": 7,
        "name": "Dhoom Machale",
        "lyrics": "Dhoom machale, dhoom machale dhoom\\n dhoom  dhoom",
        "genre": "Dance Numbers",
        "duration": 230,
        "date_created": "2022-01-07T00:00:00Z",
        "creator_id": 18
    },
    {
        "song_id": 8,
        "name": "Tum Se Hi",
        "lyrics": "Tum se hi din hota hai\\n Tum se hi din hota hai",
        "genre": "Romantic Songs",
        "duration": 310,
        "date_created": "2022-01-08T00:00:00Z",
        "creator_id": 4
    },
    {
        "song_id": 9,
        "name": "Badtameez Dil",
        "lyrics": "Badtameez dil, badtameez dil, badtameez dil\\n badtameez dil, badtameez dil",
        "genre": "Pop",
        "duration": 200,
        "date_created": "2022-01-09T00:00:00Z",
        "creator_id": 20
    },
    {
        "song_id": 10,
        "name": "Munni Badnaam Hui",
        "lyrics": "Munni badnaam hui darling tere liye\\n Munni badnaam hui darling tere liye",
        "genre": "Dance Numbers",
        "duration": 260,
        "date_created": "2022-01-10T00:00:00Z",
        "creator_id": 11
    },

    {
        "song_id": 11,
        "name": "Rock On",
        "lyrics": "Dil kya kehta hai mera,\\n  kya main bataun",
        "genre": "Rock",
        "duration": 250,
        "date_created": "2022-01-11T00:00:00Z",
        "creator_id": 5
    },
    {
        "song_id": 12,
        "name": "Tum Itna Jo Muskura Rahe Ho",
        "lyrics": "Tum itna jo muskura rahe ho,\\n  kya gham hai jisko chhupa rahe ho",
        "genre": "Classical",
        "duration": 300,
        "date_created": "2022-01-12T00:00:00Z",
        "creator_id": 6
    },
    {
        "song_id": 13,
        "name": "Dum Maro Dum",
        "lyrics": "Dum maro dum, mit jaaye gham\\n Dum maro dum, mit jaaye gham",
        "genre": "Folk",
        "duration": 210,
        "date_created": "2022-01-13T00:00:00Z",
        "creator_id": 7
    },
    {
        "song_id": 14,
        "name": "Blue Eyes",
        "lyrics": "Blue eyes, hypnotise teri kardi ai mennu\\n Blue eyes, hypnotise teri kardi ai mennu",
        "genre": "Rap",
        "duration": 220,
        "date_created": "2022-01-14T00:00:00Z",
        "creator_id": 8
    },
    {
        "song_id": 15,
        "name": "Sadda Haq",
        "lyrics": "Sadda haq, aithe rakh\\n ",
        "genre": "Rock",
        "duration": 230,
        "date_created": "2022-01-15T00:00:00Z",
        "creator_id": 9
    },
    {
        "song_id": 16,
        "name": "Lag Ja Gale",
        "lyrics": "Lag ja gale ki phir ye haseen raat ho na ho\\n ",
        "genre": "Classical",
        "duration": 240,
        "date_created": "2022-01-16T00:00:00Z",
        "creator_id": 10
    },
    {
        "song_id": 17,
        "name": "Morni Banke",
        "lyrics": "Morni banke, morni banke\\n ",
        "genre": "Folk",
        "duration": 250,
        "date_created": "2022-01-17T00:00:00Z",
        "creator_id": 11
    },
    {
        "song_id": 18,
        "name": "Swag Mera Desi",
        "lyrics": "Swag mera desi,\\n  swag swag mera desi\\n ",
        "genre": "Rap",
        "duration": 260,
        "date_created": "2022-01-18T00:00:00Z",
        "creator_id": 12
    },
    {
        "song_id": 19,
        "name": "Socha Hai",
        "lyrics": "Socha hai yeh ke\\n  tumhe rasta bhulaye\\n ",
        "genre": "Rock",
        "duration": 270,
        "date_created": "2022-01-19T00:00:00Z",
        "creator_id": 13
    },
    {
        "song_id": 20,
        "name": "Piya Tose Naina Laage Re",
        "lyrics": "Piya tose naina laage re,\\n  naina laage re\\n ",
        "genre": "Classical",
        "duration": 280,
        "date_created": "2022-01-20T00:00:00Z",
        "creator_id": 14
    },
    {
        "song_id": 21,
        "name": "Bulla Ki Jaana",
        "lyrics": "Bulla ki jaana main kaun\\n  Bulla ki jaana main kaun\\n  Bulla ki jaana main kaun\\n ",
        "genre": "Sufi",
        "duration": 300,
        "date_created": "2022-01-21T00:00:00Z",
        "creator_id": 15
    },
    {
        "song_id": 22,
        "name": "Maa Tujhe Salaam",
        "lyrics": "Maa tujhe salaam\\n  Maa tujhe salaam\\n  Vande maataram, vande maataram\\n ",
        "genre": "Patriotic",
        "duration": 310,
        "date_created": "2022-01-22T00:00:00Z",
        "creator_id": 16
    },
    {
        "song_id": 23,
        "name": "Kun Faya Kun",
        "lyrics": "Kun faya kun\\n  Kun faya kun\\n  Faya kun, faya kun, faya kun\\n ",
        "genre": "Sufi",
        "duration": 320,
        "date_created": "2022-01-23T00:00:00Z",
        "creator_id": 17
    },
    {
        "song_id": 24,
        "name": "Ae Watan",
        "lyrics": "Ae watan, watan mere,\\n  abaad rahe tu\\n  Ae watan, watan mere, abaad rahe tu\\n ",
        "genre": "Patriotic",
        "duration": 330,
        "date_created": "2022-01-24T00:00:00Z",
        "creator_id": 18
    },
    {
        "song_id": 25,
        "name": "Piya Haji Ali",
        "lyrics": "Piya Haji Ali\\n  Piya Haji Ali\\n  Piya Haji Ali, piya ho\\n  Piya Haji Ali, piya ho\\n ",
        "genre": "Sufi",
        "duration": 340,
        "date_created": "2022-01-25T00:00:00Z",
        "creator_id": 19
    },
    {
        "song_id": 26,
        "name": "Teri Mitti",
        "lyrics": "Teri mitti mein mil jaawaan\\n  Gul banke main khil jaawaan\\n  Teri mitti mein mil jaawaan\\n ",
        "genre": "Patriotic",
        "duration": 350,
        "date_created": "2022-01-26T00:00:00Z",
        "creator_id": 20
    },
    {
        "song_id": 27,
        "name": "Arziyan",
        "lyrics": "Arziyan saari main\\n  Chehre pe likh ke laaya hoon\\n  Arziyan saari main\\n  Chehre pe likh ke laaya hoon\\n ",
        "genre": "Sufi",
        "duration": 360,
        "date_created": "2022-01-27T00:00:00Z",
        "creator_id": 21
    },
    {
        "song_id": 28,
        "name": "Rang De Basanti",
        "lyrics": "Rang de basanti\\n  Rang de basanti\\n  Rang de basanti, rang de, rang de\\n ",
        "genre": "Patriotic",
        "duration": 370,
        "date_created": "2022-01-28T00:00:00Z",
        "creator_id": 22
    },
    {
        "song_id": 29,
        "name": "Mann Ki Lagan",
        "lyrics": "Mann ki lagan\\n  Mann ki lagan\\n  Mann ki lagan, mann ki lagan, mann ki lagan\\n ",
        "genre": "Sufi",
        "duration": 380,
        "date_created": "2022-01-29T00:00:00Z",
        "creator_id": 23
    },
    {
        "song_id": 30,
        "name": "Aisa Des Hai Mera",
        "lyrics": "Aisa des hai mera\\n  Aisa des hai mera\\n  Aisa des hai mera, aisa des hai mera\\n ",
        "genre": "Patriotic",
        "duration": 390,
        "date_created": "2022-01-30T00:00:00Z",
        "creator_id": 24
    },
    {
        "song_id": 31,
        "name": "Tere Bina",
        "lyrics": "Tere bina beswaadi\\n  Tere bina beswaadi ratiyaan, oh sajna\\n  Tere bina beswaadi ratiyaan\\n ",
        "genre": "Sufi",
        "duration": 400,
        "date_created": "2022-01-31T00:00:00Z",
        "creator_id": 25
    },
    {
        "song_id": 32,
        "name": "Chak De India",
        "lyrics": "Chak de India\\n  Chak de India\\n  Chak de India, chak de, chak de",
        "genre": "Patriotic",
        "duration": 390,
        "date_created": "2022-01-30T00:00:00Z",
        "creator_id": 24
    },
    {
        "song_id": 33,
        "name": "Tum Hi Ho",
        "lyrics": "Hum tere bin ab reh nahi sakte,\\n  Tere bina kya wajood mera\\n ",
        "genre": "Romantic",
        "duration": 260,
        "date_created": "2022-02-01T00:00:00Z",
        "creator_id": 1
    },
    {
        "song_id": 34,
        "name": "Dil Se Re",
        "lyrics": "Dil se re, dil se re\\n  Dooba dooba rehta hoon aankhon me teri\\n ",
        "genre": "Romantic",
        "duration": 270,
        "date_created": "2022-02-02T00:00:00Z",
        "creator_id": 2
    },
    {
        "song_id": 35,
        "name": "Pee Loon",
        "lyrics": "Pee loon tere neelay neelay nainon se shabnam,\\n  Pee loon tere geelay geelay hoto ki sargam\\n ",
        "genre": "Romantic",
        "duration": 280,
        "date_created": "2022-02-03T00:00:00Z",
        "creator_id": 3
    },
    {
        "song_id": 36,
        "name": "Tum Se Hi",
        "lyrics": "Tum se hi din hota hai, \\n Surmayi shaam aati hai,\\n  Tum se hi, tum se hi\\n ",
        "genre": "Romantic",
        "duration": 290,
        "date_created": "2022-02-04T00:00:00Z",
        "creator_id": 4
    },
    {
        "song_id": 37,
        "name": "Tera Ban Jaunga",
        "lyrics": "Meri rahe tere tak hai,\\n  Tujhpe hi toh mera haq hai,\\n  Ishq mera tu beshaq hai\\n ",
        "genre": "Romantic",
        "duration": 300,
        "date_created": "2022-02-05T00:00:00Z",
        "creator_id": 5
    },
    {
        "song_id": 38,
        "name": "Tum Mile",
        "lyrics": "Tum mile, toh lamhein tham gaye, \\n Tum mile, toh saare gum gaye\\n ",
        "genre": "Romantic",
        "duration": 310,
        "date_created": "2022-02-06T00:00:00Z",
        "creator_id": 6
    },
    {
        "song_id": 39,
        "name": "Tera Ban Jaunga",
        "lyrics": "Meri rahe tere tak hai, \\n Tujhpe hi toh mera haq hai,\\n  Ishq mera tu beshaq hai\\n ",
        "genre": "Romantic",
        "duration": 320,
        "date_created": "2022-02-07T00:00:00Z",
        "creator_id": 7
    },
    {
        "song_id": 40,
        "name": "Tum Ho",
        "lyrics": "Tum ho paas mere, \\n Saath mere ho tum yun, \\n Jitna mehsus karoon tumko,\\n  Utna hi paa bhi loon\\n ",
        "genre": "Romantic",
        "duration": 330,
        "date_created": "2022-02-08T00:00:00Z",
        "creator_id": 8
    },
    {
        "song_id": 41,
        "name": "Tera Ban Jaunga",
        "lyrics": "Meri rahe tere tak hai,\\n  Tujhpe hi toh mera haq hai, \\n Ishq mera tu beshaq hai\\n ",
        "genre": "Romantic",
        "duration": 340,
        "date_created": "2022-02-09T00:00:00Z",
        "creator_id": 9
    },
    {
        "song_id": 42,
        "name": "Tum Hi Aana",
        "lyrics": "Tum hi aana, Marjaavaan\\n  Tum hi aana, Marjaavaan\\n ",
        "genre": "Romantic",
        "duration": 350,
        "date_created": "2022-02-10T00:00:00Z",
        "creator_id": 10
    },
    {
        "song_id": 43,
        "name": "Agar Tum Saath Ho",
        "lyrics": "Agar tum saath ho\\n  Agar tum saath ho\\n ",
        "genre": "Romantic",
        "duration": 360,
        "date_created": "2022-02-11T00:00:00Z",
        "creator_id": 11
    },
    {
        "song_id": 44,
        "name": "Tum Hi Ho",
        "lyrics": "Tum hi ho\\n  Tum hi ho\\n  Tere liye hi jiya main\\n ",
        "genre": "Romantic",
        "duration": 370,
        "date_created": "2022-02-12T00:00:00Z",
        "creator_id": 12
    },
    {
        "song_id": 45,
        "name": "Channa Mereya",
        "lyrics": "Channa mereya mereya\\n  Channa mereya mereya beliya\\n ",
        "genre": "Romantic",
        "duration": 380,
        "date_created": "2022-02-13T00:00:00Z",
        "creator_id": 13
    },
    {
        "song_id": 46,
        "name": "Tera Ban Jaunga",
        "lyrics": "Tera ban jaunga\\n  Tera ban jaunga\\n ",
        "genre": "Romantic",
        "duration": 390,
        "date_created": "2022-02-14T00:00:00Z",
        "creator_id": 14
    },
    {
        "song_id": 47,
        "name": "Tum Se Hi",
        "lyrics": "Tum se hi din hota hai\\n  Tum se hi din hota hai\\n ",
        "genre": "Romantic",
        "duration": 400,
        "date_created": "2022-02-15T00:00:00Z",
        "creator_id": 15
    },
    {
        "song_id": 48,
        "name": "Tum Mile",
        "lyrics": "Tum mile, toh lamhein tham gaye\\n  Tum mile, toh saare gum gaye\\n ",
        "genre": "Romantic",
        "duration": 410,
        "date_created": "2022-02-16T00:00:00Z",
        "creator_id": 16
    },
    {
        "song_id": 49,
        "name": "Tera Ban Jaunga",
        "lyrics": "Tera ban jaunga\\n  Tera ban jaunga\\n ",
        "genre": "Romantic",
        "duration": 420,
        "date_created": "2022-02-17T00:00:00Z",
        "creator_id": 17
    },
    {
        "song_id": 50,
        "name": "Tum Ho",
        "lyrics": "Tum ho paas mere\\n  Tum ho paas mere\\n ",
        "genre": "Romantic",
        "duration": 430,
        "date_created": "2022-02-18T00:00:00Z",
        "creator_id": 18
    },
    {
        "song_id": 51,
        "name": "Tera Ban Jaunga",
        "lyrics": "Tera ban jaunga\\n  Tera ban jaunga\\n ",
        "genre": "Romantic",
        "duration": 440,
        "date_created": "2022-02-19T00:00:00Z",
        "creator_id": 19
    },
    {
        "song_id": 52,
        "name": "Tum Hi Aana",
        "lyrics": "Tum hi aana\\n  Tum hi aana\\n ",
        "genre": "Romantic",
        "duration": 450,
        "date_created": "2022-02-20T00:00:00Z",
        "creator_id": 20
    },
    {
        "song_id": 53,
        "name": "Mere Bina",
        "lyrics": "Mere bina main, rehne laga hoon\\n  Teri hawaon me, behne laga hoon\\n ",
        "genre": "Romantic",
        "duration": 460,
        "date_created": "2022-02-21T00:00:00Z",
        "creator_id": 21
    },
    {
        "song_id": 54,
        "name": "Tum Jo Aaye",
        "lyrics": "Tum jo aaye, zindagi me baat ban gayi\\n  Ishq mazhab, ishq meri zaat ban gayi\\n ",
        "genre": "Romantic",
        "duration": 470,
        "date_created": "2022-02-22T00:00:00Z",
        "creator_id": 22
    },
    {
        "song_id": 55,
        "name": "Tera Ban Jaunga",
        "lyrics": "Tera ban jaunga\\n  Tera ban jaunga\\n ",
        "genre": "Romantic",
        "duration": 480,
        "date_created": "2022-02-23T00:00:00Z",
        "creator_id": 23
    },
    {
        "song_id": 56,
        "name": "Tum Se Hi",
        "lyrics": "Tum se hi din hota hai\\n  Tum se hi din hota hai\\n ",
        "genre": "Romantic",
        "duration": 490,
        "date_created": "2022-02-24T00:00:00Z",
        "creator_id": 24
    },
    {
        "song_id": 57,
        "name": "Tum Mile",
        "lyrics": "Tum mile, toh lamhein tham gaye\\n  Tum mile, toh saare gum gaye\\n ",
        "genre": "Romantic",
        "duration": 500,
        "date_created": "2022-02-25T00:00:00Z",
        "creator_id": 25
    },
    {
        "song_id": 58,
        "name": "Tera Ban Jaunga",
        "lyrics": "Tera ban jaunga\\n  Tera ban jaunga\\n ",
        "genre": "Romantic",
        "duration": 510,
        "date_created": "2022-02-26T00:00:00Z",
        "creator_id": 26
    },
    {
        "song_id": 59,
        "name": "Tum Ho",
        "lyrics": "Tum ho paas mere\\n  Tum ho paas mere\\n ",
        "genre": "Romantic",
        "duration": 520,
        "date_created": "2022-02-27T00:00:00Z",
        "creator_id": 27
    },
    {
        "song_id": 60,
        "name": "Tera Ban Jaunga",
        "lyrics": "Tera ban jaunga\\n  Tera ban jaunga\\n ",
        "genre": "Romantic",
        "duration": 530,
        "date_created": "2022-02-28T00:00:00Z",
        "creator_id": 28
    },
    {
        "song_id": 61,
        "name": "Tum Hi Aana",
        "lyrics": "Tum hi aana\\n  Tum hi aana\\n ",
        "genre": "Romantic",
        "duration": 540,
        "date_created": "2022-03-01T00:00:00Z",
        "creator_id": 29
    },
    {
        "song_id": 62,
        "name": "Agar Tum Saath Ho",
        "lyrics": "Agar tum saath ho\\n  Agar tum saath ho\\n ",
        "genre": "Romantic",
        "duration": 550,
        "date_created": "2022-03-02T00:00:00Z",
        "creator_id": 30
    },
    {
        "song_id": 63,
        "name": "Jai Ho",
        "lyrics": "Jai ho, jai ho,\\n  aaja, aaja jind shamiyane ke tale\\n ",
        "genre": "Pop",
        "duration": 260,
        "date_created": "2022-03-03T00:00:00Z",
        "creator_id": 31
    },
    {
        "song_id": 64,
        "name": "Rock On",
        "lyrics": "Dil kya kehta hai mera,\\n  kya main bataun\\n ",
        "genre": "Rock",
        "duration": 270,
        "date_created": "2022-03-04T00:00:00Z",
        "creator_id": 32
    },
    {
        "song_id": 65,
        "name": "Dum Maro Dum",
        "lyrics": "Dum maro dum, mit jaaye gham,\\n  bolo subah shaam, Hare Krishna Hare Ram\\n ",
        "genre": "Folk",
        "duration": 280,
        "date_created": "2022-03-05T00:00:00Z",
        "creator_id": 33
    },
    {
        "song_id": 66,
        "name": "Blue Eyes",
        "lyrics": "Blue eyes, hypnotise teri kardi a mennu\\n ",
        "genre": "Rap",
        "duration": 290,
        "date_created": "2022-03-06T00:00:00Z",
        "creator_id": 34
    },
    {
        "song_id": 67,
        "name": "Chak De India",
        "lyrics": "Kuchh kariye, kuchh kariye, \\n nas nas meri khole\\n ",
        "genre": "Pop",
        "duration": 300,
        "date_created": "2022-03-07T00:00:00Z",
        "creator_id": 35
    },
    {
        "song_id": 68,
        "name": "Sadda Haq",
        "lyrics": "Sadda haq, aithe rakh, \\n sadda haq, aithe rakh\\n ",
        "genre": "Rock",
        "duration": 310,
        "date_created": "2022-03-08T00:00:00Z",
        "creator_id": 36
    },
    {
        "song_id": 69,
        "name": "Mast Qalandar",
        "lyrics": "Dama dam mast qalandar, ali dam dam de andar\\n ",
        "genre": "Folk",
        "duration": 320,
        "date_created": "2022-03-09T00:00:00Z",
        "creator_id": 37
    },
    {
        "song_id": 70,
        "name": "Swag Mera Desi",
        "lyrics": "Swag mera desi,\\n  swag swag mera desi hai\\n ",
        "genre": "Rap",
        "duration": 330,
        "date_created": "2022-03-10T00:00:00Z",
        "creator_id": 38
    },
    {
        "song_id": 71,
        "name": "Badtameez Dil",
        "lyrics": "Badtameez dil, badtameez dil, \\n badtameez dil, mane na\\n ",
        "genre": "Pop",
        "duration": 340,
        "date_created": "2022-03-11T00:00:00Z",
        "creator_id": 39
    },
    {
        "song_id": 72,
        "name": "Socha Hai",
        "lyrics": "Kya tumne kabhi kisi se pyaar kiya, \\n kya tumne kabhi kisi ko dil diya\\n ",
        "genre": "Rock",
        "duration": 350,
        "date_created": "2022-03-12T00:00:00Z",
        "creator_id": 40
    },
    {
        "song_id": 73,
        "name": "Lose Yourself",
        "lyrics": "You better lose yourself in the music,\\n  the moment\\n ",
        "genre": "Rap",
        "duration": 360,
        "date_created": "2022-03-13T00:00:00Z",
        "creator_id": 41
    },
    {
        "song_id": 74,
        "name": "Bohemian Rhapsody",
        "lyrics": "Is this the real life?\\n  Is this just fantasy?\\n ",
        "genre": "Rock",
        "duration": 370,
        "date_created": "2022-03-14T00:00:00Z",
        "creator_id": 42
    },
    {
        "song_id": 75,
        "name": "Viva la Vida",
        "lyrics": "I used to rule the world, \\n Seas would rise when I gave the word\\n ",
        "genre": "Pop",
        "duration": 380,
        "date_created": "2022-03-15T00:00:00Z",
        "creator_id": 43
    },
    {
        "song_id": 76,
        "name": "Hotel California",
        "lyrics": "On a dark desert highway, cool wind in my hair\\n ",
        "genre": "Rock",
        "duration": 390,
        "date_created": "2022-03-16T00:00:00Z",
        "creator_id": 44
    },
    {
        "song_id": 77,
        "name": "Smells Like Teen Spirit",
        "lyrics": "Load up on guns, bring your friends\\n ",
        "genre": "Rock",
        "duration": 400,
        "date_created": "2022-03-17T00:00:00Z",
        "creator_id": 45
    },
    {
        "song_id": 78,
        "name": "Imagine",
        "lyrics": "Imagine there's no heaven,\\n  It's easy if you try\\n ",
        "genre": "Pop",
        "duration": 410,
        "date_created": "2022-03-18T00:00:00Z",
        "creator_id": 46
    },
    {
        "song_id": 79,
        "name": "One",
        "lyrics": "Is it getting better,\\n  Or do you feel the same\\n ",
        "genre": "Rock",
        "duration": 420,
        "date_created": "2022-03-19T00:00:00Z",
        "creator_id": 47
    },
    {
        "song_id": 80,
        "name": "Billie Jean",
        "lyrics": "She was more like a beauty queen from a movie scene\\n ",
        "genre": "Pop",
        "duration": 430,
        "date_created": "2022-03-20T00:00:00Z",
        "creator_id": 48
    },
    {
        "song_id": 81,
        "name": "Hey Jude",
        "lyrics": "Hey Jude, don't make it bad\\n  Take a sad song and make it better\\n ",
        "genre": "Rock",
        "duration": 440,
        "date_created": "2022-03-21T00:00:00Z",
        "creator_id": 49
    },
    {
        "song_id": 82,
        "name": "Like a Rolling Stone",
        "lyrics": "Once upon a time you dressed so fine\\n ",
        "genre": "Rock",
        "duration": 450,
        "date_created": "2022-03-22T00:00:00Z",
        "creator_id": 50
    },
    {
        "song_id": 83,
        "name": "I Wanna Hold Your Hand",
        "lyrics": "Oh yeah, I'll tell you something\\n  I think you'll understand\\n ",
        "genre": "Pop",
        "duration": 460,
        "date_created": "2022-03-23T00:00:00Z",
        "creator_id": 51
    },
    {
        "song_id": 84,
        "name": "Smells Like Teen Spirit",
        "lyrics": "Load up on guns, bring your friends\\n ",
        "genre": "Rock",
        "duration": 470,
        "date_created": "2022-03-24T00:00:00Z",
        "creator_id": 52
    },
    {
        "song_id": 85,
        "name": "I Will Always Love You",
        "lyrics": "If I should stay\\n  I would only be in your way\\n ",
        "genre": "Pop",
        "duration": 480,
        "date_created": "2022-03-25T00:00:00Z",
        "creator_id": 53
    },
    {
        "song_id": 86,
        "name": "Bohemian Rhapsody",
        "lyrics": "Is this the real life?\\n  Is this just fantasy?\\n ",
        "genre": "Rock",
        "duration": 490,
        "date_created": "2022-03-26T00:00:00Z",
        "creator_id": 54
    },
    {
        "song_id": 87,
        "name": "I Wanna Dance with Somebody",
        "lyrics": "Clock strikes upon the hour\\n  And the sun begins to fade\\n ",
        "genre": "Pop",
        "duration": 500,
        "date_created": "2022-03-27T00:00:00Z",
        "creator_id": 55
    },
    {
        "song_id": 88,
        "name": "Lose Yourself",
        "lyrics": "You better lose yourself in the music,\\n  the moment\\n ",
        "genre": "Rap",
        "duration": 510,
        "date_created": "2022-03-28T00:00:00Z",
        "creator_id": 56
    },
    {
        "song_id": 89,
        "name": "Like a Rolling Stone",
        "lyrics": "Once upon a time you dressed so fine\\n ",
        "genre": "Rock",
        "duration": 520,
        "date_created": "2022-03-29T00:00:00Z",
        "creator_id": 57
    },
    {
        "song_id": 90,
        "name": "I Will Always Love You",
        "lyrics": "If I should stay\\n  I would only be in your way\\n ",
        "genre": "Pop",
        "duration": 530,
        "date_created": "2022-03-30T00:00:00Z",
        "creator_id": 58
    },
    {
        "song_id": 91,
        "name": "Imagine",
        "lyrics": "Imagine there's no heaven,\\n  It's easy if you try\\n ",
        "genre": "Pop",
        "duration": 540,
        "date_created": "2022-03-31T00:00:00Z",
        "creator_id": 59
    },
    {
        "song_id": 92,
        "name": "I Wanna Dance with Somebody",
        "lyrics": "Clock strikes upon the hour\\n  And the sun begins to fade\\n ",
        "genre": "Pop",
        "duration": 550,
        "date_created": "2022-04-01T00:00:00Z",
        "creator_id": 60
    },
    {
        "song_id": 93,
        "name": "I Will Always Love You",
        "lyrics": "If I should stay\\n  I would only be in your way\\n ",
        "genre": "Pop",
        "duration": 560,
        "date_created": "2022-04-02T00:00:00Z",
        "creator_id": 61
    },
    {
        "song_id": 94,
        "name": "Like a Rolling Stone",
        "lyrics": "Once upon a time you dressed so fine\\n ",
        "genre": "Rock",
        "duration": 570,
        "date_created": "2022-04-03T00:00:00Z",
        "creator_id": 62
    },
    {
        "song_id": 95,
        "name": "I Wanna Dance with Somebody",
        "lyrics": "Clock strikes upon the hour\\n  And the sun begins to fade\\n ",
        "genre": "Pop",
        "duration": 580,
        "date_created": "2022-04-04T00:00:00Z",
        "creator_id": 63
    },
    {
        "song_id": 96,
        "name": "I Will Always Love You",
        "lyrics": "If I should stay\\n  I would only be in your way\\n ",
        "genre": "Pop",
        "duration": 590,
        "date_created": "2022-04-05T00:00:00Z",
        "creator_id": 64
    },
    {
        "song_id": 97,
        "name": "Like a Rolling Stone",
        "lyrics": "Once upon a time you dressed so fine\\n ",
        "genre": "Rock",
        "duration": 600,
        "date_created": "2022-04-06T00:00:00Z",
        "creator_id": 65
    },
    {
        "song_id": 98,
        "name": "I Wanna Dance with Somebody",
        "lyrics": "Clock strikes upon the hour\\n  And the sun begins to fade\\n ",
        "genre": "Pop",
        "duration": 610,
        "date_created": "2022-04-07T00:00:00Z",
        "creator_id": 66
    },  
    {
        "song_id": 99,
        "name": "I Will Always Love You",
        "lyrics": "If I should stay\\n  I would only be in your way\\n ",
        "genre": "Pop",
        "duration": 620,
        "date_created": "2022-04-08T00:00:00Z",
        "creator_id": 67
    },
    {
        "song_id": 100,
        "name": "Like a Rolling Stone",
        "lyrics": "Once upon a time you dressed so fine\\n ",
        "genre": "Rock",
        "duration": 630,
        "date_created": "2022-04-09T00:00:00Z",
        "creator_id": 68
    }
]



'''

# Parse JSON data
songs = json.loads(json_data)

i=0
# Insert data into the table
for song in songs:


    c.execute('''
        INSERT INTO Songs VALUES (?,?,?,?,?,?,?,?)
    ''', (song['song_id'], song['name'], song['lyrics'], song['genre'], song['duration'], date_list[i],creators[i%2], song_file))
    i=i+1

# Commit the changes and close the connection
conn.commit()
conn.close()