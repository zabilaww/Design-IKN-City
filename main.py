from PIL import Image, ImageTk
import tkinter as tk
import random

# Konstanta ukuran peta
MAP_SIZE = 150
CELL_SIZE = 32  # Disesuaikan dengan ukuran gambar per cell

# Konstanta untuk berbagai jenis jalan
EMPTY = 0
ROAD = 'road'
PERSIMPANGAN = 'persimpangan'
JALAN_T = 'jalan_t'
TURN = 'turn'

# Batas jumlah jenis jalan
PERSIMPANGAN_LIMIT = 8
JALAN_T_LIMIT = 10
TURN_LIMIT = 20

# Jarak minimal antara jalan
MIN_DISTANCE = 5

# Konstanta ukuran bangunan
BIG_BUILDING = 'big_building'
MEDIUM_BUILDING = 'medium_building'
SMALL_BUILDING = 'small_building'
HOUSE = 'house'
TREE = 'tree'
LAKE = 'lake'

BUILDING_SIZES = {
    BIG_BUILDING: (10, 5),
    MEDIUM_BUILDING: (5, 3),
    SMALL_BUILDING: (2, 2),
    HOUSE: (1, 2),
    TREE: (1, 1),
    LAKE: (4, 4)
}

BUILDING_IMAGES = {
    BIG_BUILDING: 'big_building.png',
    MEDIUM_BUILDING: 'medium_building.png',
    SMALL_BUILDING: 'small_building.png',
    HOUSE: 'house.png',
    TREE: 'tree.png',
    LAKE: 'lake.png'
}

BUILDING_MINIMUMS = {
    BIG_BUILDING: 50,
    MEDIUM_BUILDING: 100,
    SMALL_BUILDING: 250,
    HOUSE: 500,
    TREE: 500,
    LAKE: 5  # Define minimum number of lakes
}

