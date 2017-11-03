with open("./helpers/animes", encoding="utf-8") as file_reader:
    with open("./helpers/recovered_animes", "w", encoding="utf-8") as file_writer:
        lines = file_reader.read().splitlines()
        count = 0
        for line in lines:
            count += 1
            print("line", line)
            number = line.split(",")[0]
            while count < int(number):
                print("count", count)
                file_writer.write(f"{count},dne\n")
                count += 1
