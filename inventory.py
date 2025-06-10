from PyQt5 import QtWidgets, QtGui, QtCore
from supabase import create_client, Client

SUPABASE_URL = "https://qyeegnjmzfyyhecbjomm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5ZWVnbmptemZ5eWhlY2Jqb21tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkxOTcxNjEsImV4cCI6MjA2NDc3MzE2MX0.7s7bOszi1QX6X4mAFTOOenXYcFaus-7kAVhDmSAMirU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class AddProductCard(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("addProductCard")
        self.setFixedSize(600, 700)
        self.setGraphicsEffect(self.create_shadow())

        self.move(
            self.parent().width() // 2 - self.width() // 2,
            self.parent().height()
        )

        self.init_ui()

        self.animation = QtCore.QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.end_pos = QtCore.QPoint(
            self.parent().width() // 2 - self.width() // 2,
            self.parent().height() // 2 - self.height() // 2
        )
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self.end_pos)

        self.back_button.clicked.connect(self.close_card)

    def create_shadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        return shadow

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(20)

        header_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton("←")
        self.back_button.setFixedWidth(40)
        header_layout.addWidget(self.back_button)

        title = QtWidgets.QLabel("Add Product")
        title.setObjectName("cardTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)

        self.entries = {}
        self.supplier_map = {}

        fields = {
            "productname": "Product Name",
            "description": "Description",
            "price": "Price",
            "cost": "Cost",
            "currentstock": "Current Stock",
            "reorderpoint": "Reorder Point",
            "age": "Age (months)",
            "supplier": "Supplier"
        }

        for key, label in fields.items():
            if key == "supplier":
                combo = QtWidgets.QComboBox()
                try:
                    response = supabase.table("suppliers").select("supplierid,suppliername").execute()
                    for supplier in response.data or []:
                        combo.addItem(supplier["suppliername"])
                        self.supplier_map[supplier["suppliername"]] = supplier["supplierid"]
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load suppliers:\n{e}")
                self.entries[key] = {"entry": combo}
                form_layout.addRow(label, combo)
            else:
                line = QtWidgets.QLineEdit()
                self.entries[key] = line
                form_layout.addRow(label, line)

        layout.addLayout(form_layout)

        save_btn = QtWidgets.QPushButton("Save Product")
        save_btn.setObjectName("saveProductButton")
        save_btn.clicked.connect(self.save_product)
        layout.addWidget(save_btn)

    def showEvent(self, event):
        super().showEvent(event)
        self.animation.start()

    def close_card(self):
        self.hide()

    def save_product(self):
        try:
            data = {}
            for key, entry in self.entries.items():
                if key == "supplier":
                    selected = entry["entry"].currentText()
                    if not selected:
                        QtWidgets.QMessageBox.warning(self, "Missing", "Please select a supplier.")
                        return
                    data["supplierid"] = self.supplier_map[selected]
                else:
                    data[key] = entry.text().strip()

            for field in ["price", "cost"]:
                data[field] = float(data.get(field, 0.0))

            for field in ["currentstock", "reorderpoint", "age"]:
                data[field] = int(data.get(field, 0))

            response = supabase.table("products").insert(data).execute()
            if response.data:
                QtWidgets.QMessageBox.information(self, "Success", "Product saved successfully.")
                self.hide()
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "Insert failed.")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BuiswAIz")
        self.setGeometry(100, 100, 1280, 720)

        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("style.qss not found")

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.addLayout(self.create_sidebar(), 1)

        self.main_content = self.create_main_content()
        main_layout.addLayout(self.main_content, 4)

        self.populate_data()

    def create_sidebar(self):
        layout = QtWidgets.QVBoxLayout()
        buttons = ["Dashboard", "Inventory", "Sales", "Expense", "Assistant"]
        for name in buttons:
            btn = QtWidgets.QPushButton(name)
            btn.setObjectName("sidebarButton")
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            if name == "Inventory":
                btn.setChecked(True)
            btn.clicked.connect(lambda _, n=name: self.on_sidebar_click(n))
            layout.addWidget(btn)
        layout.addStretch()
        return layout

    def create_main_content(self):
        layout = QtWidgets.QVBoxLayout()

        top_bar = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Inventory")
        label.setFont(QtGui.QFont("Montserrat", 15, QtGui.QFont.Bold))
        top_bar.addWidget(label)

        top_bar.addStretch()

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.search_input.setFixedWidth(300)
        self.search_input.setObjectName("searchInput")
        top_bar.addWidget(self.search_input)

        add_btn = QtWidgets.QPushButton("Add New Product")
        add_btn.setObjectName("addProductButton")
        add_btn.clicked.connect(self.open_add_product_window)
        top_bar.addWidget(add_btn)
        layout.addLayout(top_bar)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Code", "ProductName", "Description", "Price", "Cost", "Quantity",
            "Reorder", "Age", "Supplier", "CreatedAt"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        return layout

    def on_sidebar_click(self, name):
        if name == "Inventory":
            self.populate_data()
        else:
            QtWidgets.QMessageBox.information(self, "Info", f"{name} clicked — feature coming soon!")

    def populate_data(self):
        self.table.setRowCount(0)
        try:
            products = supabase.table("products").select("*").execute().data
            suppliers = supabase.table("suppliers").select("supplierid,suppliername").execute().data
            supplier_map = {s["supplierid"]: s["suppliername"] for s in suppliers}

            for row in products:
                current_row = self.table.rowCount()
                self.table.insertRow(current_row)
                values = [
                    row.get("productid", ""),
                    row.get("productname", ""),
                    row.get("description", ""),
                    f"₱{row.get('price', 0):,.2f}",
                    f"₱{row.get('cost', 0):,.2f}",
                    str(row.get("currentstock", "")),
                    str(row.get("reorderpoint", "")),
                    f"{row.get('age', '')} mo",
                    supplier_map.get(row.get("supplierid"), row.get("supplierid")),
                    str(row.get("createdat", ""))
                ]
                for col, val in enumerate(values):
                    item = QtWidgets.QTableWidgetItem(val)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.table.setItem(current_row, col, item)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    def open_add_product_window(self):
        self.card = AddProductCard(self)
        self.card.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
