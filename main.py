import os
import wx
import sys
import g_interface as gi
Files_directory = os.path.join(os.getcwd(), "test_input")
# Database_file = "BAZA_DANYCH.csv"
# Obsessive_file = "obsessive.xls"
# BC_file = "bielizna_centrum_test.xml"


def main():
    app = wx.App(redirect=False)
    frame = gi.MainWindow("Delove.pl - automat magazynowy")
    frame.Show()
    app.MainLoop()
    # db = database.Database(os.path.join(Files_directory, Database_file))
    # store_obs = obs.Obsessive(os.path.join(Files_directory, Obsessive_file))
    # store_bc = bc.BC(os.path.join(Files_directory, BC_file))
    #
    # products_object = products.Product()
    # products_object.count()
    # nprods = products_object.result
    # products_object.get_products()
    # result = products_object.result

    sys.exit()


if __name__ == '__main__':
    main()
