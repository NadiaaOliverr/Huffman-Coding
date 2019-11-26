# -*- coding: utf-8 -*-
import os.path
import time
import re
import struct

#
# Implementation of a compression text using Huffman's algorithm
#
__authors__ = "Genilton Barbosa, Nádia Oliveira e Natália Camilo"

#
# Functions of archives
#


def read_archive(name_archive):
    text_encode = []
    document = open(name_archive, 'r')
    text_archive = document.readlines()
    for line in text_archive:
        text_encode.append(line)
    document.close()
    return text_encode


def read_archive_bin(name_archive):
    answer_decimal = []
    control = 0

    with open(name_archive, 'rb') as files:
        data = files.read()
        control = 0
    while control <= len(data)-2:
        answer_decimal.append(struct.unpack(
            '<H', data[control:(control+2)])[0])
        control += 2

    return answer_decimal


def write_archive(string, name_archive):
    document = open(name_archive, 'w')
    document.write(str(string))
    document.close()


def write_archive_bin(pack_bin, name_archive):
    with open(name_archive, 'ab') as files:
        files.write(pack_bin)

#
# Functions of menu
#


def clear_screen():
	print("Redirecting, wait a moment...")
	time.sleep(2)
	os.system('clear') or None


def instructions():

    clear_screen()
    print("\n----= Information =----\n")
    print("[1] - It is only possible to compress and unpack ONE phrase at a time")
    print("Você será redirecionado em 3 segundos...")
    time.sleep(3)
    clear_screen()
    menu()


def encrypt():
    if(os.path.isfile('.treehuffman.txt')):
        print("There is a phrase to be unpacked, press key 2")
        time.sleep(3)
        os.system('clear') or None
        menu()
    else:
        print("\nWrite the phrase to be compressed: ", end="")
        string = str(input())
        write_archive(string, 'Originalarchive.txt')
        huffman_encrypt(string)


def menu():

	try:
	    print("\n----= Text Compressor =----\n")
	    print("Choose one option below")
	    print("[1] - Compress")
	    print("[2] - Unpack")
	    print("[3] - Information")
	    print("[4] - Exit\n")
	    print("Option: ", end="")
	    option = int(input())
	    while option < 1 or option > 4:
	        print("\nYou have chosen an invalid option, please choose again")
	        print("Option: ", end="")
	        option = int(input())
	    if option == 1:
	        encrypt()
	    elif option == 2:
	        huffman_decrypt()
	    elif option == 3:
	        instructions()
	    elif option == 4:
	        print("\nYou chose to leave...\n")
	        exit(1)
	except ValueError:
        	print("\nYou have chosen an invalid option, please choose again")
        	clear_screen()
        	menu()


#
# Functions of manipulations string
#


def remove_characters(string):
    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace("'", '')
    string = string.replace("'", '')
    return string

#
# Functions convert bin/dec and dec/bin
#


def dec_for_bin(decimal):
    binary = ''
    while decimal != 0:
        binary = binary + str(decimal % 2)
        decimal = int(decimal / 2)
    return binary[::-1]


def bin_for_dec(binary):

    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

#
# Functions of compress/decompress file
#


def compress_file(word_dvz):
    sequence_16bits = []
    control = 0
    quantity_zeros = []
    decimal = []

    while control != 1:
        if len(word_dvz) <= 16:
            sequence_16bits.append(word_dvz)
            control = 1
        else:
            sequence_16bits.append(word_dvz[:16])
            word_dvz = word_dvz[16:]
            control = 0

    for i in range(len(sequence_16bits)):
        quantity_zeros.append(sequence_16bits[i].count("0"))

    for i in range(len(sequence_16bits)):
        decimal.append(bin_for_dec(int(sequence_16bits[i])))

    for i in range(len(decimal)):
        bin_data = struct.pack('<H', decimal[i])
        write_archive_bin(bin_data, 'Compressedarchive.dvz')

    return quantity_zeros


def decompress(quantity_zeros):
    answer_decimal = read_archive_bin('Compressedarchive.dvz')
    huffman_number = []

    for i in range(len(answer_decimal)):
        binary = dec_for_bin(answer_decimal[i])
        if binary.count("0") != quantity_zeros[i]:
            size_zeros = quantity_zeros[i] - binary.count("0")
            missing_zeros = "0" * size_zeros
            binary = missing_zeros + binary
        huffman_number.append(binary)

    huffman_number = str(huffman_number)
    result_huffman_decompress = remove_characters(huffman_number)
    result_huffman_decompress = result_huffman_decompress.replace(",", "")
    result_huffman_decompress = result_huffman_decompress.replace(" ", "")

    return result_huffman_decompress

#
# Functions of huffman algorithm
#


def table_frequency(string):
    letters = []
    only_letters = []
    for letter in string:
        if letter not in letters:
            frequency = string.count(letter)
            letters.append(frequency)
            letters.append(letter)
            only_letters.append(letter)
    print("\nFrenquency of characters table")
    print(letters)
    return letters, only_letters


