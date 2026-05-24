from rich.text import Text

class TextCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Braille pixel buffer (2x horizontal, 4x vertical resolution)
        self.pixels = [[0 for _ in range(width * 2)] for _ in range(height * 4)]
        self.pixel_styles = [[None for _ in range(width * 2)] for _ in range(height * 4)]
        # Text buffer (overrides braille)
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]
        self.styles = [[None for _ in range(width)] for _ in range(height)]
        # Deferred text overlays (applied last during render)
        self.overlays = []

    def draw_pixel(self, px: int, py: int, style: str = None):
        if 0 <= px < self.width * 2 and 0 <= py < self.height * 4:
            self.pixels[py][px] = 1
            if style:
                self.pixel_styles[py][px] = style

    def draw_line(self, cx0: float, cy0: float, cx1: float, cy1: float, char: str = None, style: str = None):
        # char is ignored since we draw with pixels
        x0, y0 = int(cx0 * 2), int(cy0 * 4)
        x1, y1 = int(cx1 * 2), int(cy1 * 4)
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            self.draw_pixel(x0, y0, style)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_directed_line(self, cx0: float, cy0: float, cx1: float, cy1: float, char: str = None, style: str = None, arrow_color: str = None):
        self.draw_line(cx0, cy0, cx1, cy1, char, style)
        import math
        dx = cx1 - cx0
        dy = cy1 - cy0
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
            
        nx = dx / dist
        ny = dy / dist
        
        # Back off from cx1, cy1 to be outside the 5x3 node box
        arr_x = int(cx1 - nx * 3.5)
        arr_y = int(cy1 - ny * 2.2)
        
        if abs(dx) > abs(dy):
            arrow = ">" if dx > 0 else "<"
        else:
            arrow = "v" if dy > 0 else "^"
        
        self.overlays.append((arr_x, arr_y, arrow, arrow_color or style))

    def draw_orthogonal_edge(self, cx0: float, cy0: float, cx1: float, cy1: float, directed: bool = False, arrow: str = None, style: str = None, arrow_color: str = None):
        mid_y = (cy0 + cy1) / 2
        # Vertical drop from parent
        self.draw_line(cx0, cy0, cx0, mid_y, style=style)
        # Horizontal across
        self.draw_line(cx0, mid_y, cx1, mid_y, style=style)
        # Vertical drop to child
        self.draw_line(cx1, mid_y, cx1, cy1, style=style)
        
        arr_char = None
        arr_x, arr_y = None, None
        
        if arrow:
            arr_char = arrow
            if arrow == "v":
                arr_x, arr_y = int(cx1), int(cy1)
            elif arrow == "^":
                arr_x, arr_y = int(cx0), int(cy0)
        elif directed:
            arr_char = "v"
            arr_x, arr_y = int(cx1), int(cy1)
            
        if arr_char is not None:
            self.overlays.append((arr_x, arr_y, arr_char, arrow_color or style))

    def draw_char(self, x: int, y: int, char: str, style: str = None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char
            if style:
                self.styles[y][x] = style

    def draw_text(self, x: int, y: int, text: str, style: str = None):
        for i, char in enumerate(text):
            self.draw_char(x + i, y, char, style)

    def draw_node(self, cx: int, cy: int, label: str, style: str = None):
        val = f"{str(label):^3}"
        self.draw_text(cx - 2, cy - 1, "╭───╮", style)
        self.draw_text(cx - 2, cy,     f"│{val}│", style)
        self.draw_text(cx - 2, cy + 1, "╰───╯", style)
        
        # Clear pixels behind the node so lines don't bleed through
        for y in range((cy - 1) * 4, (cy + 2) * 4):
            for x in range((cx - 2) * 2, (cx + 3) * 2):
                if 0 <= x < self.width * 2 and 0 <= y < self.height * 4:
                    self.pixels[y][x] = 0

    def _get_braille_char(self, x: int, y: int) -> tuple[str, str]:
        dots = [1, 8, 2, 16, 4, 32, 64, 128]
        val = 0x2800
        style_counts = {}
        idx = 0
        for dy in range(4):
            for dx in range(2):
                px, py = x * 2 + dx, y * 4 + dy
                if self.pixels[py][px]:
                    val += dots[idx]
                    st = self.pixel_styles[py][px]
                    if st:
                        style_counts[st] = style_counts.get(st, 0) + 1
                idx += 1
                
        if val == 0x2800:
            return " ", None
        
        dominant_style = None
        if style_counts:
            dominant_style = max(style_counts, key=style_counts.get)
            
        return chr(val), dominant_style

    def render(self) -> Text:
        for x, y, char, style in self.overlays:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.buffer[y][x] = char
                if style:
                    self.styles[y][x] = style

        res = Text()
        for y in range(self.height):
            current_style = None
            current_chunk = ""
            for x in range(self.width):
                char = self.buffer[y][x]
                style = self.styles[y][x]
                
                if char == " ":
                    b_char, b_style = self._get_braille_char(x, y)
                    if b_char != " ":
                        char = b_char
                        style = b_style
                
                if style != current_style:
                    if current_chunk:
                        res.append(current_chunk, style=current_style)
                        current_chunk = ""
                    current_style = style
                current_chunk += char
            if current_chunk:
                res.append(current_chunk, style=current_style)
            res.append("\n")
        return res
