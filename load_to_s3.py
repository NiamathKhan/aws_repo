from csv_json_parser import File_Parser
from pip_data import Create_Bucket


class Main(object):
    def __init__(self):
        super().__init__()

    def main(self):
        __input_file, __output_file = input(f"please enter input and output file paths seperated by , \n").split(",")
        file_parser = File_Parser(inputfile=__input_file, outputfile=__output_file)
        __data = file_parser.read_as_csv()
        ret_val = file_parser.write_as_json(data=__data)
        if ret_val:
            __bucket_name = input(f"please enter bucket name \n")
            create_bucket = Create_Bucket(bucketname=__bucket_name, objectname=__output_file)
            ret_val = create_bucket.create_bucket()
            print(f"ret_val for create bucket is {ret_val}")
            if ret_val:
                print("bucket created !")
                ret_val = create_bucket.upload_object()
                if not ret_val:
                    print("object upload filed")
            else:
                print("bucket creation filed !")
        else:
            print("job filed !")


if __name__ == "__main__":
    main = Main()
    main.main()