class MapGenerator:
    def __init__(self, size):
        self.size = size
        self.map = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.generate_map()
    
    def generate_map(self):
        # Clear the map
        self.map = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        persimpangan_count = 0
        jalan_t_count = 0
        turn_count = 0

        while persimpangan_count < PERSIMPANGAN_LIMIT or jalan_t_count < JALAN_T_LIMIT or turn_count < TURN_LIMIT:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            if self.map[x][y] == EMPTY and self.is_location_valid(x, y):
                if persimpangan_count < PERSIMPANGAN_LIMIT:
                    self.map[x][y] = PERSIMPANGAN
                    self.extend_road(x, y, 'up')
                    self.extend_road(x, y, 'down')
                    self.extend_road(x, y, 'left')
                    self.extend_road(x, y, 'right')
                    persimpangan_count += 1
                elif jalan_t_count < JALAN_T_LIMIT:
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    if direction == 'up':
                        self.map[x][y] = 't_atas'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down':
                        self.map[x][y] = 't_bawah'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'left':
                        self.map[x][y] = 't_kiri'
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    elif direction == 'right':
                        self.map[x][y] = 't_kanan'
                        self.extend_road(x, y, 'right')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    jalan_t_count += 1
                elif turn_count < TURN_LIMIT:
                    direction = random.choice(['up-right', 'up-left', 'down-right', 'down-left'])
                    if direction == 'up-right':
                        self.map[x][y] = 'turn_right_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'right')
                    elif direction == 'up-left':
                        self.map[x][y] = 'turn_left_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                    elif direction == 'down-right':
                        self.map[x][y] = 'turn_right_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down-left':
                        self.map[x][y] = 'turn_left_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                    turn_count += 1

        self.place_buildings()
        self.place_trees()
        self.place_lakes()

    def is_location_valid(self, x, y, width=1, height=1):
        for i in range(max(0, x - MIN_DISTANCE), min(self.size, x + width + MIN_DISTANCE)):
            for j in range(max(0, y - MIN_DISTANCE), min(self.size, y + height + MIN_DISTANCE)):
                if self.map[i][j] != EMPTY:
                    return False
        return True

    def extend_road(self, x, y, direction):
        if direction == 'up':
            for i in range(x-1, -1, -1):
                if self.map[i][y] != EMPTY:
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'down':
            for i in range(x+1, self.size):
                if self.map[i][y] != EMPTY:
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'left':
            for j in range(y-1, -1, -1):
                if self.map[x][j] != EMPTY:
                    break
                self.map[x][j] = 'horizontal_road'
        elif direction == 'right':
            for j in range(y+1, self.size):
                if self.map[x][j] != EMPTY:
                    break
                self.map[x][j] = 'horizontal_road'

    def place_buildings(self):
        for building, minimum in BUILDING_MINIMUMS.items():
            if building == TREE or building == LAKE:
                continue
            count = 0
            while count < minimum:
                x = random.randint(0, self.size - BUILDING_SIZES[building][0])
                y = random.randint(0, self.size - BUILDING_SIZES[building][1])
                if self.is_location_valid_for_building(x, y, BUILDING_SIZES[building][0], BUILDING_SIZES[building][1]):
                    for i in range(x, x + BUILDING_SIZES[building][0]):
                        for j in range(y, y + BUILDING_SIZES[building][1]):
                            self.map[i][j] = building
                    count += 1

    def place_trees(self):
        count = 0
        while count < BUILDING_MINIMUMS[TREE]:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.map[x][y] == EMPTY:
                self.map[x][y] = TREE
                count += 1

    def place_lakes(self):
        count = 0
        while count < BUILDING_MINIMUMS[LAKE]:
            x = random.randint(0, self.size - BUILDING_SIZES[LAKE][0])
            y = random.randint(0, self.size - BUILDING_SIZES[LAKE][1])
            if self.is_location_valid_for_building(x, y, BUILDING_SIZES[LAKE][0], BUILDING_SIZES[LAKE][1]):
                for i in range(x, x + BUILDING_SIZES[LAKE][0]):
                    for j in range(y, y + BUILDING_SIZES[LAKE][1]):
                        self.map[i][j] = LAKE
                count += 1

    def is_location_valid_for_building(self, x, y, width, height):
        # Check if any cell in the proposed area is a road or another building
        for i in range(x, x + width):
            for j in range(y, y + height):
                if i >= 0 and i < self.size and j >= 0 and j < self.size:
                    if self.map[i][j] != EMPTY:
                        return False
        # Check the surrounding cells for roads within 1 cell distance
        road_found = False
        for i in range(max(0, x - 1), min(self.size, x + width + 1)):
            for j in range(max(0, y - 1), min(self.size, y + height + 1)):
                if self.map[i][j] in ['vertical_road', 'horizontal_road', 'PERSIMPANGAN', 't_atas', 't_bawah', 't_kiri', 't_kanan', 'turn_right_up', 'turn_left_up', 'turn_right_down', 'turn_left_down']:
                    road_found = True
                # Ensure a minimum distance of 2 cells from other buildings
                if i in range(x, x + width) and j in range(y, y + height):
                    continue
                if self.map[i][j] in BUILDING_SIZES:
                    return False
        return road_found

    def get_map(self):
        return self.map

