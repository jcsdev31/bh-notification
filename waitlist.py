import json
from PIL import Image
import os
from io import BytesIO

image_counter = 0
errimage_counter = 0

is_running = False
instance_id = "Tome_of_Glory"
instance_udid = None
is_restart = False

async def set_active_guild(guild_id):
    append_to_list_and_save(guild_id, 'guild.json')

async def set_type_waitlist(message):
    append_to_list_and_save(message, 'type.json')

async def set_message_waitlist(message, boss_name):
    append_to_list_and_save([message, boss_name], 'message.json')

async def set_haze_waitlist(message):
    append_to_list_and_save(message, 'haze.json')

async def set_image_waitlist(message, boss_name, image_buffer):
    global image_counter
    image_counter += 1
    
    image = Image.open(image_buffer)
    filename = f"img-{image_counter}.png"
    image.save(filename)
    append_to_list_and_save([filename, message, boss_name], 'image.json')

async def set_status_waitlist(boss_name, status, is_announced):
    append_to_list_and_save([boss_name, status, is_announced], 'status.json')

async def set_error_waitlist(err_message, e):
    append_to_list_and_save([err_message, e], 'error.json')

async def set_errimage_waitlist(err_message, image_buffer):
    global errimage_counter
    errimage_counter += 1
    image = Image.open(image_buffer)
    filename = f"img-err{errimage_counter}.png"
    image.save(filename)
    append_to_list_and_save([filename, err_message], 'errimage.json')

def get_active_guilds():
    return load_data_from_file('guild.json')

def get_type_waitlist():
    return pop_from_list_and_save(0, 'type.json')

def get_message_waitlist():
    return pop_from_list_and_save(0, 'message.json')

def get_haze_waitlist():
    return pop_from_list_and_save(0, 'haze.json')

def get_image_waitlist():
    new_image = None
    while not new_image:
        new_image = pop_from_list_and_save(0, 'image.json')
    filename, message, boss_name = new_image
    image = Image.open(filename)
    image_buffer = BytesIO()
    image.save(image_buffer, format='PNG')
    try:
        os.remove(filename)
        print(f"Original image file '{filename}' deleted.")
    except FileNotFoundError:
        print(f"Original image file '{filename}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
    return [message, boss_name, image_buffer]

def get_status_waitlist():
    return pop_from_list_and_save(0, 'status.json')

def get_error_waitlist():
    return pop_from_list_and_save(0, 'error.json')

def get_errimage_waitlist():
    new_image = None
    while not new_image:
        new_image = pop_from_list_and_save(0, 'errimage.json')
    filename, message = new_image
    image = Image.open(filename)
    image_buffer = BytesIO()
    image.save(image_buffer, format='PNG')
    try:
        os.remove(filename)
        print(f"Original image file '{filename}' deleted.")
    except FileNotFoundError:
        print(f"Original image file '{filename}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
    return [message, image_buffer]

def load_data_from_file(filename):
    success = False
    while not success:
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            success = True
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []
            success = True
        except Exception as e:
            print(f"Error opening file {filename}: {e}")

    return data

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def append_to_list_and_save(item, filename):
    # Load existing data from file or initialize an empty list
    data = load_data_from_file(filename)

    # Append the new item to the list
    data.append(item)

    # Save the updated list to the file
    save_data_to_file(data, filename)

def pop_from_list_and_save(index, filename):
    # Load existing data from file or initialize an empty list
    data = load_data_from_file(filename)

    if 0 <= index < len(data):
        # Pop the item from the list
        popped_item = data.pop(index)

        # Save the updated list to the file
        save_data_to_file(data, filename)

        return popped_item
    else:
        return None

def clear_active_guilds():
    try:
        os.remove('guild.json')
        print(f"File '{'guild.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'guild.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")

def clear_all_json():
    try:
        os.remove('errimage.json')
        print(f"File '{'errimage.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'errimage.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
    
    try:
        os.remove('error.json')
        print(f"File '{'error.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'error.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
        
    try:
        os.remove('haze.json')
        print(f"File '{'haze.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'haze.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
        
    try:
        os.remove('image.json')
        print(f"File '{'image.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'image.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
        
    try:
        os.remove('message.json')
        print(f"File '{'message.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'message.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
        
    try:
        os.remove('status.json')
        print(f"File '{'status.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'status.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")
    
    try:
        os.remove('type.json')
        print(f"File '{'type.json'}' deleted.")
    except FileNotFoundError:
        print(f"File '{'type.json'}' not found.")
    except Exception as e:
        print(f"Error deleting the original image file: {e}")