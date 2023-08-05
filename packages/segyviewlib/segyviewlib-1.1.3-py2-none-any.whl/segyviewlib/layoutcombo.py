from PyQt4.QtCore import Qt, pyqtSignal, QVariant
from PyQt4.QtGui import QComboBox, QIcon

from segyviewlib import resource_icon


class LayoutCombo(QComboBox):
    layout_changed = pyqtSignal(object)

    DEFAULT_LARGE_FILE_LAYOUT = 4
    DEFAULT_SMALL_FILE_LAYOUT = 2

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)

        layouts = [
            # {
            #     "icon": "layouts_four_grid.png",
            #     "spec": {
            #         "dims": (2, 2),
            #         "grid": [(0, 0), (0, 1), (1, 0), (1, 1)]
            #     }
            # },
            {
                "icon": "layouts_three_bottom_grid.png",
                "spec": {
                    "dims": (2, 2),
                    "grid": [(0, 0), (0, 1), (1, slice(0, 2))]
                }
            },
            {
                "icon": "layouts_three_top_grid.png",
                "spec": {
                    "dims": (2, 2),
                    "grid": [(0, slice(0, 2)), (1, 0), (1, 1)]
                }
            },
            {
                "icon": "layouts_three_left_grid.png",
                "spec": {
                    "dims": (2, 2),
                    "grid": [(slice(0, 2), 0), (0, 1), (1, 1)]
                }
            },
            {
                "icon": "layouts_three_right_grid.png",
                "spec": {
                    "dims": (2, 2),
                    "grid": [(0, 0), (1, 0), (slice(0, 2), 1)]
                }
            },
            {
                "icon": "layouts_two_horizontal_grid.png",
                "spec": {
                    "dims": (2, 1),
                    "grid": [(0, 0), (1, 0)]
                }
            },
            {
                "icon": "layouts_two_vertical_grid.png",
                "spec": {
                    "dims": (1, 2),
                    "grid": [(0, 0), (0, 1)]
                }
            },
            {
                "icon": "layouts_three_horizontal_grid.png",
                "spec": {
                    "dims": (3, 1),
                    "grid": [(0, 0), (1, 0), (2, 0)]
                }
            },
            {
                "icon": "layouts_three_vertical_grid.png",
                "spec": {
                    "dims": (1, 3),
                    "grid": [(0, 0), (0, 1), (0, 2)]
                }
            },
            {
                "icon": "layouts_single.png",
                "spec": {
                    "dims": (1, 1),
                    "grid": [(0, 0)]
                }
            }
        ]

        for layout in layouts:
            self.add_layout_item(layout)

        height = 30
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self.setMinimumWidth(60)
        self.setMaximumWidth(60)

        self.currentIndexChanged.connect(self._layout_changed)

    def add_layout_item(self, layout_item):
        self.addItem(resource_icon(layout_item['icon']), "", layout_item['spec'])

    def _layout_changed(self, index):
        spec = self._get_spec(index)
        self.layout_changed.emit(spec)

    def _get_spec(self, index):
        user_data = self.itemData(index)
        """ :type: QVariant"""
        spec = user_data.toPyObject()
        return {str(key): value for key, value in spec.items()}

    def get_current_layout(self):
        return self._get_spec(self.currentIndex())

    def __del__(self):
        self.currentIndexChanged.disconnect(self._layout_changed)

