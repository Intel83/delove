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
    __SIZEMIN = (600, 250)
    __SIZEMAX = (1000, 1000)
    __EXIT = "Wyjście"
    __OWN_DB = "Załaduj własny magazyn z pliku."
    __SUPPLIER_LABEL = "Wybierz dostawcę:"
    __PARSE_STORE = "Załaduj magazyn dostawcy"
    __LOAD_SUPPLIER = "Aktualizuj swój magazyn"
    __SAVE_FILE = "Zapisz magazyn"
    __SUPPLIERS = {
        "Bielizna Centrum": bc.BC(),
        "Boss of Toys": bot.Boss(),
        "Obsessive": obs.Obsessive(),
        "Orion": ori.Orion(),
        "Livco": liv.Livco()
    }
    __database = None

    def __init__(self, title):
        self.__database = Store()
        self.__supplier_store = Supplier()

        wx.Frame.__init__(
            self,
            None,
            title=title,
            size=self.__SIZEMIN
        )

        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(
            wx.ID_EXIT,
            "E&xit\tAlt-X",
            self.__EXIT
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
            self.__EXIT
        )
        m_close.Bind(wx.EVT_BUTTON, self.__on_exit)

        vs1 = wx.BoxSizer(wx.VERTICAL)
        hsizers = []

        # Horizontal Sizer 1
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # ladowanie bazy danych
        self.__button_load_own_store = wx.Button(
            panel,
            1,
            self.__OWN_DB
        )
        self.__db_label = wx.StaticText(
            panel,
            label=""
        )
        self.__button_load_own_store.Bind(
            wx.EVT_BUTTON,
            self.__load_own_store
        )
        hs.Add(
            self.__button_load_own_store,
            0,
            wx.LEFT,
            10
        )
        hs.Add(
            self.__db_label,
            0,
            wx.LEFT
        )
        hsizers.append(hs)

        # Horizontal Sizer 2
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # wybor dostawcy
        supplier_label = wx.StaticText(
            panel,
            label=self.__SUPPLIER_LABEL
        )
        supplier_combo = wx.ComboBox(
            panel,
            choices=[keys for keys in self.__SUPPLIERS.keys()],
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

        # Horizontal Sizer 3
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # czytanie magazynu dostawcy
        self.__button_read_store = wx.Button(
            panel,
            1,
            self.__PARSE_STORE
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

        # Horizontal Sizer 4
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # ładowanie magazynu dostawcy do swojego magazynu
        self.__button_load_supplier = wx.Button(
            panel,
            1,
            self.__LOAD_SUPPLIER
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

        # Horizontal Sizer 5
        hs = wx.BoxSizer(wx.HORIZONTAL)
        # zachowanie pliku magazyna
        self.__button_save_store = wx.Button(
            panel,
            1,
            self.__SAVE_FILE
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
        panel.SetMinSize(self.__SIZEMIN)
        panel.SetMaxSize(self.__SIZEMAX)
        # panel.Layout()
        # panel.Show(True)

    def __load_own_store(self, event):
        dialog = wx.FileDialog(
            self,
            "Open",
            os.getcwd(),
            "",
            "Pliki bazy danych (*.xml)|*.xml",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        dialog.ShowModal()
        path = dialog.GetPath()
        dialog.Destroy()
        self.__db_label.SetLabel(path)
        self.__database.load_store_from_file(path)
        self.__button_save_store.Enable()

    def __select_supplier(self, event):
        item = tuple(self.__SUPPLIERS.keys())[event.GetSelection()]
        if item:
            self.__supplier_store = self.__SUPPLIERS[item]
            self.__button_read_store.Enable()

    def __parse_supplier(self, event):
        dialog = wx.FileDialog(
            self,
            "Open",
            os.getcwd(),
            "",
            "Pliki dostawców (*.{0})|*.{0}".format(self.__supplier_store.FILETYPE),
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        dialog.ShowModal()
        try:
            self.__supplier_store.load(dialog.GetPath())
        except IOError:
            print("Błąd ładowania pliku dostawcy")
        finally:
            dialog.Destroy()
            if self.__supplier_store.test_store():
                self.__button_load_supplier.Enable()

    def __load_supplier_into_database(self, event):
        self.__database.load_supplier(self.__supplier_store)
        self.__button_save_store.Enable()

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

    def __on_exit(self, event):
        self.Close(True)
