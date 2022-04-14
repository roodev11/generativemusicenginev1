####### ------- This Program exports generative music from loops depending on rarity ------- #######
#                                 and exports metadata for OS                                      #

from pydub import AudioSegment
import random
import json

####### ----- MAKE SURE TO CHANGE EVERY ONE OF THESE IF ADDING MORE LOOPS ----- #######

# Can decide the rarity of each pool
pool = [
  "A",
  "B",
  "C",
]

pool_weightings = [30, 50, 20]

# Define what loops are in each pool
drums = [
  ["Drums 1A", "Drums 2A", "Drums 3A", "Drums 4A"],
  ["Drums 1B", "Drums 2B", "Drums 3B", "Drums 4B"],
  ["Drums 1C", "Drums 2C", "Drums 3C", "Drums 4C"],
]

bass = [
  ["Bass 1A", "Bass 2A"],
  ["Bass 1B", "Bass 2B"],
  ["Bass 1C", "Bass 2C"],
]

melody = [
  ["Melody 1A", "Melody 2A"],
  ["Melody 1B", "Melody 2B"],
  ["Melody 1C", "Melody 2C"],
]

lead = [
  ["Lead 1A", "Lead 2A", "Lead 3A", "Lead 4A", "Lead 5A", "Lead 6A"],
  ["Lead 1B", "Lead 2B", "Lead 3B", "Lead 4B"],
  ["Lead 1C", "Lead 2C", "Lead 3C"],
]

# This needs to mirror the pool array
genre = [
  "Lofi",
  "Lofi",
  "House"
]

counted = [0, 0, 0, 0]

# Define the weightings for each loop, index 0 = pool A, index 1 = pool B etc...
drums_amount = [
  [15, 35, 15, 35], 
  [35, 35, 15, 15],
  [35, 15, 35, 15],
]
bass_amount = [
  [40, 60], 
  [30, 70],
  [10, 90],
]
melody_amount = [
  [70, 30], 
  [70, 30],
  [40, 60],
]
lead_amount = [
  [20, 10, 20, 10, 10, 30], 
  [50, 30, 10, 10],
  [20, 30, 50],
]

pool_count = [0, 0, 0]

drums_count = [
  [0, 0, 0, 0],
  [0, 0, 0, 0],
  [0, 0, 0, 0],
]
bass_count = [
  [0, 0], 
  [0, 0], 
  [0, 0],
]
melody_count = [
  [0, 0], 
  [0, 0], 
  [0, 0],
]
lead_count = [
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0],
  [0, 0, 0],
]

all_loops = []

## customise so this can be used for each pool of loops
def create_new_loop():
    
    new_loop = {} #

    # For each trait category, select a random trait based on the weightings 
    new_loop ["Pool"] = random.choices(pool, pool_weightings)[0]
    new_loop ["Drums"] = random.choices(drums[pool.index(new_loop["Pool"])], drums_amount[pool.index(new_loop["Pool"])])[0]
    new_loop ["Bass"] = random.choices(bass[pool.index(new_loop["Pool"])], bass_amount[pool.index(new_loop["Pool"])])[0]
    new_loop ["Melody"] = random.choices(melody[pool.index(new_loop["Pool"])], melody_amount[pool.index(new_loop["Pool"])])[0]
    new_loop ["Lead"] = random.choices(lead[pool.index(new_loop["Pool"])], lead_amount[pool.index(new_loop["Pool"])])[0]
    new_loop ["Genre"] = genre[pool.index(new_loop["Pool"])]

    if new_loop in all_loops:
        return create_new_loop()
    else:
        return new_loop

# Generate the unique combinations based on trait weightings
for i in range(10): 
    
    new_trait_loop = create_new_loop()
    
    all_loops.append(new_trait_loop)

# Returns true if all loops are unique
def all_loops_unique(all_loops):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_loops)

print("Are all loops unique?", all_loops_unique(all_loops))
print(f"Amount of Loops: {len(all_loops)}")

# Add token Id to each image
i = 1
for item in all_loops:
    item["tokenId"] = i
    i = i + 1

print(*all_loops, sep='\n')

####### ITERATE OVER ALL COMBINATIONS OF LOOPS ########
for item in all_loops:

