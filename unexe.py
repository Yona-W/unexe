from io import TextIOWrapper
import struct
import json
from pathlib import Path
import os

def separate(file : TextIOWrapper, code_size : int, bundle_size : int, meta_size : int):

    Path("./output").mkdir(exist_ok=True)
    os.chdir("./output")

    print("Seeking to bundle")
    file.seek(-bundle_size - meta_size, 2)
    bundle = file.read(bundle_size)

    print("Extracting full bundle as-is")
    bundle_file = open("bundle.out", "wb")
    bundle_file.write(bundle)
    bundle_file.close()

    print("Seeking to code")
    file.seek(-bundle_size -code_size - meta_size, 2)
    code = str(file.read(code_size))

    print("Locating filesystem index")
    index_start = '{"resources":{'
    index_end = '}'
    start_pos = (code.find(index_start))
    if(start_pos == -1):
        print("Could not find filesystem index, maybe nexe changed some things?")
        return
    
    start_pos += len(index_start)
    end_pos = code.find(index_end, start_pos)

    if(end_pos == -1):
        print("FS index starts but doesn't end, literally how?")
        return

    index = code[start_pos - 1:end_pos + 1]
    mappings = json.loads(index)

    print("Found", len(mappings), "files to extract. Summary of files:")

    for key in mappings:
        print("\t" + key.replace("\\\\", "/"))

    if(input("Extract individual files? [y/N] ") != "y"):
        return

    for key in mappings:
        path = key.replace("\\\\", "/")
        (start, length) = mappings[key]
        print("Extracting file '" + path + "' with length", length)

        if(os.path.exists(path)):
            if(input("File exists, overwrite? (This may be a security risk!) [y/N] ") != "y"):
                continue

        directory = os.path.dirname(path)
        Path(directory).mkdir(parents=True, exist_ok=True)

        output_file = open(path, "wb")
        output_buf = bundle[start : start + length]
        output_file.write(output_buf)
        output_file.close()

    print("Filesystem extracted")

def main(argv):
    file = open(argv[1], "rb")
    sentinel_string = b"<nexe~~sentinel>"
    file.seek(-16 - len(sentinel_string), 2) # Seek to end
    check_string = file.read(len(sentinel_string))
    if(sentinel_string == check_string):
        print("File is compiled with nexe")

        code_size = int(struct.unpack("<d", file.read(8))[0])
        bundle_size = int(struct.unpack("<d", file.read(8))[0])

        print("Code size: ", code_size)
        print("Bundle size: ", bundle_size)

        separate(file, code_size, bundle_size, len(sentinel_string) + 16)

if __name__ == "__main__":
    import sys
    main(sys.argv)