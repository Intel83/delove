import os
import wx
# import database
# from redcart import products
from store_own.product_own import Product
from supplier import obsessive as obs
from supplier import bielizna_centrum as bc
from supplier import orion as ori
from supplier import boss_of_toys as bot
from supplier import livco as liv


class MainWindow(wx.Frame):
    __SIZEMIN = (600, 200)
    __SIZEMAX = (1000, 1000)
    __EXIT = "Wyjscie"
    __OWN_DB = "Zaladuj wlasny magazyn"
    __SUPPLIER_LABEL = "Wybierz dostawce:"
    __PARSE_STORE = "Zaladuj magazyn dostawcy"
    __SUPPLIERS = {
        "Bielizna Centrum": bc.BC(),
        "Boss of Toys": bot.Boss(),
        "Obsessive": obs.Obsessive(),
        "Orion": ori.Orion(),
        "Livco": liv.Livco()
    }
    __database = list()

    def __init__(self, title):
        self.__database = None
        self.__supplier_store = None

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
        # hs = wx.BoxSizer(wx.HORIZONTAL)
        # ladowanie bazy danych
        # db_button = wx.Button(
        #     panel,
        #     1,
        #     self.__OWN_DB
        # )
        # self.__db_label = wx.StaticText(
        #     panel,
        #     label=""
        # )
        # db_button.Bind(
        #     wx.EVT_BUTTON,
        #     self.__load_db
        # )
        # hs.Add(
        #     db_button,
        #     0,
        #     wx.LEFT,
        #     10
        # )
        # hs.Add(
        #     self.__db_label,
        #     0,
        #     wx.LEFT
        # )
        # hsizers.append(hs)

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
        # ladowanie magazynu dostawcy
        self.__parse_store_button = wx.Button(
            panel,
            1,
            self.__PARSE_STORE
        )
        self.__parse_store_button.Bind(
            wx.EVT_BUTTON,
            self.__parse_supplier
        )
        hs.Add(
            self.__parse_store_button,
            0,
            wx.LEFT,
            10
        )
        self.__parse_store_button.Disable()
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

    # def __load_db(self, event):
    #     dialog = wx.FileDialog(
    #         self,
    #         "Open",
    #         os.getcwd(),
    #         "",
    #         "Pliki bazy danych (*.csv)|*.csv",
    #         wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    #     )
    #     dialog.ShowModal()
    #     path = dialog.GetPath()
    #     dialog.Destroy()
    #     self.__db_label.SetLabel(path)
    #     self.__database = database.Database(path)

    def __select_supplier(self, event):
        item = tuple(self.__SUPPLIERS.keys())[event.GetSelection()]
        if item:
            self.__supplier_store = self.__SUPPLIERS[item]
            self.__parse_store_button.Enable()

    def __parse_supplier(self, event):
        dialog = wx.FileDialog(
            self,
            "Open",
            os.getcwd(),
            "",
            "Pliki dostawcow (*.{0})|*.{0}".format(self.__supplier_store.FILETYPE),
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        dialog.ShowModal()
        try:
            self.__supplier_store.load(dialog.GetPath())
        except IOError:
            print("Blad ladowania pliku dostawcy")
        finally:
            dialog.Destroy()
            if self.__supplier_store.test_store():
                c_map = self.__supplier_store.get_conv_map()
                for prod_ean, prod_fields in self.__supplier_store.get_store().items():
                    code = "{}-{}".format(self.__supplier_store.get_prefix(), prod_fields[c_map[0]])
                    ean = prod_fields[c_map[1]]
                    is_available = prod_fields[c_map[2]]
                    quant = "100" if is_available else "0"
                    avail = "Dostępny" if is_available else "Zapytaj o dostępność"
                    date = "Do 7 dni" if is_available else "Brak informacji"
                    self.__database += Product(code, ean, quant, avail, date)

    def __on_exit(self, event):
        self.Close(True)
