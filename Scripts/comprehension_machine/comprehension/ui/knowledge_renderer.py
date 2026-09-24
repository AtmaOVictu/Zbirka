"""
Knowledge Renderer — TAZV Comprehension Machine
=================================================
Renders indexed knowledge as interactive mandala + text + sacred geometry.

Uses:
  - QPainter for mandala visualization (7 base modules + tradition rings)
  - QTextBrowser for cross-system reference display
  - corpus-validated colors from egyptian_color_semantics
  - corpus-validated frequencies from tonos

Sacred Geometry Visualizations:
  - Mandala: Base 7 modules + tradition rings
  - Torus: Flow and transformation
  - Yggdrasil: Tree of Life (Nordic)
  - Flower: Flower of Life pattern
  - SriYantra: Sri Yantra geometry

Architecture note: This file imports from the EXISTING modules:
  - egyptian_color_semantics (for colors)
  - module_semantics (for module definitions)
  - tonos (for sound frequencies)
  - rozetni_kamni (for tradition mappings)

It does NOT duplicate these. It renders what they hold.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QLabel, 
                               QComboBox, QStackedWidget, QPushButton)
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PyQt6.QtCore import Qt, QPointF, QRectF, QSize
import math
import json

# For PyQt6: Alignment flags are in Qt.AlignmentFlag
from PyQt6.QtCore import Qt

try:
    from comprehension.core.egyptian_color_semantics import COLORS, MODULE_COLOR_HEX
    from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
    from comprehension.core.tonos import TONOS_FREQUENCIES, get_frequency, get_note
    from comprehension.core.rozetni_kamni import TRADITIONS, get_cross_references
except ImportError:
    # Fallback for standalone testing
    COLORS = {}
    MODULE_COLOR_HEX = {}
    MODULE_SEMANTICS = {}
    MODULE_ORDER = ["bios", "state", "uaf", "jewik", "apd", "micro", "visualization"]
    TONOS_FREQUENCIES = {}
    TRADITIONS = {}


class MandalaView(QWidget):
    """Renders the base 7 modules + tradition rings as a mandala."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 600)
        self.selected_tradition = None
        self.selected_operator = None
        self.depth = 1  # \u2202 Globina level (1-4)

    def set_tradition(self, tradition_name):
        self.selected_tradition = tradition_name
        self.update()

    def set_depth(self, depth):
        self.depth = depth
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor("#0A0A0A"))

        # Center (the root \u2205)
        painter.setBrush(QColor("#1B2838"))
        painter.setPen(QPen(QColor("#333"), 1))
        center_r = 30 + (self.depth * 5)
        painter.drawEllipse(QPointF(cx, cy), center_r, center_r)
        painter.setPen(QColor("#E0E0E0"))
        painter.drawText(QRectF(cx - 20, cy - 8, 40, 16), Qt.AlignmentFlag.AlignCenter, "\u2205")

        # Base 7 modules in inner ring
        base_radius = 120
        for i, mod_name in enumerate(MODULE_ORDER):
            angle = (2 * math.pi * i / 7) - math.pi / 2  # start at top
            x = cx + base_radius * math.cos(angle)
            y = cy + base_radius * math.sin(angle)

            mod = MODULE_SEMANTICS.get(mod_name, {})
            color_hex = MODULE_COLOR_HEX.get(mod_name, "#444444")
            glyph = mod.get("symbol", "?")

            # Module circle
            r = 25 + (self.depth * 2)
            painter.setBrush(QColor(color_hex))
            painter.setPen(QPen(QColor("#333"), 1))
            painter.drawEllipse(QPointF(x, y), r, r)

            # Glyph
            painter.setPen(QColor("#E0E0E0"))
            painter.drawText(QRectF(x - 15, y - 8, 30, 16), Qt.AlignmentFlag.AlignCenter, glyph)

            # Connection line to center
            painter.setPen(QPen(QColor("#222"), 1))
            painter.drawLine(QPointF(cx, cy), QPointF(x, y))

        # Tradition rings (outer)
        if self.selected_tradition:
            trad = TRADITIONS.get(self.selected_tradition, {})
            ring_num = trad.get("ring", 1)
            mappings = trad.get("mappings", {})

            ring_radius = 200 + (ring_num * 50)
            items = list(mappings.items())

            for i, (native_term, (root_op, math_prop)) in enumerate(items):
                angle = (2 * math.pi * i / max(len(items), 1)) - math.pi / 2
                x = cx + ring_radius * math.cos(angle)
                y = cy + ring_radius * math.sin(angle)

                # Find color for this root operator
                color_hex = "#666666"
                for mod_name, mod in MODULE_SEMANTICS.items():
                    if mod.get("symbol") == root_op:
                        color_hex = MODULE_COLOR_HEX.get(mod_name, "#666666")
                        break

                # Tradition node
                painter.setBrush(QColor(color_hex))
                painter.setPen(QPen(QColor("#555"), 1))
                painter.drawEllipse(QPointF(x, y), 20, 20)

                # Label
                painter.setPen(QColor("#E0E0E0"))
                label = native_term.split("(")[0].strip()[:12]
                painter.setFont(QFont("Consolas", 7))
                painter.drawText(
                    QRectF(x - 40, y + 22, 80, 14),
                    Qt.AlignmentFlag.AlignCenter, label
                )

                # Connection to corresponding base module
                for j, mod_name in enumerate(MODULE_ORDER):
                    mod = MODULE_SEMANTICS.get(mod_name, {})
                    if mod.get("symbol") == root_op:
                        base_angle = (2 * math.pi * j / 7) - math.pi / 2
                        bx = cx + base_radius * math.cos(base_angle)
                        by = cy + base_radius * math.sin(base_angle)
                        painter.setPen(QPen(QColor("#333"), 1, Qt.DashLine))
                        painter.drawLine(QPointF(x, y), QPointF(bx, by))
                        break

        painter.end()


