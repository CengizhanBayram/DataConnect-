import sqlite3

class DataConnect:
    def __init__(self, db_name) -> str:
        """
        DataConnect sınıfı için yapıcı metot.
        
        :param db_name: Veritabanı dosyasının adı veya yolunu içeren bir string.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    def connect(self) -> None:
        """
        Veritabanına bağlanmak için kullanılan metot.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Bağlantı başarılı!")
        except sqlite3.Error as e:
            print("Bağlantı hatası:", e)
    def disconnect(self) -> None:
        """
        Veritabanı bağlantısını kapatmak için kullanılan metot.
        """
        if self.connection:
            self.connection.close()
            print("Bağlantı kapatıldı.")