class MapDisplay(tk.Frame):
    def __init__(self, parent, map_data):
        super().__init__(parent)
        self.parent = parent
        self.map_data = map_data

        # Load images
        self.images = {
            'vertical_road': ImageTk.PhotoImage(Image.open("img/road/vertical_road.png")),
            'horizontal_road': ImageTk.PhotoImage(Image.open("img/road/horizontal_road.png")),
            'persimpangan': ImageTk.PhotoImage(Image.open("img/road/persimpangan.png")),
            't_atas': ImageTk.PhotoImage(Image.open("img/road/t_atas.png")),
            't_bawah': ImageTk.PhotoImage(Image.open("img/road/t_bawah.png")),
            't_kiri': ImageTk.PhotoImage(Image.open("img/road/t_kiri.png")),
            't_kanan': ImageTk.PhotoImage(Image.open("img/road/t_kanan.png")),
            'turn_left_down': ImageTk.PhotoImage(Image.open("img/road/turn_left_down.png")),
            'turn_left_up': ImageTk.PhotoImage(Image.open("img/road/turn_left_up.png")),
            'turn_right_up': ImageTk.PhotoImage(Image.open("img/road/turn_right_up.png")),
            'turn_right_down': ImageTk.PhotoImage(Image.open("img/road/turn_right_down.png")),
            BIG_BUILDING: ImageTk.PhotoImage(Image.open(f"img/building/{BUILDING_IMAGES[BIG_BUILDING]}")),
            MEDIUM_BUILDING: ImageTk.PhotoImage(Image.open(f"img/building/{BUILDING_IMAGES[MEDIUM_BUILDING]}")),
            SMALL_BUILDING: ImageTk.PhotoImage(Image.open(f"img/building/{BUILDING_IMAGES[SMALL_BUILDING]}")),
            HOUSE: ImageTk.PhotoImage(Image.open(f"img/building/{BUILDING_IMAGES[HOUSE]}")),
            TREE: ImageTk.PhotoImage(Image.open(f"img/{BUILDING_IMAGES[TREE]}")),
            LAKE: ImageTk.PhotoImage(Image.open(f"img/{BUILDING_IMAGES[LAKE]}")),  # Load lake image
            'grass': ImageTk.PhotoImage(Image.open("img/grass.png"))  # Tambahkan gambar rumput
        }

        # Frame untuk kanvas peta dan tombol
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Kanvas untuk menampilkan peta dengan scrollbars
        self.canvas = tk.Canvas(self.main_frame, bg="white", scrollregion=(0, 0, MAP_SIZE * CELL_SIZE, MAP_SIZE * CELL_SIZE))
        self.canvas.grid(row=1, column=0, sticky=tk.NSEW)
        
        self.hbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=2, column=0, sticky=tk.EW)
        self.vbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=1, column=1, sticky=tk.NS)
        
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.draw_map()

        # Frame untuk tombol
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

        self.redesign_button = tk.Button(self.button_frame, text="Redesign", command=self.redesign_map, bg="red", fg="white")
        self.redesign_button.pack()

    def draw_map(self):
        self.canvas.delete("all")
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell_type = self.map_data[i][j]
                if cell_type in self.images:
                    if cell_type in BUILDING_SIZES:
                        building_size = BUILDING_SIZES[cell_type]
                        if self.is_top_left_of_building(i, j, building_size):
                            self.canvas.create_image(j * CELL_SIZE, i * CELL_SIZE, anchor=tk.NW, image=self.images[cell_type])
                    else:
                        self.canvas.create_image(j * CELL_SIZE, i * CELL_SIZE, anchor=tk.NW, image=self.images[cell_type])
                else:
                    self.canvas.create_image(j * CELL_SIZE, i * CELL_SIZE, anchor=tk.NW, image=self.images['grass'])

    def is_top_left_of_building(self, i, j, building_size):
        if i + building_size[0] <= MAP_SIZE and j + building_size[1] <= MAP_SIZE:
            for x in range(building_size[0]):
                for y in range(building_size[1]):
                    if self.map_data[i + x][j + y] != self.map_data[i][j]:
                        return False
            return True
        return False

    def redesign_map(self):
        # Generate new map data
        map_generator = MapGenerator(MAP_SIZE)
        self.map_data = map_generator.get_map()
        # Redraw map
        self.draw_map()

def main():
    root = tk.Tk()
    root.title("Map")

    map_generator = MapGenerator(MAP_SIZE)
    map_data = map_generator.get_map()
    map_display = MapDisplay(root, map_data)
    map_display.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