def huffman_encrypt(string):

    letters, only_letters = table_frequency(string)

    # Gerando uma floresta onde cada caracter é um nó
    nodes = []
    while len(letters) > 0:
        nodes.append(letters[0:2])
        letters = letters[2:]

    nodes.sort()
    huffman_tree = []
    huffman_tree.append(nodes)

    def tree(nodes):
        position = 0
        newnode = []
        if len(nodes) > 1:
            nodes.sort()
            nodes[position].append("0")
            nodes[position+1].append("1")
            join_node1 = (nodes[position][0] + nodes[position+1][0])
            join_node2 = (nodes[position][1] + nodes[position+1][1])
            newnode.append(join_node1)
            newnode.append(join_node2)
            newnodes = []
            newnodes.append(newnode)
            newnodes = newnodes + nodes[2:]
            nodes = newnodes
            huffman_tree.append(nodes)
            tree(nodes)
        return huffman_tree

    tree(nodes)
    huffman_tree.sort(reverse=True)

    checklist = []
    for level in huffman_tree:
        for node in level:
            if node not in checklist:
                checklist.append(node)
            else:
                level.remove(node)

    letter_binary = []
    if len(only_letters) == 1:
        letter_code = [only_letters[0], "0"]
        letter_binary.append(letter_code*len(string))
    else:
        for letter in only_letters:
            lettercode = ""
            for node in checklist:
                if len(node) > 2 and letter in node[1]:
                    lettercode = lettercode + node[2]
            lettercode = [letter, lettercode]
            letter_binary.append(lettercode)

    decompression = []
    print("\nHuffman's Table: ".upper())
    for letter in letter_binary:
        print(letter[0], letter[1])
        decompression.append(letter[0])
        decompression.append(letter[1])

    word_dvz = []

    for letter in string:
        if letter in string:
            position = decompression.index(letter)
            word_dvz.append(decompression[position+1])

    separator = ''
    result = [separator.join(word_dvz)]
    result = str(result)
    word_dvz = remove_characters(result)
    print("\nThe phrase in Huffman is: ".upper(), end="")
    print(word_dvz)

    binary = ((bin(int(word_dvz, base=2))))
    size_bin = len(binary) - 2
    print("\nOriginal text has {0} bits".format(str(len(word_dvz)*8)))
    print("\nCompressed text has {0} bits".format(size_bin))

    word_to_record = decompression
    word_to_record = str(word_to_record)
    word_to_record = word_to_record.replace("[", "")
    word_to_record = word_to_record.replace("]", "")
    word_to_record = word_to_record.replace("'", "")
    word_to_record = word_to_record.replace("'", "")
    word_to_record = word_to_record.replace(",", "")

    slicing = word_to_record.split()

    quantity_zeros = compress_file(word_dvz)
    document = open('.treehuffman.txt', 'a')
    document.write(str(quantity_zeros))
    document.write('\n')

    for i in range(len(slicing)):
        if string.find('1') != -1 or string.find('0') != -1 or string.find(' ') != -1:
            document = open('.treehuffman.txt', 'w')
            document.write(string)
            break
        document = open('.treehuffman.txt', 'a')
        document.write(slicing[i])
        document.write('\n')

    document.close()


def huffman_decrypt():

    if(os.path.isfile('Compressedarchive.dvz')):

        separator = ''
        quantity_zeros = []

        with open('.treehuffman.txt') as f:
            string_read = [line.rstrip('\n') for line in f]

        size_string_read = len(string_read)

        if size_string_read > 1:
            for i in string_read[0]:
                if i.isdigit():
                    quantity_zeros.append(int(i))

            quantity_zeros = list(quantity_zeros)
            string = decompress(quantity_zeros)
            string_read = string_read[1:]

            numbers = []

            for i in string:
                numbers.append(i)

            i = 0
            walks = numbers[::]

            i = 1
            word = []
            size = len(walks)

            numbers = walks[0:i]
            numbers = str(numbers)
            pattern = re.search(r"[0-1]+", numbers)
            numbers = pattern.group()

        if size_string_read > 1:
            while size > 0:
                if numbers in string_read:
                    position = string_read.index(numbers)
                    word.append(string_read[position-1])
                    numbers = walks[i::]
                    walks = numbers
                    if len(numbers) == 1:
                        numbers = str(numbers)
                        pattern = re.search(r"[0-1]+", numbers)
                        numbers = pattern.group(0)
                    i = 1
                else:
                    i += 1
                    numbers = walks[0:i]
                    result = [separator.join(numbers)]
                    numbers = result
                    numbers = str(numbers)
                    if numbers == "['']":
                        break
                    else:
                        pattern = re.search(r"[0-1]+", numbers)
                        numbers = pattern.group(0)
                size -= 1
        os.remove('.treehuffman.txt')
        os.remove('Originalarchive.txt')
        os.remove('Compressedarchive.dvz')

        if size_string_read > 1:
            result = [separator.join(word)]
            result = str(result)
            result_archive = remove_characters(result)
            print()
            print('The word that is in the archive is: {0}'.format(
                result_archive))
        else:
            print()
            string_read = str(string_read)
            string_read = remove_characters(string_read)
            print('The word that is in the archive is: {0}'.format(string_read))

    else:
        print("There is nothing compressed yet")
        time.sleep(2)
        os.system('clear') or None
        menu()


if __name__ == "__main__":

    menu()