# ── Sacred Geometry Views ──

class TorusView(QWidget):
    """Renders a torus as a representation of flow and transformation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 600)
        self.rotation = 0
        self.highlight_module = None

    def set_highlight(self, symbol):
        """Highlight a specific module/operator."""
        self.highlight_module = symbol
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor("#0A0A0A"))

        # Torus parameters
        major_radius = min(w, h) * 0.35
        minor_radius = major_radius * 0.3

        # Draw torus as a series of circles
        num_tubes = 36
        for i in range(num_tubes):
            angle = (2 * math.pi * i / num_tubes) + self.rotation
            tx = cx + major_radius * math.cos(angle)
            ty = cy + major_radius * math.sin(angle)

            # Get color based on module order
            color_idx = i % len(MODULE_ORDER)
            mod_name = MODULE_ORDER[color_idx]
            color_hex = MODULE_COLOR_HEX.get(mod_name, "#666666")

            # Highlight if this is the selected module
            mod = MODULE_SEMANTICS.get(mod_name, {})
            if self.highlight_module and mod.get("symbol") == self.highlight_module:
                painter.setBrush(QColor("#FFD700"))  # Gold highlight
            else:
                painter.setBrush(QColor(color_hex))

            painter.setPen(QPen(QColor("#333"), 1))
            painter.drawEllipse(QPointF(tx, ty), minor_radius, minor_radius)

            # Draw glyph
            glyph = mod.get("symbol", "?")
            painter.setPen(QColor("#E0E0E0"))
            painter.drawText(QRectF(tx - 12, ty - 8, 24, 16), Qt.AlignmentFlag.AlignCenter, glyph)

        # Draw central axis
        painter.setPen(QPen(QColor("#555"), 2))
        painter.drawLine(QPointF(cx, cy - major_radius * 1.2), 
                        QPointF(cx, cy + major_radius * 1.2))
        painter.drawLine(QPointF(cx - major_radius * 1.2, cy),
                        QPointF(cx + major_radius * 1.2, cy))

        # Label
        painter.setPen(QColor("#E0E0E0"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(QRectF(10, 10, w - 20, 20), Qt.AlignmentFlag.AlignLeft, "Torus: Flow & Transformation")
        painter.end()


class YggdrasilView(QWidget):
    """Renders Yggdrasil (Nordic Tree of Life) with 9 worlds."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 600)
        self.highlight_world = None

    def set_highlight(self, symbol):
        """Highlight a specific world based on symbol."""
        self.highlight_world = symbol
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor("#0A0A0A"))

        # Yggdrasil structure
        trunk_width = 20
        root_spread = 150
        crown_spread = 120
        branch_height = 180

        # Draw roots (3 roots)
        painter.setBrush(QColor("#553311"))
        painter.setPen(QPen(QColor("#332211"), 2))
        for i in range(3):
            angle = (2 * math.pi * i / 3) + math.pi / 6
            x1 = cx
            y1 = cy + 50
            x2 = cx + root_spread * math.cos(angle)
            y2 = cy + root_spread * math.sin(angle) + 80
            points = [QPointF(x1, y1), QPointF(x2, y2)]
            painter.drawPolyline(points)

        # Draw trunk
        painter.setBrush(QColor("#8B4513"))
        painter.setPen(QPen(QColor("#553311"), 2))
        painter.drawRect(QRectF(cx - trunk_width // 2, cy - 50, trunk_width, 100))

        # Draw branches (6 branches)
        for i in range(6):
            angle = (2 * math.pi * i / 6) - math.pi / 6
            x1 = cx
            y1 = cy - 50
            x2 = cx + branch_height * math.cos(angle)
            y2 = cy - branch_height * math.sin(angle) - 80
            points = [QPointF(x1, y1), QPointF(x2, y2)]
            painter.drawPolyline(points)

        # 9 Worlds positioning
        worlds = [
            ("Asgard", cx, cy - 200, "⟡", "#FFD700"),
            ("Vanaheim", cx + 80, cy - 150, "∮", "#ADFF2F"),
            ("Alfheim", cx + 120, cy - 80, "∂", "#90EE90"),
            ("Midgard", cx, cy, "⊥", "#00BFFF"),
            ("Jotunheim", cx - 120, cy - 80, "∅", "#800080"),
            ("Svartalfheim", cx - 80, cy - 150, "¬", "#696969"),
            ("Nidavellir", cx, cy + 80, "∆", "#FFA500"),
            ("Muspelheim", cx + 100, cy + 150, "⊢", "#FF4500"),
            ("Hel", cx - 100, cy + 150, "∅", "#000000"),
        ]

        # Draw worlds
        for name, x, y, symbol, color in worlds:
            # Check if this world's symbol should be highlighted
            is_highlighted = self.highlight_world and symbol == self.highlight_world

            if is_highlighted:
                painter.setBrush(QColor("#FFD700"))
            else:
                painter.setBrush(QColor(color))

            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawEllipse(QPointF(x, y), 25, 25)

            # Draw symbol
            painter.setPen(QColor("#E0E0E0"))
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            painter.drawText(QRectF(x - 15, y - 12, 30, 24), Qt.AlignmentFlag.AlignCenter, symbol)

            # Draw name
            painter.setPen(QColor("#E0E0E0"))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(QRectF(x - 40, y + 18, 80, 16), Qt.AlignmentFlag.AlignCenter, name)

        # Label
        painter.setPen(QColor("#E0E0E0"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(QRectF(10, 10, w - 20, 20), Qt.AlignmentFlag.AlignLeft, "Yggdrasil: 9 Worlds")
        painter.end()


class FlowerOfLifeView(QWidget):
    """Renders the Flower of Life sacred geometry pattern."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 600)
        self.depth = 3  # Number of layers
        self.highlight_center = False

    def set_depth(self, depth):
        """Set the number of layers to render."""
        self.depth = max(1, min(depth, 7))
        self.update()

    def set_highlight_center(self, highlight):
        """Highlight the center."""
        self.highlight_center = highlight
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor("#0A0A0A"))

        # Circle parameters
        circle_radius = min(w, h) * 0.25

        # Draw concentric circles
        painter.setPen(QPen(QColor("#444"), 1))
        for i in range(1, self.depth + 1):
            r = circle_radius * i / self.depth
            painter.drawEllipse(QPointF(cx, cy), r, r)

        # Draw Flower of Life pattern
        num_circles = 19  # 1 center + 6 + 12
        for i in range(num_circles):
            if i == 0:
                # Center
                angle = 0
                distance = 0
            elif i <= 6:
                # First ring
                angle = (2 * math.pi * (i - 1) / 6)
                distance = circle_radius * 2 / 3
            else:
                # Second ring
                angle = (2 * math.pi * (i - 7) / 12)
                distance = circle_radius * 4 / 3

            x = cx + distance * math.cos(angle)
            y = cy + distance * math.sin(angle)

            # Get color from module order
            color_idx = (i - 1) % len(MODULE_ORDER) if i > 0 else 0
            mod_name = MODULE_ORDER[color_idx]
            color_hex = MODULE_COLOR_HEX.get(mod_name, "#666666")

            # Highlight center
            if i == 0 and self.highlight_center:
                painter.setBrush(QColor("#FFD700"))
            else:
                painter.setBrush(QColor(color_hex))

            painter.setPen(QPen(QColor("#333"), 1))
            r = circle_radius / self.depth if i > 0 else circle_radius / self.depth * 1.5
            painter.drawEllipse(QPointF(x, y), r, r)

            # Draw glyph in center circle
            if i == 0:
                mod = MODULE_SEMANTICS.get(mod_name, {})
                glyph = mod.get("symbol", "∅")
                painter.setPen(QColor("#E0E0E0"))
                painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
                painter.drawText(QRectF(cx - 20, cy - 20, 40, 40), Qt.AlignmentFlag.AlignCenter, glyph)

        # Label
        painter.setPen(QColor("#E0E0E0"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(QRectF(10, 10, w - 20, 20), Qt.AlignmentFlag.AlignLeft, 
                        f"Flower of Life: {self.depth} layers")
        painter.end()


class SriYantraView(QWidget):
    """Renders Sri Yantra sacred geometry."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 600)
        self.level = 4  # Number of triangle layers
        self.highlight_symbol = None

    def set_level(self, level):
        """Set the number of triangle layers."""
        self.level = max(1, min(level, 9))
        self.update()

    def set_highlight(self, symbol):
        """Highlight a specific symbol."""
        self.highlight_symbol = symbol
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx, cy = w // 2, h // 2

        # Background
        painter.fillRect(0, 0, w, h, QColor("#0A0A0A"))

        # Sri Yantra parameters
        center_size = min(w, h) * 0.08
        triangle_height = min(w, h) * 0.3

        # Draw central bindu (point)
        painter.setBrush(QColor("#FFD700"))
        painter.setPen(QPen(QColor("#333"), 1))
        painter.drawEllipse(QPointF(cx, cy), center_size / 2, center_size / 2)

        # Draw overlapping triangles
        for layer in range(1, self.level + 1):
            # Upward triangles (Shakti - feminine)
            tri_height = triangle_height * layer / self.level
            tri_base = tri_height * 2 / math.sqrt(3)

            for i in range(3):
                angle = (2 * math.pi * i / 3)
                
                # Get color for this triangle
                color_idx = (layer + i - 1) % len(MODULE_ORDER)
                mod_name = MODULE_ORDER[color_idx]
                color_hex = MODULE_COLOR_HEX.get(mod_name, "#888888")

                # Highlight if matches
                if self.highlight_symbol:
                    mod = MODULE_SEMANTICS.get(mod_name, {})
                    if mod.get("symbol") == self.highlight_symbol:
                        color_hex = "#FFD700"

                painter.setBrush(QColor(color_hex))
                painter.setPen(QPen(QColor("#333"), 1))

                # Calculate triangle points (upward)
                top_x = cx + 0 * math.cos(angle) - tri_height * math.sin(angle)
                top_y = cy + 0 * math.sin(angle) + tri_height * math.cos(angle)
                
                bl_x = cx + tri_base / 2 * math.cos(angle) + tri_height / 2 * math.sin(angle)
                bl_y = cy + tri_base / 2 * math.sin(angle) - tri_height / 2 * math.cos(angle)
                
                br_x = cx - tri_base / 2 * math.cos(angle) + tri_height / 2 * math.sin(angle)
                br_y = cy - tri_base / 2 * math.sin(angle) - tri_height / 2 * math.cos(angle)

                points = [
                    QPointF(top_x, top_y),
                    QPointF(bl_x, bl_y),
                    QPointF(br_x, br_y)
                ]
                painter.drawPolygon(points)

            # Downward triangles (Shiva - masculine)
            for i in range(3):
                angle = (2 * math.pi * i / 3) + math.pi / 3
                
                color_idx = (layer + i + 3 - 1) % len(MODULE_ORDER)
                mod_name = MODULE_ORDER[color_idx]
                color_hex = MODULE_COLOR_HEX.get(mod_name, "#666666")

                # Highlight if matches
                if self.highlight_symbol:
                    mod = MODULE_SEMANTICS.get(mod_name, {})
                    if mod.get("symbol") == self.highlight_symbol:
                        color_hex = "#FFD700"

                painter.setBrush(QColor(color_hex))
                painter.setPen(QPen(QColor("#333"), 1))

                # Calculate triangle points (downward)
                top_x = cx + 0 * math.cos(angle) + tri_height * math.sin(angle)
                top_y = cy + 0 * math.sin(angle) - tri_height * math.cos(angle)
                
                bl_x = cx + tri_base / 2 * math.cos(angle) - tri_height / 2 * math.sin(angle)
                bl_y = cy + tri_base / 2 * math.sin(angle) + tri_height / 2 * math.cos(angle)
                
                br_x = cx - tri_base / 2 * math.cos(angle) - tri_height / 2 * math.sin(angle)
                br_y = cy - tri_base / 2 * math.sin(angle) + tri_height / 2 * math.cos(angle)

                points = [
                    QPointF(top_x, top_y),
                    QPointF(bl_x, bl_y),
                    QPointF(br_x, br_y)
                ]
                painter.drawPolygon(points)

        # Draw outer circle
        outer_radius = center_size + triangle_height * self.level / self.level * 1.2
        painter.setPen(QPen(QColor("#FFD700"), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), outer_radius, outer_radius)

        # Label
        painter.setPen(QColor("#E0E0E0"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(QRectF(10, 10, w - 20, 20), Qt.AlignmentFlag.AlignLeft, 
                        f"Sri Yantra: {self.level} levels")
        painter.end()


# ── Geometry Selector ──

class GeometrySelector(QWidget):
    """Widget to select and view different sacred geometries."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Geometry type selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Geometry:"))
        
        self.geometry_combo = QComboBox()
        self.geometry_names = [
            ("Mandala", "mandala"),
            ("Torus", "torus"),
            ("Yggdrasil", "yggdrasil"),
            ("Flower of Life", "flower"),
            ("Sri Yantra", "sriyantra"),
        ]
        for name, key in self.geometry_names:
            self.geometry_combo.addItem(name)
        self.geometry_combo.currentIndexChanged.connect(self._on_geometry_changed)
        selector_layout.addWidget(self.geometry_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)

        # Stacked widget for different geometries
        self.stack = QStackedWidget()
        
        # Create all geometry views
        self.mandala_view = MandalaView()
        self.torus_view = TorusView()
        self.yggdrasil_view = YggdrasilView()
        self.flower_view = FlowerOfLifeView()
        self.sriyantra_view = SriYantraView()
        
        self.stack.addWidget(self.mandala_view)
        self.stack.addWidget(self.torus_view)
        self.stack.addWidget(self.yggdrasil_view)
        self.stack.addWidget(self.flower_view)
        self.stack.addWidget(self.sriyantra_view)
        
        layout.addWidget(self.stack, stretch=1)
        
        # Tradition selector for Mandala
        self.tradition_selector = QHBoxLayout()
        self.tradition_selector.addWidget(QLabel("Tradition:"))
        self.tradition_combo = QComboBox()
        self.tradition_combo.addItem("(none)")
        for name in sorted(TRADITIONS.keys()):
            self.tradition_combo.addItem(name)
        self.tradition_combo.currentTextChanged.connect(self._on_tradition_changed)
        self.tradition_selector.addWidget(self.tradition_combo)
        self.tradition_selector.addStretch()
        layout.addLayout(self.tradition_selector)

        # Depth/Level controls
        self.controls_layout = QHBoxLayout()
        self.controls_layout.addWidget(QLabel("Depth/Level:"))
        self.depth_slider = QComboBox()
        for i in range(1, 8):
            self.depth_slider.addItem(str(i))
        self.depth_slider.currentTextChanged.connect(self._on_depth_changed)
        self.controls_layout.addWidget(self.depth_slider)
        self.controls_layout.addStretch()
        layout.addLayout(self.controls_layout)

        # Highlight controls
        self.highlight_layout = QHBoxLayout()
        self.highlight_layout.addWidget(QLabel("Highlight:"))
        self.highlight_combo = QComboBox()
        self.highlight_combo.addItem("(none)")
        for mod_name in MODULE_ORDER:
            mod = MODULE_SEMANTICS.get(mod_name, {})
            symbol = mod.get("symbol", "?")
            self.highlight_combo.addItem(f"{symbol} ({mod_name})")
        self.highlight_combo.currentTextChanged.connect(self._on_highlight_changed)
        self.highlight_layout.addWidget(self.highlight_combo)
        self.highlight_layout.addStretch()
        layout.addLayout(self.highlight_layout)

    def _on_geometry_changed(self, index):
        """Switch to the selected geometry view."""
        self.stack.setCurrentIndex(index)
        
        # Show/hide controls based on geometry
        geometry_key = self.geometry_names[index][1]
        self.tradition_selector.setVisible(geometry_key == "mandala")
        self.controls_layout.setVisible(geometry_key in ["flower", "sriyantra"])
        self.highlight_layout.setVisible(geometry_key in ["torus", "yggdrasil", "sriyantra"])

    def _on_tradition_changed(self, tradition):
        """Update mandala with selected tradition."""
        if tradition == "(none)":
            self.mandala_view.set_tradition(None)
        else:
            self.mandala_view.set_tradition(tradition)

    def _on_depth_changed(self, depth):
        """Update flower or sriyantra with depth level."""
        current_index = self.stack.currentIndex()
        geometry_key = self.geometry_names[current_index][1]
        
        if geometry_key == "flower":
            self.flower_view.set_depth(int(depth))
        elif geometry_key == "sriyantra":
            self.sriyantra_view.set_level(int(depth))

    def _on_highlight_changed(self, text):
        """Update highlight on current geometry."""
        if text == "(none)":
            symbol = None
        else:
            # Extract symbol from text like "∅ (bios)"
            symbol = text.split()[0]
        
        current_index = self.stack.currentIndex()
        geometry_key = self.geometry_names[current_index][1]
        
        if geometry_key == "torus":
            self.torus_view.set_highlight(symbol)
        elif geometry_key == "yggdrasil":
            self.yggdrasil_view.set_highlight(symbol)
        elif geometry_key == "sriyantra":
            self.sriyantra_view.set_highlight(symbol)

    def set_highlight_from_comprehension(self, symbols):
        """Set highlight based on comprehension layer results."""
        if symbols and self.stack.currentIndex() == 1:  # Torus
            self.torus_view.set_highlight(symbols[0] if symbols else None)
        elif symbols and self.stack.currentIndex() == 2:  # Yggdrasil
            self.yggdrasil_view.set_highlight(symbols[0] if symbols else None)
        elif symbols and self.stack.currentIndex() == 4:  # SriYantra
            self.sriyantra_view.set_highlight(symbols[0] if symbols else None)


class KnowledgeRenderer(QWidget):
    """Interactive knowledge explorer: sacred geometry + mandala + info panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create geometry selector (which includes all sacred geometry views)
        self.geometry_selector = GeometrySelector()
        layout.addWidget(self.geometry_selector, stretch=1)

        # Info panel
        self.info_panel = QTextBrowser()
        self.info_panel.setStyleSheet(
            "background-color: #111; color: #E0E0E0; "
            "border: 1px solid #333; font-family: Consolas;"
        )
        self.info_panel.setHtml(
            "<h3>TAZV Knowledge Renderer</h3>"
            "<p>Select a sacred geometry and explore the knowledge.</p>"
            "<p>R-7: \u2205 \u2192 \u00ac \u2192 \u2206 \u2192 1 \u2192 \u2316 \u2192 \u222e \u2192 \u27e1</p>"
        )
        layout.addWidget(self.info_panel, stretch=1)

    def set_tradition(self, tradition_name):
        """Set the tradition for the mandala view."""
        self.geometry_selector.mandala_view.set_tradition(tradition_name)
        self.geometry_selector.tradition_combo.setCurrentText(tradition_name if tradition_name else "(none)")

    def set_highlight_symbols(self, symbols):
        """Set highlight based on comprehension layer results."""
        self.geometry_selector.set_highlight_from_comprehension(symbols)
        
        # Also update info panel
        if symbols:
            html_parts = ["<h3>Comprehension Highlights</h3>"]
            html_parts.append("<p><b>Highlighted symbols:</b> " + ", ".join(symbols) + "</p>")
            
            # Get tradition references for these symbols
            from comprehension.core.rozetni_kamni import get_cross_references
            for symbol in symbols:
                refs = get_cross_references(symbol)
                if refs:
                    html_parts.append(f"<p><b>{symbol}</b> found in:")
                    for ref in refs[:5]:  # Limit to first 5
                        html_parts.append(f"  - {ref['tradition']}: {ref['term']}")
            
            self.info_panel.setHtml("\n".join(html_parts))

    def set_depth(self, depth):
        """Set depth for flower or sriyantra."""
        self.geometry_selector.depth_slider.setCurrentText(str(depth))

    def set_geometry(self, geometry_name):
        """Switch to a specific geometry view."""
        for i, (name, key) in enumerate(self.geometry_selector.geometry_names):
            if name == geometry_name:
                self.geometry_selector.geometry_combo.setCurrentIndex(i)
                self.geometry_selector.stack.setCurrentIndex(i)
                break


def _get_refs_for_glyph(glyph, exclude=""):
    """Helper: get cross-references excluding one tradition."""
    results = []
    for trad_name, trad in TRADITIONS.items():
        if trad["name"] == exclude:
            continue
        for native, (root_op, math_prop) in trad["mappings"].items():
            if root_op == glyph:
                results.append({
                    "tradition": trad["name"],
                    "native_term": native,
                })
    return results
