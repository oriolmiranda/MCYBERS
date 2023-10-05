import subprocess
import os

IV_ARRAY = [0x01FF00, 0x03FF00, 0x04FF00, 0x05FF00, 0x06FF00, 0x07FF00, 0x08FF00, 0x09FF00, 0x0AFF00, 0x0BFF00, 0x0CFF00, 0x0DFF00, 0x0EFF00, 0x0FFF00]

INITIAL_IV = 0x01FF00
KEY = 0x870a4b6c091ffd2a9485c97b99

def calculate_iv_vectors(initial_iv):
    folder_path = './files'
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If it doesn't exist, create it
        os.makedirs(folder_path)
        print(f"Directory {folder_path} has been created.")
    filename = "bytes_" + format(initial_iv, '06X')
    path = './files/' + filename[0:10] + 'xx.DAT'
    file = open(path, "w")
    for i in range(256):
        iv = initial_iv + i
        try:
            # Convert iv and KEY to hexadecimal strings and concatenate them
            hex_key = format(iv, '06X') + format(KEY, 'X')
            #command = f'cat ./byte.txt | ./test -L 16 -K {hex_key}'
            command = f"echo -n 'f'| ./test -L 16 -K {hex_key}"
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, check=True)
            # result = subprocess.run(['cat ./byte.txt', '|', './test', '-L', '16', '-K', hex_key, './byte.txt'], stdout=subprocess.PIPE, text=True, check=True)
            cypher = result.stdout
            cypher_int = int.from_bytes(cypher, byteorder='big')
            line = '0X{:06X}'.format(iv) + ' 0X{:02X}'.format(cypher_int) + '\n'
            file.write(line)
        except subprocess.CalledProcessError as e:
            print(f"Error running './test -L -K': {e}")
            file.close()

    file.close()

if __name__ == '__main__':
    print("Key used: 0x{:13X}".format(KEY))

    for iv in IV_ARRAY:
        calculate_iv_vectors(iv)
        print("File for iv: 0X{:04X}XX created.".format(iv))
    # vectors, cyphers = calculate_iv_vectors()
    # print(['0x{:06X}'.format(iv) for iv in vectors])
    # print([hex(iv) for iv in vectors])
    # print(vectors)
    # print(cyphers)
