import base64
import timer
import os

class fileOnA85():
    """Encode your file using A85 algorithm
    How to use ??
    It's so simple:
    import fileCrypto
	myfile = fileCrypto.fileOnBase16("exemple.jpg")
	myfile.encode() #This Methode To Encode The File
	myfile.decode() #This Methode To Decode the File
	#Encryption And Decryption of File Was Never Easy Than Before
    """

    def __init__(self,path,extension=".filecrypto"):
        self.path = str(path)
        self.extension = str(extension)

    def encode(self,timerPrinting=False):
        """To Give The Order To Encode The File"""
        t = time.time()
        if self.extension not in self.path:
            # Encoding The file data
            with open(self.path,"rb") as f:
                file_data = f.read()
            self.encoded = base64.a85encode(file_data)

            # Create the encoder file
            with open(self.path + self.extension,"wb") as f:
                f.write(file_data)

            # Delete the file
            os.remove(self.path)
            if timerPrinting:
                print("Done in "+str(time.time() - t))
        else:
            print("File is already encoded")

    def decoded(self,timerPrinting=False):
        """To Give The Order To Decode The File"""
        t = time.time()
        if self.extension in self.path:
            # Decoding the file data$
            with open(self.path,"rb") as f:
                file_data = f.read()
            self.decoded = base64.a85decode(file_data)

            # Create the decoded file
            self.path2 = self.path.replace(self.extension,"")
            with open(self.path2,"wb") as f:
                f.write(self.decoded)

            # Delete the main file
            os.remove(self.path)

            if timerPrinting:
                print("Done in "+str(time.time() - t))
        else:
            print("The file is not encoded to decoded")
