import abc

class Decryptor(abc.ABC):
    @abc.abstractmethod
    def Decrypt(self):
        """Base method."""
    
    @abc.abstractmethod
    def GetBrowser(self):
        """Browser name getter."""