# Create a JSON metadata file ---- This will need changing when the art side is done
    nft_data ={
      "description": "A saintly figure, doused in holiness. No two songs or characters are the same...", 
      "external_url": "https://saintsofsound.io/", 
      "image": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png", 
      "name": f"Saint #{str(item['tokenId']).zfill(4)}",
      "attributes": [
            {
                  "trait_type": "Unique?",
                  "value": "Yes"
            },
            {
                  "trait_type": "Background",
                  "value": "Orange"
            },
            {
                  "trait_type": "Halo",
                  "value": "Royal"
            },
            {
                  "trait_type": "Hair",
                  "value": "Royal"
            },
            {
                  "trait_type": "Eyes",
                  "value": "Vertical"
            },
            {
                  "trait_type": "Clothes",
                  "value": "Royal"
            },
            {
                  "trait_type": "Genre",
                  "value": item["Genre"]
            },
            {
                  "trait_type": "Drums",
                  "value": f"{item['Genre']} {item['Drums']}" 
            },
            {
                  "trait_type": "Bass",
                  "value": f"{item['Genre']} {item['Bass']}"   
            },
            {
                  "trait_type": "Melody",
                  "value": f"{item['Genre']} {item['Melody']}" 
            },
            {
                  "trait_type": "Lead",
                  "value": f"{item['Genre']} {item['Lead']}"
            }
        ]
    }

    # Serialize data
    json_object = json.dumps(nft_data, indent = 2)

    # Writing to json files
    with open(f"output/test2/json/{item['tokenId']}.json", "w") as outfile:
          outfile.write(json_object)


    ######## MUSIC STUFF #########

    drums_path = f"audio/{item['Pool']}/1_drums/{drums[pool.index(item['Pool'])].index(item['Drums']) + 1}.wav"
    bass_path = f"audio/{item['Pool']}/2_bass/{bass[pool.index(item['Pool'])].index(item['Bass']) + 1}_{drums[pool.index(item['Pool'])].index(item['Drums']) + 1}.wav"
    melody_path = f"audio/{item['Pool']}/3_melody/{melody[pool.index(item['Pool'])].index(item['Melody']) + 1}_{drums[pool.index(item['Pool'])].index(item['Drums']) + 1}.wav"
    lead_path = f"audio/{item['Pool']}/4_lead/{lead[pool.index(item['Pool'])].index(item['Lead']) + 1}_{drums[pool.index(item['Pool'])].index(item['Drums']) + 1}.wav"

    # Set the loops according to combination
    drums_loop = AudioSegment.from_wav(drums_path)
    bass_loop = AudioSegment.from_wav(bass_path)
    melody_loop = AudioSegment.from_wav(melody_path)
    lead_loop = AudioSegment.from_wav(lead_path)
    
    #print(f"audio/{item['Pool']}/4_lead/{lead[pool.index(item['Pool'])].index(item['Lead']) + 1}_{drums[pool.index(item['Pool'])].index(item['Drums']) + 1}.wav")
    # Overlay the drums and bass, and then the melodies to create final mix
    drumsandbass = drums_loop.overlay(bass_loop, position=0)
    melodyandlead = melody_loop.overlay(lead_loop, position=0)
    overlay = drumsandbass.overlay(melodyandlead, position=0)


    # Export audio as mp3 - wav is faster but obviously takes more space, named with the counter
    file_handle = overlay.export(f"output/test2/audio/{item['tokenId']}.wav", format="wav")


    ######### Keep count of each loop #########
    # Add to the count of each loop depending on Pool
    pool_count[pool.index(item["Pool"])] += 1
    drums_count[pool.index(item["Pool"])][drums[pool.index(item["Pool"])].index(item["Drums"])] += 1
    bass_count[pool.index(item["Pool"])][bass[pool.index(item["Pool"])].index(item["Bass"])] += 1
    melody_count[pool.index(item["Pool"])][melody[pool.index(item["Pool"])].index(item["Melody"])] += 1
    lead_count[pool.index(item["Pool"])][lead[pool.index(item["Pool"])].index(item["Lead"])] += 1


# Print to console the tally of each loop, can compare with set weightings
print("---------------------")
print("Pool Count...")
print(*pool_count, sep='\n')
print("---------------------")
print("Drums Count...")
print(*drums_count, sep='\n')
print("---------------------")
print("Bass Count...")
print(*bass_count, sep='\n')
print("---------------------")
print("Melody Count...")
print(*melody_count, sep='\n')
print("---------------------")
print("Lead Count...")
print(*lead_count, sep='\n')
print("---------------------")
