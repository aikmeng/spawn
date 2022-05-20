# File generation technique taken https://www.bswen.com/2018/04/python-How-to-generate-random-large-file-using-python.html

import click
import os 
import random
import string
import time

NOUNS = ("puppy", "car", "rabbit", "girl", "monkey")
VERBS = ("runs", "hits", "jumps", "drives", "barfs")
ADVERBS = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
ADJECTIVES = ("adorable", "clueless", "dirty", "odd", "stupid")
ALL_WORDS = [NOUNS, VERBS, ADJECTIVES, ADVERBS]

BATCH_SIZE = 64 * 128
PROGRESS_REPORT_STEPS = 10
PROGRESS_REPORT_SIZE = PROGRESS_REPORT_STEPS * BATCH_SIZE

def generate_big_sparse_file(file_name, target_size):
    with open(file_name, 'wb') as file_object:
        file_object.seek(target_size - 1)
        file_object.write(os.urandom(1))

def write_big_random_bin_file(file_object, write_size):
    file_object.write(os.urandom(write_size))
    return "bytes"

def generate_big_random_bin_file(file_name, target_size):
    with open(file_name, 'wb') as file_object:
        write_file_in_batch(write_big_random_bin_file, file_object, target_size, file_name)

def write_big_random_letters(file_object, write_size):
    chars = ''.join([random.choice(string.ascii_letters) for index in range(write_size)])
    file_object.write(chars)
    return "characters"

def generate_big_random_letters(file_name, target_size):
    with open(file_name, 'w') as file_object:
        write_file_in_batch(write_big_random_letters, file_object, target_size, file_name)     

def write_big_random_sentences(file_object, write_size):
    for index in range(write_size):
        file_object.writelines([' '.join([random.choice(word_index) for word_index in ALL_WORDS]),'\n'])
    return "rows"

def generate_big_random_sentences(file_name, line_count):
    with open(file_name,'w') as file_object:
        write_file_in_batch(write_big_random_sentences, file_object, line_count, file_name)    

def write_file_in_batch(file_write_method, file_object, target_size, file_name):
    current_size = 0
    write_size = BATCH_SIZE
    progress_report_counter = 0

    while current_size + BATCH_SIZE < target_size:
        current_size, progress_report_counter = write_file(file_write_method, file_object, current_size, BATCH_SIZE, target_size, file_name, progress_report_counter)
    
    write_size = target_size - current_size
    if write_size > 0:
        current_size, progress_report_counter = write_file(file_write_method, file_object, current_size, write_size, target_size, file_name, progress_report_counter)

def write_file(file_write_method, file_object, current_size, write_size, target_size, file_name, progress_report_counter):
    unit = file_write_method(file_object, write_size)
    current_size += write_size

    report_flag, progress_report_counter = should_report_progress(progress_report_counter, current_size, target_size)    
    if (report_flag):
        click.echo(f"Populating {file_name} with {write_size} {unit}. Current Progress {current_size}/{target_size}, {current_size / target_size * 100:0.2f}%")
    
    return current_size, progress_report_counter

def should_report_progress(progress_report_counter, current_size, target_size):
    if(target_size < PROGRESS_REPORT_SIZE):
        return False, 0

    report_interval = target_size / PROGRESS_REPORT_STEPS
    if(current_size > report_interval * (progress_report_counter + 1)):
        progress_report_counter = progress_report_counter + 1
        return True, progress_report_counter
    
    return False, progress_report_counter

def generate_file(type, size, file_index):
    generate_file_start_time = time.perf_counter()

    epoch_time = int(time.time())
    file_name = f"{epoch_time}-{file_index}"

    match type:
        case 1:
            file_name = f"empty-{file_name}.dat"
            generate_big_sparse_file(file_name, size)
        case 2:
            file_name = f"binary-{file_name}.dat"
            generate_big_random_bin_file(file_name, size)
        case 3:
            file_name = f"letters-{file_name}.log"
            generate_big_random_letters(file_name, size)
        case 4:
            file_name = f"sentences-{file_name}.txt"
            generate_big_random_sentences(file_name, size)
        case _:
            click.echo(f"{type} is invalid")
    
    generate_file_end_time = time.perf_counter()
    click.echo(f"{file_name} is generated in {generate_file_end_time - generate_file_start_time:0.4f} seconds")

@click.command()
@click.option('-t', '--type', default=1, help="""Type of file generation
    (1 - Sparse/Empty,
    2 - Random Binary,
    3 - Random Letters,
    4 - Random Sentences)""")
@click.option('-c', '--count', default=1, help='Number of files')
@click.option('-s', '--size', default=1000, help='Size of file generation')
def main(type, count, size):
    for file_index in range(count):
        generate_file(type, size, file_index)

if __name__ == '__main__':
    main()