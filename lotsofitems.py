#! /usr/bin/python
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

from models import *

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Items).delete()
# Delete Users if exisitng.
session.query(User).delete()

# Create fake user
User1 = User(name="Chris S.",
              email="chriss0@gmail.com",
              picture='https://pbs.twimg.com/profile_images/880157232398180356/_0m67-aw_400x400.jpg')
session.add(User1)
session.commit()



category1 = Category(name="Recording", user=User1)
session.add(category1)
session.commit()
category2 = Category(name="Musical Instruments", user=User1)
session.add(category2)
session.commit()
category3 = Category(name="Live Sound", user=User1)
session.add(category3)
session.commit()
category4 = Category(name="Computer Audio", user=User2)
session.add(category4)
session.commit()

Item1 = Item(name="Yamaha TF1 Digital Mixing Console",      
            price="$1,999.99",
            description="The Yamaha TF1 is a rack-mountable digital audio mixing console.",            
            image="https://static.bhphoto.com/images/images500x500/yamaha_tf1_16_1_fader_digital_audio_1429542047000_1138578.jpg",
            category=category1,
            user = User1)

session.add(Item1)
session.commit()

Item2 = Item(name="Mackie ProFX12v2 12-Channel Sound Reinforcement Mixer with Built-In FX",
            price="$249.99",      
            description="The ProFX12v2 12-channel mixing console from Mackie features a built-in effects engine, and is ideal for a plethora of live sound reinforcement applications ranging from live bands and DJs to lecturers and presenters.",
            image="https://static.bhphoto.com/images/images500x500/mackie_profx12v2_12_channel_professional_fx_mixer_1429724326000_1139063.jpg",
            category=category1,
            user=User1)

session.add(Item2)
session.commit()


#Some category 2 items
Item3 = Item(name="Alesis Melody 61 - 61-Key Portable Keyboard with Accessories Kit",
            price="$99.00",
            description="The Melody 61 Portable Keyboard with Accessories Kit from Alesis includes a 61-key, compact and lightweight keyboard with built-in speakers, piano bench, handheld microphone, power adapter, headphones, and a keyboard stand and has 200 built in sounds.",
            image="https://static.bhphoto.com/images/images500x500/alesis_melody61_melody_61_61_key_portable_1490018803000_1326754.jpg",
            category=category2,
            user = User1)

session.add(Item3)
session.commit()


Item4 = Item(name="Alesis Forge 8-Piece Electronic Drum Kit with Module",
            price="$499.00",
            description="The Forge Drum Kit from Alesis is an 8-piece electronic drum set with 3 cymbals, a 4-post aluminum rack, and all connection cables and hardware. It can be used in applications for recording studios, live stage, rehearsals, and more.",
            image="https://static.bhphoto.com/images/images500x500/alesis_forge_8_piece_electronic_drum_1454945738000_1222660.jpg",
            category=category2,
            user = User1)

session.add(Item4)
session.commit()


#Some category 3 items
Item5 = Item(name="Shure SM58-LC Dynamic Microphone with Stand & Cable Kit",
            price="$110.99",
            description="The SM58-LC Vocal Microphone from Shure features a unidirectional (cardioid) dynamic vocal design, suitable for professional vocal use in live performance, sound reinforcement, and studio recording.",
            image="https://static.bhphoto.com/images/images500x500/1432063238000_688464.jpg",
            category=category3,
            user = User1)

session.add(Item5)
session.commit()

Item6 = Item(name="QSC K12.2 K.2 Series 12 inch, 2-Way 2000 Watt Powered Speaker",
            price="$799.99",      
            description="The K.2 Series K12.2 Two-Way 2000 Watt Powered Speaker from QSC features 'next generation' upgrades to the popular K-Series powered speakers and is well suited for live bands, public speaking, DJ and Club applications, as well as schools, houses of worship, and event production companies.",
            image="https://static.bhphoto.com/images/images500x500/qsc_k12_2_k_2_series_1492404606000_1329322.jpg",
            category=category3,
            user = User1)

session.add(Item6)
session.commit()


#Some category 4 items
Item7 = Item(name="Focusrite Scarlett 2i2 USB Audio Interface (2nd Generation)",
            price="$149.99",      
            description="Focusrite's second-generation Scarlett 2i2 is a portable audio interface designed specifically for use in a portable computer environment.",
            image="https://static.bhphoto.com/images/images500x500/focusrite_scarlett_2i2_2nd_gen_scarlett_2i2_usb_audio_1464752813000_1251655.jpg",
            category=category4,
            user = User1)

session.add(Item7)
session.commit()

Item8 = Item(name="Image-Line FL Studio 12 Producer Edition - Complete Music Production Software (Boxed)",
            price="$199.00",      
            description="The FL Studio 12 Producer Edition from Image-Line is a complete software music production environment.",
            image="https://static.bhphoto.com/images/images500x500/image_line_10_15222_fl_studio_12_producer_1430400101000_1142132.jpg",
            category=category4,
            user= User1)

session.add(Item8)
session.commit()


print "added new items!"

Base.metadata.create_all(engine)