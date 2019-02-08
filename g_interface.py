import os
import wx
from store_own.database_own import Store
from supplier.supplier import Supplier
from supplier import obsessive as obs
from supplier import bielizna_centrum as bc
from supplier import orion as ori
from supplier import boss_of_toys as bot
from supplier import livco as liv


class MainWindow(wx.Frame):
    __sizemin = (600, 300)
    __sizemax = (1000, 1000)
    __exit = "Wyjście."
    __download_db = "Ściągnij własny magazyn z bazy danych."
    __supplier_label = "Wybierz dostawcę:"
    __download_supplier = "Ściągnij magazyn z serwera dostawcy."
    __parse_store = "Wczytaj magazyn dostawcy."
    __load_supplier = "Aktualizuj swój magazyn danymi od dostawcy."
    __save_current_store = "Zapisz swój magazyn do pliku xml."
    __save_new_products_caption = "Zapisz nowe produkty do pliku xml."
    __suppliers = {
        # "Bielizna Centrum": bc.BC(),
        "Boss of Toys": bot.Boss(),
        # "Obsessive": obs.Obsessive(),
        "Orion": ori.Orion(),
        # "Livco": liv.Livco()
    }
    __database = None
    __own_store_loaded = False
    __supplier_store_loaded = False

    def __init__(self, title):
        self.__database = Store()
        self.__supplier_store = Supplier()

        wx.Frame.__init__(
            self,
            None,
            title=title,
            size=self.__sizemin
        )

        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(
            wx.ID_EXIT,
            "E&xit\tAlt-X",
            self.__exit
        )
        self.Bind(
            wx.EVT_MENU,
            self.__on_exit,
            m_exit
        )
        menu_bar.Append(menu, "&File")
        menu = wx.Menu()
        menu_bar.Append(menu, "&Help")
        self.SetMenuBar(menu_bar)
        self.status_bar = self.CreateStatusBar()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        m_close = wx.Button(
            panel,
            wx.ID_CLOSE,
            self.__exit
        )
        m_close.Bind(wx.EVT_BUTTON, self.__on_exit)

        vs1 = wx.BoxSizer(wx.VERTICAL)
        hsizers = []

        # Przycisk ściągnięcia swojego magazynu
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # ladowanie bazy danych
        self.__button_get_own_database = wx.Button(
            panel,
            1,
            self.__download_db
        )
        self.__button_get_own_database.Bind(
            wx.EVT_BUTTON,
            self.__get_own_db
        )
        hs.Add(
            self.__button_get_own_database,
            0,
            wx.LEFT,
            10
        )
        hsizers.append(hs)

        # Przycisk zachowania pliku swojego magazynu
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # zachowanie pliku magazyna
        self.__button_save_store = wx.Button(
            panel,
            1,
            self.__save_current_store
        )
        self.__button_save_store.Bind(
            wx.EVT_BUTTON,
            self.__save_store
        )
        hs.Add(
            self.__button_save_store,
            0,
            wx.LEFT,
            10
        )
        self.__button_save_store.Disable()
        hsizers.append(hs)

        # Lista dostawców
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # wybor dostawcy
        supplier_label = wx.StaticText(
            panel,
            label=self.__supplier_label
        )
        supplier_combo = wx.ComboBox(
            panel,
            choices=[keys for keys in self.__suppliers.keys()],
            style=wx.CB_READONLY
        )
        supplier_combo.Bind(wx.EVT_COMBOBOX, self.__select_supplier)
        hs.Add(
            supplier_label,
            0,
            wx.LEFT,
            10
        )
        hs.Add(
            supplier_combo,
            0,
            wx.LEFT,
            10
        )
        hsizers.append(hs)

        # Przycisk ściągania pilku dostawcy
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # ściąganie magazynu dostawcy
        self.__button_download_supplier_store = wx.Button(
            panel,
            1,
            self.__download_supplier
        )
        self.__button_download_supplier_store.Bind(
            wx.EVT_BUTTON,
            self.__download_supplier_store
        )
        hs.Add(
            self.__button_download_supplier_store,
            0,
            wx.LEFT,
            10
        )
        self.__button_download_supplier_store.Disable()
        hsizers.append(hs)

        # Przycisk czytania pilku dostawcy
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # czytanie magazynu dostawcy
        self.__button_read_store = wx.Button(
            panel,
            1,
            self.__parse_store
        )
        self.__button_read_store.Bind(
            wx.EVT_BUTTON,
            self.__parse_supplier
        )
        hs.Add(
            self.__button_read_store,
            0,
            wx.LEFT,
            10
        )
        self.__button_read_store.Disable()
        hsizers.append(hs)

        # Przycisk aktualizacji swojego magazynu
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # ładowanie magazynu dostawcy do swojego magazynu
        self.__button_load_supplier = wx.Button(
            panel,
            1,
            self.__load_supplier
        )
        self.__button_load_supplier.Bind(
            wx.EVT_BUTTON,
            self.__load_supplier_into_database
        )
        hs.Add(
            self.__button_load_supplier,
            0,
            wx.LEFT,
            10
        )
        self.__button_load_supplier.Disable()
        hsizers.append(hs)

        # Przycisk zachowania pliku nowych produktów
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # zachowanie pliku magazyna
        self.__button_save_new_products = wx.Button(
            panel,
            1,
            self.__save_new_products_caption
        )
        self.__button_save_new_products.Bind(
            wx.EVT_BUTTON,
            self.__save_new_products
        )
        hs.Add(
            self.__button_save_new_products,
            0,
            wx.LEFT,
            10
        )
        self.__button_save_new_products.Disable()
        hsizers.append(hs)

        for sizer in hsizers:
            vs1.Add(sizer)
        box.Add(
            vs1,
            1,
            wx.EXPAND
        )
        box.Add(
            m_close,
            0,
            wx.LEFT,
            10
        )

        panel.SetSizer(box)
        panel.SetMinSize(self.__sizemin)
        panel.SetMaxSize(self.__sizemax)
        # panel.Layout()
        # panel.Show(True)

    def __get_own_db(self, event):
        self.__button_save_store.Disable()
        self.__database.void_main_store()
        self.__database.download_own_store()
        self.__button_save_store.Enable()
        self.__own_store_loaded = True

    def __select_supplier(self, event):
        item = tuple(self.__suppliers.keys())[event.GetSelection()]
        try:
            if len(self.__supplier_store):
                self.__supplier_store.void_store()
                self.__button_load_supplier.Disable()
                self.__button_save_new_products.Disable()
        except AttributeError:
            self.__button_load_supplier.Disable()
        if item:
            self.__supplier_store = self.__suppliers[item]
            self.__button_download_supplier_store.Enable()
            self.__button_read_store.Enable()

    def __download_supplier_store(self, event):
        self.__supplier_store.download_store_xml()

    def __parse_supplier(self, event):
        dialog = wx.FileDialog(
            self,
            "Open",
            os.getcwd(),
            "",
            "Pliki dostawców (*.{0})|*.{0}".format(self.__supplier_store.filetype),
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        dialog.ShowModal()
        try:
            self.__supplier_store.load(dialog.GetPath())
            if self.__supplier_store.test_store():
                self.__button_load_supplier.Enable()
        except IOError:
            print("Błąd ładowania pliku dostawcy.")
        except AssertionError:
            print("Nie wybrano pliku dostawcy.")
        finally:
            dialog.Destroy()

    def __load_supplier_into_database(self, event):
        self.__database.load_supplier(self.__supplier_store)
        if self.__own_store_loaded:
            self.__button_save_store.Enable()
        self.__button_save_new_products.Enable()

    def __save_store(self, event):
        with wx.FileDialog(
            self,
            "Zachowaj plik magazynu",
            os.getcwd(),
            "",
            "Pliki XML (*.xml)|*.xml",
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.__database.dump_store_to_xml(file_dialog.GetPath())

    def __save_new_products(self, event):
        with wx.FileDialog(
            self,
            "Zachowaj nowe produkty.",
            os.getcwd(),
            "",
            "Pliki XML (*.xml)|*.xml",
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.__database.dump_store_to_xml(file_dialog.GetPath(), True)

    def __on_exit(self, event):
        self.Close(True)
