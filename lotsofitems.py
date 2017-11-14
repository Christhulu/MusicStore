"""
    Drop and create all tables.
    Populate application database with sample data.
"""

from database_setup import clearDb, session
from catalog.models import User, Category, Items
from datetime import datetime


def createCategory(name, user_id):
    """ Create a category record """
    c = Category(name=name, user_id=user_id)
    session.add(c)
    session.commit()
    return c


def createItem(name, price, description, image, category_id,  user_id):
    """ Create an item record """
    i = Items(name=name, price=price, description=description,
             image=image, category_id=category_id, user_id=user_id)
    session.add(i)
    session.commit()
    return i


def createUser(name, email, picture):
    """ Create a user record """
    u = User(name=name, email=email, picture=picture)
    session.add(u)
    session.commit()
    return u

# Clear database tables
clearDb()

# Create fake user
User1 = createUser("Chris S.", "chriss0@gmail.com", "https://pbs.twimg.com/profile_images/880157232398180356/_0m67-aw_400x400.jpg")

User2 = createUser("the boy", "theboy0@gmail.com", "https://pbs.twimg.com/profile_images/880157232398180356/_0m67-aw_400x400.jpg")



category1 = createCategory("Recording", User1.id)

category2 = createCategory("Musical Instruments", User1.id)

category3 = createCategory("Live Sound", User1.id)

category4 = createCategory("Computer Audio", User1.id)




Item1 = createItem("Yamaha TF1 Digital Mixing Console", "$1,999.99", "The Yamaha TF1 is a rack-mountable digital audio mixing console.",            
            "https://static.bhphoto.com/images/images500x500/yamaha_tf1_16_1_fader_digital_audio_1429542047000_1138578.jpg",
            category1.id,
            User1.id)


Item2 = createItem("Mackie ProFX12v2 12-Channel Sound Reinforcement Mixer with Built-In FX",
            "$249.99",      
            "The ProFX12v2 12-channel mixing console from Mackie features a built-in effects engine, and is ideal for a plethora of live sound reinforcement applications ranging from live bands and DJs to lecturers and presenters.",
            "https://static.bhphoto.com/images/images500x500/mackie_profx12v2_12_channel_professional_fx_mixer_1429724326000_1139063.jpg",
            category1.id,
            User1.id)




#Some category 2 items
Item3 = createItem("Alesis Melody 61 - 61-Key Portable Keyboard with Accessories Kit",
            "$99.00",
            "The Melody 61 Portable Keyboard with Accessories Kit from Alesis includes a 61-key, compact and lightweight keyboard with built-in speakers, piano bench, handheld microphone, power adapter, headphones, and a keyboard stand and has 200 built in sounds.",
            "https://static.bhphoto.com/images/images500x500/alesis_melody61_melody_61_61_key_portable_1490018803000_1326754.jpg",
            category2.id,
            User1.id)




Item4 = createItem("Alesis Forge 8-Piece Electronic Drum Kit with Module",
            "$499.00",
            "The Forge Drum Kit from Alesis is an 8-piece electronic drum set with 3 cymbals, a 4-post aluminum rack, and all connection cables and hardware. It can be used in applications for recording studios, live stage, rehearsals, and more.",
            "https://static.bhphoto.com/images/images500x500/alesis_forge_8_piece_electronic_drum_1454945738000_1222660.jpg",
            category2.id,
            User1.id)




#Some category 3 items
Item5 = createItem("Shure SM58-LC Dynamic Microphone with Stand & Cable Kit",
            "$110.99",
            "The SM58-LC Vocal Microphone from Shure features a unidirectional (cardioid) dynamic vocal design, suitable for professional vocal use in live performance, sound reinforcement, and studio recording.",
            "https://static.bhphoto.com/images/images500x500/1432063238000_688464.jpg",
            category3.id,
            User1.id)


Item6 = createItem("QSC K12.2 K.2 Series 12 inch, 2-Way 2000 Watt Powered Speaker",
            "$799.99",      
            "The K.2 Series K12.2 Two-Way 2000 Watt Powered Speaker from QSC features 'next generation' upgrades to the popular K-Series powered speakers and is well suited for live bands, public speaking, DJ and Club applications, as well as schools, houses of worship, and event production companies.",
            "https://static.bhphoto.com/images/images500x500/qsc_k12_2_k_2_series_1492404606000_1329322.jpg",
            category3.id,
            User1.id)




#Some category 4 items
Item7 = createItem("Focusrite Scarlett 2i2 USB Audio Interface (2nd Generation)",
            "$149.99",      
            "Focusrite's second-generation Scarlett 2i2 is a portable audio interface designed specifically for use in a portable computer environment.",
            "https://static.bhphoto.com/images/images500x500/focusrite_scarlett_2i2_2nd_gen_scarlett_2i2_usb_audio_1464752813000_1251655.jpg",
            category4.id,
            User1.id)



Item8 = createItem("Image-Line FL Studio 12 Producer Edition - Complete Music Production Software (Boxed)",
            "$199.00",      
            "The FL Studio 12 Producer Edition from Image-Line is a complete software music production environment.",
            "https://static.bhphoto.com/images/images500x500/image_line_10_15222_fl_studio_12_producer_1430400101000_1142132.jpg",
            category4.id,
            User1.id)




print "added new items!"
